from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
from image_check import is_original_image
import ai_filters
from flask_bcrypt import Bcrypt
import os
import re
from pymongo import MongoClient
import datetime
import uuid
import random
from chatbot import get_reply


# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
mongo_pass = 'er0br8UTpHbU56Ir'
client = MongoClient(f'mongodb+srv://hiralgujrathi7:{mongo_pass}@travel.aarhqxn.mongodb.net/?retryWrites=true&w=majority')
db = client['myblogdb']


# Create User collection object
users_collection = db['User']
blog_collection = db['Blog']
comment_collection = db['Comments']
likes_collection = db['Likes']
chat_collection = db['Chat']
notifications_collection = db['notifications']

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'testKey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({'username': user_id})
    if not user_data:
        return None
    return User(user_data['username'])


class User(UserMixin):
    def __init__(self, username, email=''):
        self.username = username
        self.id = username
        self.email = email

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


all_categories = {'Beaches': 8, 'Mountains/Hill Stations': 5, 'National Parks/Wildlife Sanctuaries': 3, 'Historical/Cultural sites': 9, 'Theme Parks/Adventure': 7,
                  'Artistic destinations': 4, 'Deserts': 6, 'Dams/Lakes': 1, 'Religious/Spiritual destinations': 0, 'Educational destinations': 2, 'Cities': 7}

tag_categories = {
    'Beaches': '1',
    'Mountains/Hill Stations': '2',
    'National Parks/Wildlife Sanctuaries': '3',
    'Historical/Cultural sites': '4',
    'Theme Parks/Adventure (e.g., trekking, skiing, rafting, bungee jumping)': '5',
    'Artistic destinations': '6',
    'Deserts': '7',
    'Dams/Lakes': '8',
    'Religious/Spiritual destinations': '9',
    'Educational destinations': '10',
    'Cities': '11',
    'Others': '12'
}

tag_dict = {
    '1': 'Beaches',
    '2': 'Mountains/Hill Stations',
    '3': 'National Parks/Wildlife Sanctuaries',
    '4': 'Historical/Cultural sites',
    '5': 'Theme Parks/Adventure (e.g., trekking, skiing, rafting, bungee jumping)',
    '6': 'Artistic destinations',
    '7': 'Deserts',
    '8': 'Dams/Lakes',
    '9': 'Religious/Spiritual destinations',
    '10': 'Educational destinations',
    '11': 'Cities',
    '12': 'Others'
}


@app.route("/")
def home():
    category = request.args.get('category')
    keyword = request.args.get('keyword')
    title_ = None
    if category:
        blogs = blog_collection.find({'category': category}, {
                                     '_id': 0}).sort('date', -1)
        blogs = [blog for blog in blogs]

    elif keyword:
        blogs = []
        if False:
            blogs = blog_collection.find({}).sort('datetime', -1)
            for b in blogs:
                result = ai_filters.rake_algorithm(b['title']).extend(ai_filters.rake_algorithm(b['blog_post']))
                for r in result:
                    if keyword.strip() in r:
                        blogs.append(b)
                        
        else:
            ## Search by mongo methods
            blogs = blog_collection.find({"$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"blog_post": {"$regex": keyword, "$options": "i"}}
            ]}, {'_id': 0}).sort('date', -1)
            blogs = [blog for blog in blogs]


    else:
        title_ = 'Top 10 Blogs'
        blogs = blog_collection.find({}, {'_id': 0}).sort('date', -1)
        blogs = [blog for blog in blogs]

        most_liked = {}
        likes = likes_collection.find({}, {'_id': 0})
        for l in likes:
            if most_liked.get(l['blog_id']):
                most_liked[l['blog_id']] += 1
            else:
                most_liked[l['blog_id']] = 1

        sorted_most_liked = sorted(
            most_liked.items(), key=lambda x: x[1], reverse=True)

        # Create a final list of blogs sorted by most likes
        final_list = []
        for blog_id, _ in sorted_most_liked:
            for blog in blogs:
                if blog.get('blog_id') == blog_id:
                    final_list.append(blog)
                    break

        for blog in blogs:
            if blog not in final_list:
                final_list.append(blog)
                blogs = final_list

    # Query the Blog collection to get the blogs
    likes_ = likes_collection.find({}, {'_id': 0}).sort('date', -1)
    recommendation_blog_ids = ai_filters.recommendation_functionality(
        session.get('user_id', 'test'), list(likes_))

    recom_blogs = blog_collection.find({}, {'_id': 0}).sort('date', -1)
    recom_blogs = [blog for blog in recom_blogs]
    recommendations = []
    for b in recom_blogs:
        if b['blog_id'] in recommendation_blog_ids:
            recommendations.append(b)

    if len(recommendations) > 3:
        recommendations = random.sample(blogs, 3)

    return render_template('index.html', blogs=blogs, recommended=recommendations, all_categories=all_categories, is_admin=session.get('user_type', False), search=keyword, title=title_)


