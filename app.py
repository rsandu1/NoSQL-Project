from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import datetime
import random

# test comment

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB Configuration
client = MongoClient("mongodb+srv://varteagagonzalez:A4kdFOLEN8smbr0D@cluster0.9lkow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['Restaurants']
users_collection = db['users']
restaurants_collection = db['Restaurant_Reviews']
accounts_collection = db['accounts']

@app.route('/')
def index():
    first_row = restaurants_collection.find_one()
    return render_template('index.html', title="Home", first_row=first_row)


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Check if username already exists
        if accounts_collection.find_one({'username': username}):
            flash("Username already exists. Please choose another.")
            return redirect(url_for('register'))
        
        # Create a new account in the 'accounts' collection
        accounts_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'created_at': datetime.datetime.utcnow(),
            'last_login': None
        })
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register")


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the account by username
        account = accounts_collection.find_one({'username': username})
        if account and check_password_hash(account['password'], password):
            # Update last login time
            accounts_collection.update_one(
                {'_id': account['_id']},
                {'$set': {'last_login': datetime.datetime.utcnow()}}
            )
            session['username'] = username
            flash("Logged in successfully!")
            return redirect(url_for('dashboard'))
        
        flash("Invalid username or password.")
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    posts = []
    results = restaurants_collection.find({}, {"Name": 1, "Rating":1, "Rating Count":1, "Address":1, "Food":1, "image":1, "_id": 0}) 
    for document in results:
        posts.append(document)
    suggested_restaurants = random.sample(posts, 18)
    for item in posts:
        if "Rating Count" in item and isinstance(item["Rating Count"], float):
            item["Rating Count"] = int(item["Rating Count"])
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], title="Dashboard", posts=suggested_restaurants)
    return render_template('dashboard.html', title="Dashboard", posts=suggested_restaurants)

@app.route('/search', methods=['POST'])
def search():
    '''query = request.form['query']
    results = restaurants_collection.find({"name": {"$regex": query, "$options": "i"}})
    # return render_template('search.html', title="Search Results", results=results)
    return redirect(url_for('search'))
    return render_template('search.html', title="Search Results", results=results)'''
    if 'username' not in session:
        flash("Please log in to access this feature.")
        # return redirect(url_for('login'))
        return render_template('search.html', title="Search Page", results=[])
    
    results = []
    query = None

    if request.method == 'POST':
        query = request.form.get('query', '')

        if query:
            # Perform a case-insensitive search in the MongoDB collection
            results = restaurants_collection.find({"Name": {"$regex": query, "$options": "i"}})

        # results = restaurants_collection.find({"name": {"$regex": query, "$options": "i"}})
        '''for document in results :
            posts.append(document)
        for item in posts:
        if "Rating Count" in item and isinstance(item["Rating Count"], float):
            item["Rating Count"] = int(item["Rating Count"])'''
        # return render_template('search.html', title="Search Results", results=results)
    return render_template('search.html', title="Search Page", results=[])

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if 'username' not in session:
        flash("Please log in to access this feature.")
        return redirect(url_for('login'))
        #return render_template('insert.html', title="Insert Record")
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        rating = request.form['rating']
        price = request.form['price']
        url = request.form['url']

        # Check if Restaurant already exists
        if restaurants_collection.find_one({"Name": name}):
            flash("Restaurant already exists. Please choose another.")
            return redirect(url_for('insert'))
        
        # Create a new restaurant in the 'restaurants' collection
        restaurants_collection.insert_one({
            "URL": url,
            "Name": name,
            "Rating": float(rating),
            "Rating Count": 1,
            "Detailed Ratings": "",
            "Price Category": price,
            "Address": address
        })
        
        flash("Record inserted successfully!")
        return redirect(url_for('dashboard'))
    return render_template('insert.html', title="Insert Record")

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'username' not in session:
        flash("Please log in to access this feature.")
        return redirect(url_for('login'))
        #return render_template('delete.html', title="Delete Record")
    
    if request.method == 'POST':
        name = request.form['name']

        restaurant = restaurants_collection.find_one({"Name": name})
        if restaurant :
            try:
                restaurants_collection.delete_one({"Name": name})
                flash("Record deleted successfully!")
            except Exception as e:
                # flash("Invalid Restaurant Name.")
                flash("An error occurred while trying to delete the record.")
                print(f"Error: {e}")
        else :
            flash(f"Restaurant '{name}' does not exist.")
            return redirect(url_for('delete'))
        return redirect(url_for('dashboard'))
    return render_template('delete.html', title="Delete Record")

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'username' not in session:
        flash("Please log in to access this feature.")
        return redirect(url_for('login'))
        #return render_template('update.html', title="Update Record")
    
    if request.method == 'POST':
        name = request.form['name']
        user_rating = float(request.form['rating'])

        # find restaurant by name
        restaurant = restaurants_collection.find_one({"Name": name})
        if not restaurant:
            flash("Restaurant not found.")
            return redirect(url_for('update'))

        '''new_data = {
            # "address": request.form['address'],
            "rating": float(request.form['rating'])
        }'''
        try:
            current_rating = restaurant.get("Rating", 0.0)
            current_count = restaurant.get("Rating Count", 0)
            total_score = current_rating * current_count
            # print(total_score)
            total_score = int(round(total_score))
            new_total_score = total_score + user_rating
            new_count = current_count + 1
            new_average_rating = new_total_score / new_count

            # Update the database
            restaurants_collection.update_one(
                {"_id": restaurant["_id"]},
                {
                    "$set": {"Rating": round(new_average_rating, 1)},
                    "$inc": {"Rating Count": 1}
                }
            )
            # restaurants_collection.update_one({'_id': ObjectId(record_id)}, {'$set': new_data})
            flash("Record updated successfully!")
        except Exception as e:
            flash("Invalid record ID.")
        return redirect(url_for('dashboard'))
    return render_template('update.html', title="Update Record")

if __name__ == '__main__':
    app.run(debug=True)
