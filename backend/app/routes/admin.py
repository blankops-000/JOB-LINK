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

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """Update user details (admin only)"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Check if email already exists
            existing = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing:
                return jsonify({'error': 'Email already exists'}), 409
            user.email = data['email']
        if 'phone' in data:
            user.phone = data['phone']
        if 'role' in data:
            try:
                user.role = RoleEnum[data['role'].upper()]
            except KeyError:
                return jsonify({'error': 'Invalid role'}), 400
        if 'is_verified' in data:
            user.is_verified = data['is_verified']
            
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user', 'details': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Prevent admin from deleting themselves
        current_user_id = get_jwt_identity()
        if int(current_user_id) == user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
            
        user_data = user.to_dict()
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User deleted successfully',
            'deleted_user': user_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500

@admin_bp.route('/providers', methods=['GET'])
@jwt_required()
@admin_required
def get_all_providers():
    """Get all providers with details (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        providers = ProviderProfile.query.order_by(ProviderProfile.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        provider_list = []
        for provider in providers.items:
            provider_data = provider.to_dict()
            provider_data['user'] = provider.user.to_dict() if provider.user else None
            provider_data['service_category'] = provider.service_category.to_dict() if provider.service_category else None
            
            # Add booking and review counts
            booking_count = Booking.query.filter_by(provider_id=provider.user_id).count()
            review_count = Review.query.filter_by(provider_id=provider.user_id).count()
            
            provider_data['booking_count'] = booking_count
            provider_data['review_count'] = review_count
            
            provider_list.append(provider_data)
        
        return jsonify({
            'providers': provider_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': providers.total,
                'pages': providers.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch providers', 'details': str(e)}), 500

@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
@admin_required
def get_all_bookings():
    """Get all bookings overview (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        query = Booking.query
        
        # Filter by status if provided
        if status:
            try:
                query = query.filter_by(status=BookingStatus(status))
            except ValueError:
                return jsonify({'error': 'Invalid status'}), 400
        
        bookings = query.order_by(Booking.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        booking_list = []
        for booking in bookings.items:
            booking_data = booking.to_dict()
            booking_data['client'] = booking.client.to_dict() if booking.client else None
            booking_data['provider_user'] = booking.provider.to_dict() if booking.provider else None
            booking_data['service_category'] = booking.service_category.to_dict() if booking.service_category else None
            booking_list.append(booking_data)
        
        return jsonify({
            'bookings': booking_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': bookings.total,
                'pages': bookings.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch bookings', 'details': str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_stats():
    """Get comprehensive admin statistics"""
    try:
        # Basic counts
        total_users = User.query.count()
        total_providers = ProviderProfile.query.count()
        total_bookings = Booking.query.count()
        total_reviews = Review.query.count()
        
        # Revenue calculation (sum of completed bookings)
        total_revenue = db.session.query(func.sum(Booking.total_amount)).filter(
            Booking.status == BookingStatus.COMPLETED
        ).scalar() or 0
        
        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        recent_users = User.query.filter(User.created_at >= thirty_days_ago).count()
        recent_bookings = Booking.query.filter(Booking.created_at >= thirty_days_ago).count()
        recent_reviews = Review.query.filter(Review.created_at >= thirty_days_ago).count()
        
        # Top service categories
        top_categories = db.session.query(
            ServiceCategory.name,
            func.count(Booking.id).label('booking_count')
        ).join(Booking).group_by(ServiceCategory.name).order_by(
            desc('booking_count')
        ).limit(5).all()
        
        return jsonify({
            'totals': {
                'users': total_users,
                'providers': total_providers,
                'bookings': total_bookings,
                'reviews': total_reviews,
                'revenue': float(total_revenue)
            },
            'recent_activity': {
                'new_users_30d': recent_users,
                'new_bookings_30d': recent_bookings,
                'new_reviews_30d': recent_reviews
            },
            'top_categories': [
                {'name': name, 'booking_count': count} 
                for name, count in top_categories
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch admin statistics', 'details': str(e)}), 500