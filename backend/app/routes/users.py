from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User, RoleEnum
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/users')


# ---------- CREATE USER (Register)------------
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    role = data.get('role', 'client').lower()

    # Validate required fields
    if not all([email, password, first_name, last_name]):
        return jsonify({'message': 'All fields (email, password, first_name, last_name) are required.'}), 400

    # Validate role
    if role not in [r.value for r in RoleEnum]:
        return jsonify({'message': 'Invalid role value.'}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered.'}), 400

    try:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=RoleEnum(role)
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!', 'user': user.to_dict()}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error occurred.'}), 500


# -------------------- LOGIN USER --------------------
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password.'}), 401

    return jsonify({'message': 'Login successful.', 'user': user.to_dict()}), 200


#--------- GET ALL USERS --------
@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


# ---------- GET SINGLE USER ----------
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    return jsonify(user.to_dict()), 200


#-------- UPDATE USER ---------
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone = data.get('phone', user.phone)
    role = data.get('role')
    if role and role in [r.value for r in RoleEnum]:
        user.role = RoleEnum(role)

    db.session.commit()
    return jsonify({'message': 'User updated successfully.', 'user': user.to_dict()}), 200


# ---------- DELETE USER------------
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200
