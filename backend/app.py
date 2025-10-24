from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

# User routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if User.objects(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    user.save()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'user_id': str(user.id),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user_id': str(user.id),
            'username': user.username
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': str(user.id),
        'username': user.username,
        'email': user.email
    })

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.objects(id=user_id).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    user.save()
    
    return jsonify({'message': 'User updated successfully'})