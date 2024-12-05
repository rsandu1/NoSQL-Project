from pymongo import MongoClient
import random

try:
    # Replace with your actual connection URI
    client = MongoClient("mongodb+srv://varteagagonzalez:A4kdFOLEN8smbr0D@cluster0.9lkow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    client.admin.command('ping')
    print("Connection to MongoDB successful!")
except Exception as e:
    print("Error:", e)

# first_row = Restaurant_Reviews.find_one()
# print(first_row)



posts = {
    "American": ["American1.jpg", "American2.jpg", "American3.jpeg", "American4.jpg", "American5.jpeg"],
    "Italian": ["Italian1.jpeg", "Italian2.jpeg", "Italian3.jpg", "Italian4.jpeg", "Italian5.jpeg"],
    "Spanish": ["Spanish1.jpeg", "Spanish2.jpg", "Spanish3.jpg"],
    "Indian": ["Indian1.jpg", "Indian2.jpg", "Indian3.jpg"],
    "Latin": ["Latin1.jpg", "Latin2.jpg", "Latin3.jpg", "Latin4.jpeg", "Latin5.jpeg"],
    "Mexican": ["Mexican1.jpeg", "Mexican2.jpeg", "Mexican3.jpg"],
    "Caribbean": ["Caribbean1.jpg", "Caribbean2.jpg", "Caribbean3.jpg"],
    "Mediterranean": ["M1.jpg", "M2.jpg", "M3.jpeg"],
    "Eastern European": ["EE1.jpeg", "EE2.jpg", "EE3.jpg"],
    "Korean": ["K1.jpg", "K2.jpg"],
    "Chinese": ["CH1.jpg", "CH2.jpg", "CH3.jpg"],
    "Japanese": ["J1.jpg", "J2.jpeg", "J3.jpg"],
    "Middle Eastern": ["ME1.jpg", "ME2.jpg", "ME3.jpg"],
    "South Asian": ["SA1.jpg", "SA2.jpg", "SA3.jpg"],
    "French": ["F1.png", "F2.jpg", "F3.jpg"]
}

# images = {American:[]}
# db =  client[('Restaurants')]
# Restaurants_collection = db['Restaurant_Reviews']
# results = Restaurants_collection.find({}, {"Name": 1, "Rating Count":1, "Food":1, "_id": 0}) 
# for document in results:
#     posts.append(document)
# suggested_restaurants = random.sample(posts, 10)
# print(suggested_restaurants)


# Retrieve all restaurant names
db =  client[('Restaurants')]
Restaurants_collection = db['Restaurant_Reviews']
restaurant_names = Restaurants_collection.find({}, {"Name": 1, "_id": 0})
cuisine_names= Restaurants_collection.find({}, {"Food": 1, "_id": 0})

# Extract the names into a Python list
names_list = [restaurant["Name"] for restaurant in restaurant_names if "Name" in restaurant]
cuisine_list = [restaurant["Food"] for restaurant in cuisine_names if "Food" in restaurant]

for restaurant, cuisine in zip(names_list, cuisine_list):
    image = random.choice(posts[cuisine])    
    result = Restaurants_collection.update_one(
        {"name": restaurant},  # Find the document by restaurant name
        {"$set": {"image": image}}  # Add or update the "image" field
    )
    if result.matched_count == 0:
        print(f"No document found for restaurant: {restaurant}")
    elif result.modified_count == 1:
        print(f"Updated document for restaurant: {restaurant}")
