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
posts = []
db =  client[('Restaurants')]
Restaurants_collection = db['Restaurant_Reviews']
results = Restaurants_collection.find({}, {"Name": 1, "Address":1, "Food":1, "_id": 0}) 
for document in results:
    posts.append(document)

print(type(posts))
i = 0 
while i < 2:
    print(posts[i])
    i+=1