@app.route("/weekend")
@login_required
def weekend():
    user_ip = request.remote_addr
    user_location = ai_filters.get_location(user_ip)

    locations = ai_filters.weekend_planner(user_location.get('region', ''))

    return render_template('weekend.html', locations=locations, is_admin=session.get('user_type', False))


@app.route("/chatbot", methods=['GET', 'POST'])
@login_required
def chatbot():
    user_id = session.get('user_id', 'test')

    if request.method == 'POST':
        message = request.form['message']
        reply = get_reply(message)
        chat_collection.insert_one({'user_id': user_id, 'message': message, 'reply': reply,
                                   'datetime': datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})

        chats = chat_collection.find({'user_id': user_id}, {
                                     '_id': 0}).sort('datetime', 1)
        return render_template('chatbot.html', chats=chats, is_admin=session.get('user_type', False))
    chats = chat_collection.find({'user_id': user_id}, {
                                 '_id': 0}).sort('datetime', 1)
    return render_template('chatbot.html', chats=chats, is_admin=session.get('user_type', False))


@app.route("/analytics")
@login_required
def analytics():
    user_id = session.get('user_id')
    if not user_id:
        return render_template('analytics.html', is_admin=session.get('user_type', False))

    comments = comment_collection.find({}, {'_id': 0})
    likes = likes_collection.find({}, {'_id': 0})
    blogs = blog_collection.find({'user_id': user_id}, {'_id': 0})

    analytics = {}

    for b in blogs:
        if analytics.get(b['blog_id']):
            analytics[b['blog_id']]['title'] = b['title']
            analytics[b['blog_id']]['datetime'] = b['datetime']
        else:
            analytics[b['blog_id']] = {
                'title': b['title'], 'datetime': b['datetime'], 'comments': 0, 'likes': 0}

    for c in comments:
        if analytics.get(c['blog_id']):
            analytics[c['blog_id']]['comments'] += 1

    for l in likes:
        if analytics.get(l['blog_id']):
            analytics[l['blog_id']]['likes'] += 1


    totalLikes, totalComments = 0, 0
    for a in analytics.values():
        totalLikes += a['likes']
        totalComments += a['comments']

    return render_template('analytics.html', is_admin=session.get('user_type', False), analytics=analytics, totalLikes=totalLikes, totalComments=totalComments)


@app.route('/add_comment', methods=['POST'])
def add_comment():
    blog_id = request.args.get('blog_id')
    if not blog_id:
        return 'No blog id'

    subject = request.form['subject']
    message = request.form['message']
    comment = {'name': session.get('user_id', 'Guest'), 'subject': subject, 'message': message,
               "datetime": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
               "blog_id": blog_id
               }
    comment_collection.insert_one(comment)
    flash('Comment added successfully', 'success')

    return redirect('/blog?id={}'.format(blog_id))


