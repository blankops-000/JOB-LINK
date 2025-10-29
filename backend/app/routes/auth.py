from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models.user import User, RoleEnum

# Make sure this line exists and the blueprint is named 'auth_bp'
auth_bp = Blueprint('auth', __name__)  # This creates the auth_bp variable

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    role = data.get('role')

    if not first_name or not last_name or not email or not password:
        return jsonify({'msg': 'first_name, last_name, email and password are required'}), 400

    # check for existing user by email
    existing = User.query.filter(User.email == email).first()
    if existing:
        return jsonify({'msg': 'user with given email already exists'}), 409

    user = User(first_name=first_name, last_name=last_name, email=email)
    user.set_password(password)

    # attempt to set role if provided and valid
    if role:
        try:
            user.role = RoleEnum[role.upper()]
        except (KeyError, AttributeError):
            # ignore invalid role and let model default apply
            pass

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'msg': 'user registered',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'email and password required'}), 400

    user = User.query.filter(User.email == email).first()
    if not user:
        return jsonify({'msg': 'invalid credentials'}), 401

    if not user.check_password(password):
        return jsonify({'msg': 'invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token, 'user': user.to_dict()}), 200

