from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: user
        description: User registration data
        schema:
          type: object
          required:
            - email
            - password
            - first_name
            - last_name
          properties:
            email:
              type: string
            password:
              type: string
            first_name:
              type: string
            last_name:
              type: string
            phone:
              type: string
            role:
              type: string
              enum: [customer, provider, admin]
    responses:
      201:
        description: User created successfully
      400:
        description: Email already exists
    """
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone'),
        role=data.get('role', 'customer')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: credentials
        description: User login credentials
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401