@app.route('/add_like', methods=['GET'])
def add_like():
    blog_id = request.args.get('blog_id')
    if not blog_id:
        return 'No blog id'

    name = session.get('user_id', 'test')

    like = {
            'name': name,
            "datetime": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
            "blog_id": blog_id
            }

    # check if already liked this blog by the user
    mylike = likes_collection.find_one({'name': name, 'blog_id': blog_id})
    if mylike:
        likes_collection.delete_one(mylike)
    else:
        likes_collection.insert_one(like)
    return redirect('/blog?id={}'.format(blog_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Check if user has submitted the registration form
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        account_type = request.form.get('account_type')

        user_ip = request.remote_addr
        user_location = ai_filters.get_location(user_ip)
        location = user_location.get('city', '') + ', ' + user_location.get('region', '')
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if password matches the confirm password
        if password != confirm_password:
            flash('Passwords do not match', 'warning')
            return render_template('register.html', error='Passwords do not match')

        # Check if the user already exists in the database
        user = users_collection.find_one(
            {"$or": [{"username": username}, {"email": email}]})

        if account_type == 'creator':
            session['user_type'] = account_type

        # If user already exists, show an error message
        if user:
            flash('User already exists', 'warning')
            return render_template('register.html', error='Username or email already exists')

        # Insert the new user into the User collection
        user_data = {
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": pw_hash,
            "account_type": account_type,
            "location": location
        }
        users_collection.insert_one(user_data)

        # Redirect the user to the login page
        return redirect('/login')

    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Check if user has submitted the login form
    if request.method == 'POST':
        # Get user input from the form
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        print(password, username_or_email)
        # Check if the username or email exists in the database
        user = users_collection.find_one(
            {'$or': [{'username': username_or_email}, {'email': username_or_email}]})
        # If user exists, check if the password is correct
        # if user and user['password'] == password:
        if user:
            if bcrypt.check_password_hash(user['password'], request.form['password']):
                # Log the user in and redirect to the home page
                user_obj = User(user['username'])
                login_user(user_obj, remember=True)
                session['user_id'] = user['username']
                flash("Successful Login", "success")

                if user['account_type'] == 'creator' or user['account_type'] == 'on':
                    session['user_type'] = user['account_type']
                    flash("Successful Login", "success")
                return redirect(url_for('home'))
            else:
                flash('Incorrect Username/Email or Password', 'danger')
            # If user does not exist or password is incorrect, show an error message
                return render_template('login.html', error='Invalid username/email or password')

    # If the user has not submitted the login form, show the login form
    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('register'))


# Route to create a new blog post
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():

    if request.method == 'POST':
        # Get user input from the form
        title = request.form['title']
        blog_post = request.form['blog_post']
        means_of_travel = request.form['means_of_travel']
        category = request.form['category']
        location = request.form.get('location', '')
        image = request.files['image'] if 'image' in request.files else None
        # Get the user id from the session
        user_id = session.get('user_id', "test")

        # checking for profanity
        if ai_filters.check_profanity(title) or ai_filters.check_profanity(blog_post):
            flash('Profanity is not allowed', 'danger')
            return redirect(url_for('create_post'))

        # check for duplicate article
        if ai_filters.is_plagiarism(text,threshold):
            flash('Plagiarism is not allowed', 'danger')
            return redirect(url_for('create_post'))

        # Create a new document for the blog post
        new_blog = {
            "title": title,
            "blog_post": blog_post,
            "means_of_travel": means_of_travel,
            "category": tag_dict[category],
            "location": location,
            "user_id": user_id,
            "datetime": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
            "blog_id": uuid.uuid4().hex[:8]
        }

        # If image is uploaded, save it to the file system and insert the image path into the Image table
        if image:
            image_filename = image.filename
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)
            new_blog['image_filename'] = image_filename
            new_blog['image_path'] = image_path

            # Test image if original or not
            if not is_original_image(image_path):
                flash('Image is not original', 'danger')
                return redirect(url_for('create_post'))

        # Insert the new blog post into the Blog collection
        blog_collection.insert_one(new_blog).inserted_id

        # Redirect the user to the home page
        return redirect('/')

    # If the user has not submitted the create post form, show the create post form
    return render_template('create_blog.html', is_admin=session.get('user_type', False))


# Route to fetch blogs with limit and offset
@app.route('/my-blogs', methods=['GET'])
@app.route('/blogs', methods=['GET'])
@login_required
def get_blogs():
    user_id = session.get('user_id', "test")
    limit, offset = request.args.get('limit', 0), request.args.get('offset', 0)
    # Query the Blog collection to get the blogs with limit and offset
    blogs = blog_collection.find({'user_id': user_id}, {'_id': 0}).sort(
        'date', -1).skip(offset).limit(limit)

    blogs = [blog for blog in blogs]

    return render_template('myBlogs.html', blogs=blogs, is_admin=session.get('user_type', False))


