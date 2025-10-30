from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models.user import User, RoleEnum

# Make sure this line exists and the blueprint is named 'auth_bp'
auth_bp = Blueprint('auth', __name__)  # This creates the auth_bp variable

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    
    # Accept either 'name' or split 'first_name'/'last_name'
    name = data.get('name', '')
    first_name = data.get('first_name', name.split()[0] if name else '')
    last_name = data.get('last_name', ' '.join(name.split()[1:]) if len(name.split()) > 1 else '')
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not first_name or not email or not password:
        return jsonify({'msg': 'name, email and password are required'}), 400

    # check for existing user by email
    existing = User.query.filter(User.email == email).first()
    if existing:
        return jsonify({'msg': 'user with given email already exists'}), 409

    # hash password
    try:
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    except Exception:
        # fallback if generate_password_hash returns a str already
        pw_hash = bcrypt.generate_password_hash(password)

    user = User(first_name=first_name, last_name=last_name, email=email, password_hash=pw_hash)

    # attempt to set role if provided and valid
    if role:
        try:
            user.role = RoleEnum[role]
        except Exception:
            try:
                user.role = RoleEnum[role.upper()]
            except Exception:
                # ignore invalid role and let model default apply
                pass

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'msg': 'user registered',
        'user': {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role.value
        }
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

    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'msg': 'invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    user_info = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role.value if user.role else 'client'
    }

    return jsonify({'access_token': access_token, 'user': user_info}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({'msg': 'user not found'}), 404

    user_info = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role.value if user.role else 'client'
    }

    return jsonify({'user': user_info}), 200