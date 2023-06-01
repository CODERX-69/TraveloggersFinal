import pymongo
from datetime import datetime, timedelta
import time


def weekend_planner(place):
    if place=='':
        return tourist_places.get("Maharashtra")
    return tourist_places.get(place)




tourist_places = {
    'Rajasthan': ['Ranthambore National Park', 'Amber Palace', 'Hawa Mahal', 'City Palace, Jaipur', 'Umaid Bhawan Palace, Jodhpur', 'Jantar Mantar, Jaipur', 'Mehrangarh Fort Museum and Trust, Jodhpur', 'Jal Mahal, Jaipur', 'Jaisalmer Fort', 'Sariska Tiger Reserve', 'Chittorgarh Fort', 'Jag Mandir, Udaipur'],
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
        "Gateway of India", "Chhatrapati Shivaji Maharaj Terminus", "Shree Siddhivinayak Ganpati Temple", "Colaba Causeway", "Crawford Market",
        "Trimbakeshwar Jyotirling Mandir",
        "Bhaja Caves", "Ajanta Caves", "Elephanta Caves", "Kanheri Caves",
        "Tadoba-Andhari National Park", "Sanjay Gandhi National Park",
        "Shaniwar Wada", "Lohagad Fort", "Sinhagad Fort",
        "Lonar Lake", "Aga Khan Palace"
    ]
}

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['myblogdb']

users_collection = db['User']
notifications_collection = db['notifications']


# Function to add a notification to the database
def add_notification(message, username, place):
    notification = {
        'username':username,
        'message': message,
        'place':place,
        'created_at': time.time()
    }
    notifications_collection.insert_one(notification)


def get_users():
    data = users_collection.find({})
    return [d for d in data]



def main():
    # Check if today is Saturday
    today = datetime.now().date()
    if today.weekday() == 5:  # Saturday is represented by 5 in Python's weekday()
        for user in get_users():
            # Add your notification data here
            notification_message = "Hello! New Weekly Travel Recommendation"
            
            location = user['location']
            if location.split(','):
                region = location.split(',')[1].strip()
                if region != '':
                    location = region

            place = weekend_planner(tourist_places.get(location, ''))

            # Add the notification to the database
            add_notification(notification_message, user['username'], place)
            print("Notification added successfully.")


    # Close the MongoDB connection
    client.close()


if __name__ == '__main__':
    # main()
    add_notification("New Notification", "Kunal", "Karnataka")