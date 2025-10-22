from flask import Blueprint, jsonify, request
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.get_by_id(user_id)
    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.save()
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200