# Route to fetch single blog
@app.route('/blog', methods=['GET'])
@login_required
def get_single_blog():

    blog_id = request.args.get('id')
    # Query the Blog collection to get the blog with the specified title
    blog = blog_collection.find_one({'blog_id': blog_id}, {'_id': 0})

    comments = comment_collection.find({'blog_id': blog_id}, {'_id': 0})
    likes = likes_collection.find({'blog_id': blog_id}, {'_id': 0})
    mylike = likes_collection.find_one({'name':session.get('user_id', 'Guest'), 'blog_id': blog_id}, {'_id': 0})
    print(mylike,  session.get('user_id', 'Guest'))
    comments = list(comments)

    # Query the Blog collection to get the blogs
    likes_ = likes_collection.find({}, {'_id': 0}).sort('date', -1)
    recommendation_blog_ids = ai_filters.recommendation_functionality(
        session.get('user_id', 'test'), list(likes_))

    blogs = blog_collection.find({}, {'_id': 0}).sort('date', -1)
    blogs = [blog for blog in blogs]
    recommendations = []
    for b in blogs:
        if b['blog_id'] in recommendation_blog_ids:
            recommendations.append(b)

    if len(recommendations) > 3:
        recommendations = random.sample(blogs, 3)

    return render_template('single_blog.html', blog=blog, comments=comments, likes=len(list(likes)), recommendations=recommendations,  is_admin=session.get('user_type', False), mylike=mylike)


# Route to delete a blog by ID
@app.route('/delete-blog/<string:id>', methods=['GET'])
@login_required
def delete_blog(id):

    # Delete the blog with the specified ID from the blogs collection
    # result = blog_collection.delete_one({'_id': ObjectId(id)})
    result = blog_collection.delete_one({'blog_id': id})

    # Check if the deletion was successful
    if result.deleted_count == 1:
        # Return a JSON response indicating that the blog was deleted
        return redirect('/blogs')
    else:
        # Return a JSON response indicating that the blog could not be found
        return jsonify({'status': 'error', 'message': f'Blog with ID {id} not found.'})


# Route to update a blog by ID
@app.route('/update-blog', methods=['GET', 'POST'])
@login_required
def update_blog():

    id = request.args.get('id')

    # Get the blog with the specified ID from the database
    blog = blog_collection.find_one({'blog_id': id})
    # Check if the current user is the creator of the blog
    if blog['user_id'] != session['user_id']:
        return jsonify({'status': 'error', 'message': 'You are not authorized to edit this blog.'})

    if request.method == 'POST':
        # Get user input from the form
        title = request.form['title']
        blog_post = request.form['blog_post']
        means_of_travel = request.form['means_of_travel']
        category = request.form['category']
        location = request.form.get('location', '')
        image = request.files['image'] if 'image' in request.files else None

        # checking for profanity
        if ai_filters.check_profanity(title) or ai_filters.check_profanity(blog_post):
            flash('Profanity is not allowed', 'danger')
            return redirect(url_for('create_post'))

        # Create a new document for the blog post
        new_blog = {
            "title": title,
            "blog_post": blog_post,
            "means_of_travel": means_of_travel,
            "category": tag_dict[category],
            "location": location,
            "datetime": datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
        }

        # If image is uploaded, save it to the file system and insert the image path into the Image table
        if image:
            image_filename = image.filename
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)
            new_blog['image_filename'] = image_filename
            new_blog['image_path'] = image_path
                        # Test image if original or not
            if not is_original_image(image_path):
                flash('Image is not original', 'danger')
                return redirect('/blogs')

        # Update the blog with the specified ID in the Blog collection
        blog_collection.update_one({'blog_id': id}, {'$set': new_blog})

        # Redirect the user to the home page
        return redirect('/')

    return render_template('update_blog.html', blog=blog)

@app.route('/get-notifications', methods=['GET'])
def get_notifications():
    user_id=request.args.get('username')
    # Query the Blog collection to get the blogs with limit and offset
    result = notifications_collection.find({'username': user_id}, {'_id': 0}).sort(
        'created_at', -1)
    result = list(result)
    return jsonify(result)

# ADDED FROM OUR SIDE


@app.route('/check_password_strength', methods=['POST'])
def check_password_strength():
    password = request.json['password']
    strength = get_password_strength(password)
    return jsonify({'strength': strength})


def get_password_strength(password):
    # Minimum length check
    if len(password) < 8:
        return 'weak'

    # Regular expressions for checking different criteria
    has_lowercase = re.search(r'[a-z]', password)
    has_uppercase = re.search(r'[A-Z]', password)
    has_digit = re.search(r'\d', password)
    has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    # Checking different criteria
    if has_lowercase and has_uppercase and has_digit and has_special_char:
        return 'strong'
    elif has_lowercase or has_uppercase or has_digit:
        return 'medium'
    else:
        return 'weak'

if __name__ == "__main__":
    app.run(debug=True)
