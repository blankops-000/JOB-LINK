from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User, RoleEnum
from app.utils.auth import admin_required
from app.utils.cloudinary_service import upload_image, delete_image
from sqlalchemy.exc import IntegrityError

users_bp = Blueprint('users', __name__)


# ---------- CREATE USER (Register)------------
@users_bp.route('/register', methods=['POST'])
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
@users_bp.route('/login', methods=['POST'])
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
@users_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtering
        role = request.args.get('role')
        search = request.args.get('search', '')
        
        query = User.query
        
        if role:
            query = query.filter_by(role=RoleEnum(role))
        
        if search:
            query = query.filter(
                (User.first_name.ilike(f'%{search}%')) |
                (User.last_name.ilike(f'%{search}%')) |
                (User.email.ilike(f'%{search}%'))
            )
        
        users = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'users': [u.to_dict() for u in users.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages
            }
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'details': str(e)}), 500


# ---------- GET CURRENT USER PROFILE ----------
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_current_user_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch profile', 'details': str(e)}), 500

# ---------- GET SINGLE USER ----------
@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Users can only view their own profile, admins can view any
        if current_user.role.value != 'admin' and current_user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found.'}), 404
        return jsonify({'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user', 'details': str(e)}), 500


#-------- UPDATE USER ---------
@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Users can only update their own profile, admins can update any
        if current_user.role.value != 'admin' and current_user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found.'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        
        # Only admins can change roles
        role = data.get('role')
        if role and current_user.role.value == 'admin':
            if role in [r.value for r in RoleEnum]:
                user.role = RoleEnum(role)

        db.session.commit()
        return jsonify({'message': 'User updated successfully.', 'user': user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user', 'details': str(e)}), 500


# ---------- DELETE USER------------
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found.'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500

# ---------- UPLOAD PROFILE IMAGE ----------
@users_bp.route('/profile/image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'error': 'Invalid file type. Use PNG, JPG, JPEG, or GIF'}), 400
        
        # Delete old image if exists
        if user.profile_image_public_id:
            delete_image(user.profile_image_public_id)
        
        # Upload new image
        public_id = f"users/{current_user_id}"
        result = upload_image(file, folder="joblink/users", public_id=public_id)
        
        if not result['success']:
            return jsonify({'error': 'Failed to upload image', 'details': result['error']}), 500
        
        # Update user profile
        user.profile_image_url = result['url']
        user.profile_image_public_id = result['public_id']
        db.session.commit()
        
        return jsonify({
            'message': 'Profile image uploaded successfully',
            'image_url': result['url']
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upload profile image', 'details': str(e)}), 500
