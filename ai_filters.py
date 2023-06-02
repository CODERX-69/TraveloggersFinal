import requests
from profanity import profanity
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from rake_nltk import Rake
import time


def rake_algorithm(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()


# API_TOKEN = 'i2bIgiDFdWVngAL7dzokTav_svLEmtVI'

# def req1(text):
#     headers = {
#         'X-API-TOKEN': API_TOKEN,
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }

#     data = 'language=en&text={}'.format(text)

#     response = requests.post('https://plagiarismcheck.org/api/v1/text', headers=headers, data=data)
#     print(response.json())
#     return response.json()


# def req2(text_id):
#     headers = {
#         'X-API-TOKEN': API_TOKEN,
#     }

#     response = requests.get('https://plagiarismcheck.org/api/v1/text/{}'.format(text_id), headers=headers)
#     print(response)
#     return response.json()


# def req3(text_id):
#     headers = {
#         'X-API-TOKEN': API_TOKEN,
#     }

#     response = requests.get('https://plagiarismcheck.org/api/v1/text/report/{}'.format(text_id), headers=headers)
#     print(response.json())

#     return response.json()


# def is_plagiarism(text, threshold):
#     response = req1(text)
#     if response['success']:
#         text_id = response['data']['text']['id']
#         print(text_id)
#         req2(text_id)
#         interval = 1 # seconds
#         while True:
#             try:
#                 if int(req3(text_id)['data']['report']['percent']) > threshold:
#                     return True
#             except Exception as e:
#                 print(e)
#                 pass

#             time.sleep(interval)

#     return False



def check_profanity(text):
    return profanity.contains_profanity(text)


def get_location(ipaddress):
    url = "https://ipapi.co/{}/json/".format(ipaddress)

    response = requests.get(url)
    return response.json()


def recommendation_functionality(target_user_id, data):
    """
    Collaborative Filtering
    """    

    data = pd.DataFrame(data)
    
    # Initialize LabelEncoder
    label_encoder = LabelEncoder()


    try:
        # Fit and transform the user_id labels
        data['user_id'] = label_encoder.fit_transform(data['name'])
        data['blog_id'] = data['blog_id'].apply(lambda x: int(x,16))
        data['like'] = 1
        data.drop(['name'], axis=1, inplace=True)
        data.drop(['datetime'], axis=1, inplace=True)

        user_item_matrix = pd.pivot_table(data, values='like', index='user_id', columns='blog_id', fill_value=0)

        # Similarity computation
        user_similarity = cosine_similarity(user_item_matrix)

        # Recommendation generation
        similar_users = user_similarity[label_encoder.transform([target_user_id])[0]].argsort()[::-1][:10] # Get top 10 similar users

        recommended_blogs = []
        for user_id in similar_users:
            liked_blogs = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index
            for blog_id in liked_blogs:
                if user_item_matrix.loc[label_encoder.transform([target_user_id])[0]][blog_id] == 0:
                    blog_id = hex(blog_id)
                    print(blog_id)
                    if blog_id.startswith('0x'):
                        blog_id = blog_id[2:]
                        recommended_blogs.append(blog_id)
                    else:
                        recommended_blogs.append(blog_id)

        return recommended_blogs

    except Exception as e:
        print(str(e))
        return []


def weekend_planner(place):
    if place=='':
        return tourist_places.get("Maharashtra", [])
    return tourist_places.get(place, [])


