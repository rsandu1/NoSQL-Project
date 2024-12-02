from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import datetime

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
    if 'username' in session:
        return render_template('search.html', title="Dashboard")
    flash("Please log in to access the dashboard.")
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = restaurants_collection.find({"name": {"$regex": query, "$options": "i"}})
    return render_template('search.html', title="Search Results", results=results)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if 'username' not in session:
        flash("Please log in to access this feature.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        rating = request.form['rating']
        restaurants_collection.insert_one({'name': name, 'address': address, 'rating': float(rating)})
        flash("Record inserted successfully!")
        return redirect(url_for('dashboard'))
    return render_template('insert.html', title="Insert Record")

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'username' not in session:
        flash("Please log in to access this feature.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        record_id = request.form['record_id']
        try:
            restaurants_collection.delete_one({'_id': ObjectId(record_id)})
            flash("Record deleted successfully!")
        except Exception as e:
            flash("Invalid record ID.")
        return redirect(url_for('dashboard'))
    return render_template('delete.html', title="Delete Record")

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'username' not in session:
        flash("Please log in to access this feature.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        record_id = request.form['record_id']
        new_data = {
            "name": request.form['name'],
            "address": request.form['address'],
            "rating": float(request.form['rating'])
        }
        try:
            restaurants_collection.update_one({'_id': ObjectId(record_id)}, {'$set': new_data})
            flash("Record updated successfully!")
        except Exception as e:
            flash("Invalid record ID.")
        return redirect(url_for('dashboard'))
    return render_template('update.html', title="Update Record")

if __name__ == '__main__':
    app.run(debug=True)
