from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Configuration
client = MongoClient("mongodb+srv://varteagagonzalez:A4kdFOLEN8smbr0D@cluster0.9lkow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['restaurant_db']

# Test connection
try:
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print("Error connecting to MongoDB:", e)

# Collections
users_collection = db['users']
restaurants_collection = db['restaurants']

# Helper Functions
def insert_restaurant(name, address, rating):
    """Insert a new restaurant record into the collection."""
    restaurants_collection.insert_one({
        "name": name,
        "address": address,
        "rating": rating
    })

def find_restaurant_by_name(name):
    """Find restaurants by name."""
    return restaurants_collection.find({"name": {"$regex": name, "$options": "i"}})

def update_restaurant(record_id, new_data):
    """Update a restaurant record by ID."""
    restaurants_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": new_data}
    )

def delete_restaurant(record_id):
    """Delete a restaurant record by ID."""
    restaurants_collection.delete_one({"_id": ObjectId(record_id)})