tourist_places = {
     "Gujrat":[
        {"name":"Statue of Unity", "image":"static\weekend\SOU.jpg","link":""}, 
        {"name":"Pavagadh Hill", "image":"static\weekend\pavagadh.jfif","link":""}, 
        {"name":"Kankaria Lake", "image":"static\weekend\kankaria.jfif","link":""},
        {"name":"Anand", "image":"static\weekend\_anand.jfif","link":""}, 
        {"name":"Sardar Sarovar Dam ", "image":"static\weekend\SSD.jfif","link":""}, 
        {"name":"Ajwa Water Park", "image":"static\weekend\_ajwa.jfif","link":""}, 
        {"name":"Kadia Dungar Caves", "image":"static\weekend\kdc.jfif","link":""}, 
        {"name":"Hathni Mata Waterfall ", "image":"static\weekend\HMW.jfif","link":""} 
        ],
     
     "Rajasthan": [
        {"name": "Ranthambore National Park", "image": "static/images/rajasthan_ranthambore.jpg"},
        {"name": "Amber Palace", "image": "static/images/rajasthan_amber_palace.jpg"},
        {"name": "Hawa Mahal", "image": "static/images/rajasthan_hawa_mahal.jpg"},
        {"name": "City Palace, Jaipur", "image": "static/images/rajasthan_city_palace_jaipur.jpg"},
        {"name": "Umaid Bhawan Palace, Jodhpur", "image": "static/images/rajasthan_umaid_bhawan_palace.jpg"},
        {"name": "Jantar Mantar, Jaipur", "image": "static/images/rajasthan_jantar_mantar.jpg"},
        {"name": "Mehrangarh Fort Museum and Trust, Jodhpur", "image": "static/images/rajasthan_mehrangarh_fort.jpg"},
        {"name": "Jal Mahal, Jaipur", "image": "static/images/rajasthan_jal_mahal.jpg"},
        {"name": "Jaisalmer Fort", "image": "static/images/rajasthan_jaisalmer_fort.jpg"},
        {"name": "Sariska Tiger Reserve", "image": "static/images/rajasthan_sariska_tiger_reserve.jpg"},
        {"name": "Chittorgarh Fort", "image": "static/images/rajasthan_chittorgarh_fort.jpg"},
        {"name": "Jag Mandir, Udaipur", "image": "static/images/rajasthan_jag_mandir.jpg"}
    ],
    'Kerala': ['Bekal Fort', 'Bekal Beach', 'Chottanikkara Bhagavathy Temple', 'Guruvayur Temple', 'Shree Padmanabhaswamy Temple', 'Jatayu Earth’s Centre', 'Sakthan Thampuran Palace', 'Mullaperiyar Dam', 'Aralam Wildlife Sanctuary', 'Attukad Waterfalls', 'Sree Krishna Swamy Temple, Ambalapuzha', 'Lakkam Waterfalls, Munnar', 'Thusharagiri Waterfalls', 'Many places in Kochi', 'Pookode Lake'],
    'Arunachal Pradesh': ['Pasighat', 'Mechuka', 'Ziro', 'Tawang – The mighty Brahmaputra river emerges from the foothills of Pasighat under the name Siang or Dihang. Pasighat is the oldest town in Arunachal Pradesh founded in 1911 A.D. by the British Raj.'],
    'Assam': ['Sivasagar', 'Brahmaputra River – One of the major rivers of India. It flows through China, India, and Bangladesh.', 'Kamakhya Temple', 'Kaziranga National Park – This is a World Heritage Site. It has the highest density of tigers. It hosts two-thirds of the world’s one-horned rhinoceros.'],
    'Tripura': ['Ujjayanta Palace', 'Rudrasagar Lake', 'Tripura Sundari Temple', 'Unakoti'],
    'Sikkim': ['Aritar', 'Rumtek', 'Changu Lake', 'Gangtok'],
    'Mizoram': ['Vantawng Falls', 'Hmuifang', 'Thenzawl', 'Aizawl'],
    'Nagaland': ['Mokokchung', 'Pfutsero', 'Wokha', 'Khonoma'],
    'Manipur': ['Khwairamband Bazar/IMA Market', 'Moirang', 'Loktak Lake'],
    'Meghalaya': ['Mawlynnong', 'Cherrapunji', 'Shillong – the capital of Meghalaya. It is known as the “Scotland of the East.”', 'Mawphlang Sacred Grove', 'Dawki'],
    "Uttar Pradesh": [
        "Prayagraj Kumbh Mela",
        "Kashi Vishwanath Temple at Varanasi",
        "Sankat Mochan Temple at Varanasi",
        "Ganga Aarti at Varanasi",
        "Sarnath",
        "Kushinagar",
        "Ayodhya",
        "Vrindavan",
        "Taj Mahal",
        "Agra Fort",
        "Fatehpur Sikri",
        "Dudhwa National Park",
        "Jhansi Fort",
        "Okhla Bird Sanctuary",
        "Anand Bhawan Museum"
    ],
    
    "Tamil Nadu": [
        "Meenakshi Amman Temple at Madurai",
        "Rameshwaram",
        "Brihadeeswara Temple at Thanjavur",
        "Marina Beach at Chennai",
        "Shore Temple at Mahabalipuram",
        "Kodaikanal Lake",
        "Anamalai Tiger Reserve",
        "Nilgiri Mountain Railway Line",
        "Nataraja Temple at Chidambaram",
        "Monuments at Mamallapuram"
    ],
    "Delhi": [
        "India Gate", "National War Memorial", "Akshardham Temple", "Rashtrapati Bhawan", "Parliament of India", "Red Fort", "Qutub Minar", "Lotus Temple", "Juma Masjid", "Humayun’s Tomb", "Purana Qila", "Birla Mandir", "Rajghat",
        "National Rail Museum", "National Zoological Park", "National Gallery of Modern Art",
        "Khan Market"
    ],
    "West Bengal": [
        "Victoria Memorial", "Indian Museum", "Howrah Bridge", "Dakshineswar Kali Temple", "Batasia Loop", "Science City", "Kalighat", "Belur Math", "Marble Palace", "Eden Gardens",
        "Sundarban National Park", "Jaldapara National Park", "Gorumara National Park",
        "Darjeeling Himalayan Railway", "Tiger Hill",
        "Yiga Choeling Monastery", "Zoological Park, Darjeeling"
    ],
    "Karnataka": [
        "Jog Falls", "Bandipur National Park", "Nagarhole National Park", "Bannerghatta National Park",
        "Kudremukh",
        "Agumbe",
        "Madikeri",
        "Hampi", "Pattadakal",
        "Aihole", "Badami",
        "Belur", "Helebidu",
        "Shivanasamudra Falls"
    ],
    "Andhra Pradesh": [
         "Tirumala Tirupati Temple", "Simhachalam Temple", "Annavaram Temple", "Srikalahasti", "Kanaka Durga Temple",
        "Horsley Hills", "Papi Hills", "Araku Valley",
         "Belum Caves", "Undavalli Caves", "Borra Caves"
    ],
    "Maharashtra": [
        {'name': 'Rajmachi', 'image': 'static\weekend\_rajmachi.jpg', 'link':'https://maps.app.goo.gl/z3T2QfHQBPJXsPwf7'},
        {'name': 'Shaniwar Wada', 'image': 'static\weekend\Shaniwar-Wada-Pune.jpg', 'link':'https://maps.app.goo.gl/rRjapFNBFgJKRsGY9'},
        {'name': 'Sinhagad Fort', 'image': 'static\weekend\sinhgad.jfif', 'link':'https://maps.app.goo.gl/R6FxgDTv6wBxDVFXA'},
        {'name': 'Aga Khan Palace', 'image': 'static\weekend\_agaKhan.jfif', 'link':'https://maps.app.goo.gl/KQAJpoRAkGFxZaUr6'},
        {'name': 'Gateway of India', 'image': 'static\weekend\GWOI.jfif', 'link':'https://maps.app.goo.gl/1MPLHNQmQChLAgdj6'},
        {'name': 'Chhatrapati Shivaji Maharaj Terminus', 'image': 'static\weekend\CST.jfif', 'link':'https://maps.app.goo.gl/87KHJ81mcG3Vb1hy8'},
        {'name': 'Shree Siddhivinayak Ganpati Temple', 'image': 'static\weekend\siddhivinayak.jfif', 'link':'https://maps.app.goo.gl/oZWgSUwXy16R2ve7A'},
        {'name': 'Colaba Causeway', 'image': 'static\weekend\colaba.jfif', 'link':'https://maps.app.goo.gl/byQUGMgKegWkyJj28'},
        {'name': 'Crawford Market', 'image': 'static\weekend\crofrd.jfif', 'link':'https://maps.app.goo.gl/X6si7ssU2q6vwDnX6'},
        {'name': 'Trimbakeshwar Jyotirling Mandir', 'image': 'static\weekend\_trimbaeshwar.jfif', 'link':'https://maps.app.goo.gl/iCnv553k2QfDMcmC6'},
        {'name': 'Bhaja Caves', 'image': 'static\weekend\_bhaja.jfif', 'link':'https://maps.app.goo.gl/vUifpyYUFvoaA24eA'},
        {'name': 'Lonar Lake', 'image': 'static\weekend\lonar.jfif', 'link':'https://maps.app.goo.gl/a2q855CFYqyVWUtCA'},
        {'name': 'Ajanta Caves', 'image': 'static\weekend\_ajanta.jfif', 'link':'https://maps.app.goo.gl/DcyGJ2dk23v4Ca8f8'},
        {'name': 'Elephanta Caves', 'image': 'static\weekend\elephanta.jfif', 'link':'https://maps.app.goo.gl/dxDNaer11i23vwwr6'},
        {'name': 'Tadoba-Andhari National Park', 'image': 'static\weekend\_tadoba.jfif', 'link':'https://maps.app.goo.gl/T86E56RnhzUn9zmr9'},
        {'name': 'Lohagadh', 'image': 'static\weekend\lohgad.jfif', 'link':'https://maps.app.goo.gl/sJQZ5NQEZ9EtBjbx9'},
        {'name': 'Sanjay Gandhi National Park', 'image': 'static\weekend\SGNP.jfif', 'link':'https://maps.app.goo.gl/CoMWfKTCCtiLyZWH6'},
        {'name': 'Kanheri Caves', 'image': 'static\weekend\kanheri.jfif', 'link':'https://maps.app.goo.gl/Pb51qxBnrM53hT758'}

    ]
}
