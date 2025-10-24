from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models.user import User, RoleEnum

# Make sure this line exists and the blueprint is named 'auth_bp'
auth_bp = Blueprint('auth', __name__)  # This creates the auth_bp variable

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not username or not email or not password:
        return jsonify({'msg': 'username, email and password are required'}), 400

    # check for existing user by username or email
    existing = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing:
        return jsonify({'msg': 'user with given username or email already exists'}), 409

    # hash password
    try:
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    except Exception:
        # fallback if generate_password_hash returns a str already
        pw_hash = bcrypt.generate_password_hash(password)

    user = User(username=username, email=email, password=pw_hash)

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
        'user': {'id': user.id, 'username': user.username, 'email': user.email}
    }), 201

@auth_bp.route('/login', methods=['POST'])  
def login():
    data = request.get_json() or {}
    identifier = data.get('email') or data.get('username') or data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'msg': 'identifier and password required'}), 400

    user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
    if not user:
        return jsonify({'msg': 'invalid credentials'}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'msg': 'invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    user_info = {'id': user.id, 'username': user.username, 'email': user.email}
    if hasattr(user, 'role') and user.role is not None:
        try:
            user_info['role'] = user.role.name
        except Exception:
            user_info['role'] = str(user.role)

    return jsonify({'access_token': access_token, 'user': user_info}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'msg': 'user not found'}), 404

    user_info = {'id': user.id, 'username': user.username, 'email': user.email}
    if hasattr(user, 'role') and user.role is not None:
        try:
            user_info['role'] = user.role.name
        except Exception:
            user_info['role'] = str(user.role)

    return jsonify({'user': user_info}), 200