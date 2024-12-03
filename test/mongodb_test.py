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
posts = []
db =  client[('Restaurants')]
Restaurants_collection = db['Restaurant_Reviews']
results = Restaurants_collection.find({}, {"Name": 1, "Address":1, "Food":1, "_id": 0}) 
for document in results:
    posts.append(document)

suggested_restaurants = random.sample(posts, 10)
print(suggested_restaurants)