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
    "American": ["static/images/American1.jpg", "static/images/American2.jpg", "static/images/American3.jpeg", "static/images/American4.jpg", "static/images/American5.jpeg"],
    "Italian": ["static/images/Italian1.jpeg", "static/images/Italian2.jpeg", "static/images/Italian3.jpg", "static/images/Italian4.jpeg", "static/images/Italian5.jpeg"],
    "Spanish": ["static/images/Spanish1.jpeg", "static/images/Spanish2.jpg", "static/images/Spanish3.jpg"],
    "Indian": ["static/images/Indian1.jpg", "static/images/Indian2.jpg", "static/images/Indian3.jpg"],
    "Latin": ["static/images/Latin1.jpg", "static/images/Latin2.jpg", "static/images/Latin3.jpg", "static/images/Latin4.jpeg", "static/images/Latin5.jpeg"],
    "Mexican": ["static/images/Mexican1.jpeg", "static/images/Mexican2.jpeg", "static/images/Mexican3.jpg"],
    "Caribbean": ["static/images/Caribbean1.jpg", "static/images/Caribbean2.jpg", "static/images/Caribbean3.jpg"],
    "Mediterranean": ["static/images/M1.jpg", "static/images/M2.jpg", "static/images/M3.jpeg"],
    "Eastern European": ["static/images/EE1.jpeg", "static/images/EE2.jpg", "static/images/EE3.jpg"],
    "Korean": ["static/images/K1.jpg", "static/images/K2.jpg"],
    "Chinese": ["static/images/CH1.jpg", "static/images/CH2.jpg", "static/images/CH3.jpg"],
    "Japanese": ["static/images/J1.jpg", "static/images/J2.jpeg", "static/images/J3.jpg"],
    "Middle Eastern": ["static/images/ME1.jpg", "static/images/ME2.jpg", "static/images/ME3.jpg"],
    "East Asian": ["static/images/SA1.jpg", "static/images/SA2.jpg", "static/images/SA3.jpg"],
    "South Asian": ["static/images/SA1.jpg", "static/images/SA2.jpg", "static/images/SA3.jpg"],
    "French": ["static/images/F1.png", "static/images/F2.jpg", "static/images/F3.jpg"],
    "English":["static/images/E1.jpg", "static/images/E2.jpg"]
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
# Query all documents to retrieve restaurants and cuisines
documents = Restaurants_collection.find({}, {"Name": 1, "Food": 1})  # Retrieve only the 'name' and 'cuisine' fields

# Update each document with a random image
i=0
for doc in documents:
    
    restaurant_name = doc.get("Name")  # Restaurant name
    cuisine_type = doc.get("Food")  # Cuisine type
    
    # Skip if the cuisine is not in the posts dictionary
    if cuisine_type not in posts:
        print(f"Skipped {restaurant_name}: Cuisine '{cuisine_type}' not found in posts. ", i)
        continue

    # Select a random image for the cuisine
    image = random.choice(posts[cuisine_type])
    
    # Update the document with the random image
    result = Restaurants_collection.update_one(
        {"_id": doc["_id"]},  # Match by document ID
        {"$set": {"image": image}}  # Add or update the "image" field
    )
    
    if result.modified_count == 1:
        print(f"Updated {restaurant_name} with image: {image} ",  i)
    else:
        print(f"No changes made to {restaurant_name}. ", i)
    
    i+=1
    

print("Script completed.")
