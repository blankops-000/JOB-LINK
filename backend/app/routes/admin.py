from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app import db
from app.models.user import User, RoleEnum
from app.models.provider_profile import ProviderProfile
from app.models.booking import Booking, BookingStatus
from app.models.review import Review  # Make sure this import is correct
from app.models.payment import Payment, PaymentStatus
from app.models.service_category import ServiceCategory
from app.utils.auth import admin_required

# Create blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_stats():
    """Get dashboard statistics for admin panel"""
    try:
        # User statistics
        user_stats = db.session.query(
            User.role,
            func.count(User.id).label('count')
        ).group_by(User.role).all()
        
        user_stats_dict = {role.value: count for role, count in user_stats}
        
        # Booking statistics
        booking_stats = db.session.query(
            Booking.status,
            func.count(Booking.id).label('count')
        ).group_by(Booking.status).all()
        
        booking_stats_dict = {status.value: count for status, count in booking_stats}
        
        return jsonify({
            'user_statistics': {
                'total_users': sum(user_stats_dict.values()),
                'clients': user_stats_dict.get('client', 0),
                'providers': user_stats_dict.get('provider', 0),
                'admins': user_stats_dict.get('admin', 0)
            },
            'booking_statistics': {
                'total_bookings': sum(booking_stats_dict.values()),
                'pending': booking_stats_dict.get('pending', 0),
                'confirmed': booking_stats_dict.get('confirmed', 0),
                'completed': booking_stats_dict.get('completed', 0),
                'cancelled': booking_stats_dict.get('cancelled', 0)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard statistics', 'details': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """Get all users with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = User.query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        user_list = []
        for user in users.items:
            user_data = user.to_dict()
            if user.role == RoleEnum.PROVIDER and user.provider_profile:
                user_data['provider_profile'] = user.provider_profile.to_dict()
            user_list.append(user_data)
        
        return jsonify({
            'users': user_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'details': str(e)}), 500

# Add more admin routes as needed...