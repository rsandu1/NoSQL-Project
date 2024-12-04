from pymongo import MongoClient
from bson.objectid import ObjectId

# @app.route('/update', methods=['GET', 'POST'])
client = MongoClient("mongodb+srv://varteagagonzalez:A4kdFOLEN8smbr0D@cluster0.9lkow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Restaurants']
users_collection = db['users']
restaurants_collection = db['Restaurant_Reviews']

# Test connection
try:
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print("Error connecting to MongoDB:", e)


name = input("Enter restaurant name: ")
user_rating = float(input("Enter rating: "))
print(user_rating)

# find restaurant by name
restaurant = restaurants_collection.find_one({"Name": name})
if not restaurant:
    print("Restaurant not found.")

try:
    current_rating = restaurant.get("Rating", 0.0)
    print(current_rating)
    current_count = restaurant.get("Rating Count", 0)
    print(current_count)
    total_score = current_rating * current_count
    print(total_score)
    total_score = int(round(total_score))
    new_total_score = total_score + user_rating
    new_count = current_count + 1
    new_average_rating = new_total_score / new_count
    print(new_average_rating)

    # Update the database
    restaurants_collection.update_one(
        {"_id": restaurant["_id"]},
        {
            "$set": {"Rating": round(new_average_rating, 1)},
            "$inc": {"Rating Count": 1}
        }
    )
    # restaurants_collection.update_one({'_id': ObjectId(record_id)}, {'$set': new_data})
    print("Record updated successfully!")
except Exception as e:
    print("Invalid record ID.")

#main
