from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['RestaurantReviews']
users_collection = db['users']
reviews_collection = db['reviews']

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    if users_collection.find_one({'username': data['username']}):
        return jsonify({'message': 'User already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    users_collection.insert_one({'username': data['username'], 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({'username': data['username']})
    
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        access_token = create_access_token(identity=user['username'])
        return jsonify({'token': access_token}), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401

# Add a new restaurant review
@app.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    data = request.get_json()
    required_fields = ['URL', 'Name', 'Rating', 'Rating Count', 'Detailed Ratings',
                       'Price Category', 'Address', 'Lat', 'Log', 'Zip Code']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    review = {field: data[field] for field in required_fields}
    reviews_collection.insert_one(review)
    return jsonify({'message': 'Review added successfully'}), 201

# Get all reviews or search by name
@app.route('/reviews', methods=['GET'])
@jwt_required()
def get_reviews():
    name_query = request.args.get('name')
    query = {'Name': {'$regex': name_query, '$options': 'i'}} if name_query else {}
    reviews = list(reviews_collection.find(query, {'_id': 0}))
    return jsonify(reviews), 200

# Update a review
@app.route('/reviews/<string:name>', methods=['PUT'])
@jwt_required()
def update_review(name):
    data = request.get_json()
    updated_fields = {key: data[key] for key in data if key in ['Rating', 'Detailed Ratings', 'Price Category']}
    result = reviews_collection.update_one({'Name': name}, {'$set': updated_fields})
    
    if result.matched_count:
        return jsonify({'message': 'Review updated successfully'}), 200
    return jsonify({'message': 'Review not found'}), 404

# Delete a review
@app.route('/reviews/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_review(name):
    result = reviews_collection.delete_one({'Name': name})
    if result.deleted_count:
        return jsonify({'message': 'Review deleted successfully'}), 200
    return jsonify({'message': 'Review not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
