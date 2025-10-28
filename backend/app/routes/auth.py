from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models.user import User, RoleEnum

# Make sure this line exists and the blueprint is named 'auth_bp'
auth_bp = Blueprint('auth', __name__)  # This creates the auth_bp variable

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    role = data.get('role')

    if not email or not password or not first_name or not last_name:
        return jsonify({'msg': 'email, password, first_name and last_name are required'}), 400

    # check for existing user by email
    existing = User.query.filter(User.email == email).first()
    if existing:
        return jsonify({'msg': 'user with given email already exists'}), 409

    # Create user with hashed password
    user = User(email=email, first_name=first_name, last_name=last_name, phone=phone)
    user.set_password(password)

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
        'user': {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}
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

    access_token = create_access_token(identity=str(user.id))
    user_info = {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}
    if hasattr(user, 'role') and user.role is not None:
        try:
            user_info['role'] = user.role.value
        except Exception:
            user_info['role'] = str(user.role)

    return jsonify({'access_token': access_token, 'user': user_info}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({'msg': 'user not found'}), 404

    user_info = {'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}
    if hasattr(user, 'role') and user.role is not None:
        try:
            user_info['role'] = user.role.value
        except Exception:
            user_info['role'] = str(user.role)

    return jsonify({'user': user_info}), 200