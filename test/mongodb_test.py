from pymongo import MongoClient

try:
    # Replace with your actual connection URI
    client = MongoClient("mongodb+srv://varteagagonzalez:A4kdFOLEN8smbr0D@cluster0.9lkow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    client.admin.command('ping')
    print("Connection to MongoDB successful!")
except Exception as e:
    print("Error:", e)

# first_row = Restaurant_Reviews.find_one()
# print(first_row)

db =  client[('Restaurants')]
Restaurants_collection = db['Restaurant_Reviews']

first_row = Restaurants_collection.find_one()
print(first_row)