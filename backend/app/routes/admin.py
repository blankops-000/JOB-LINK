# Import Flask components for creating routes and handling HTTP requests
from flask import Blueprint, request, jsonify
# Import JWT components for authentication and authorization
from flask_jwt_extended import jwt_required, get_jwt_identity
# Import SQLAlchemy for database operations and aggregate functions
from sqlalchemy import func, desc, and_
# Import datetime for time-based analytics
from datetime import datetime, timedelta
# Import database instance and all models
from app import db
from app.models.user import User, RoleEnum
from app.models.provider_profile import ProviderProfile
from app.models.booking import Booking, BookingStatus
from app.models.review import Review
from app.models.payment import Payment, PaymentStatus
from app.models.service_category import ServiceCategory
# Import admin-only authorization decorator
from app.utils.auth import admin_required

# Create a Blueprint to group all admin-related routes
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_stats():
    """
    Get comprehensive dashboard statistics for admin panel
    Provides overview of platform health and business metrics
    """
    try:
        # Calculate total users count grouped by role
        user_stats = db.session.query(
            User.role,                    # Select role column
            func.count(User.id).label('count')  # Count users per role
        ).group_by(User.role).all()       # Group by role
        
        # Convert to dictionary for easier access
        user_stats_dict = {role.value: count for role, count in user_stats}
        
        # Calculate total providers (both with and without profiles)
        total_providers = User.query.filter_by(role=RoleEnum.PROVIDER).count()
        providers_with_profiles = ProviderProfile.query.count()
        
        # Calculate booking statistics by status
        booking_stats = db.session.query(
            Booking.status,               # Select booking status
            func.count(Booking.id).label('count')  # Count bookings per status
        ).group_by(Booking.status).all()  # Group by status
        
        # Convert to dictionary
        booking_stats_dict = {status.value: count for status, count in booking_stats}
        
        # Calculate total revenue from completed payments
        total_revenue = db.session.query(
            func.sum(Payment.amount)      # Sum all payment amounts
        ).filter(Payment.status == PaymentStatus.COMPLETED).scalar() or 0
        
        # Calculate today's date for time-based analytics
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Calculate new users in last 7 days
        new_users_week = User.query.filter(
            User.created_at >= week_ago   # Users created in last 7 days
        ).count()
        
        # Calculate new bookings in last 7 days
        new_bookings_week = Booking.query.filter(
            Booking.created_at >= week_ago  # Bookings created in last 7 days
        ).count()
        
        # Calculate weekly revenue
        weekly_revenue = db.session.query(
            func.sum(Payment.amount)      # Sum payments from last week
        ).filter(
            and_(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.created_at >= week_ago
            )
        ).scalar() or 0
        
        # Return comprehensive dashboard statistics
        return jsonify({
            'user_statistics': {
                'total_users': sum(user_stats_dict.values()),  # Sum all user counts
                'clients': user_stats_dict.get('client', 0),
                'providers': user_stats_dict.get('provider', 0),
                'admins': user_stats_dict.get('admin', 0),
                'providers_with_profiles': providers_with_profiles,
                'providers_without_profiles': total_providers - providers_with_profiles,
                'new_users_this_week': new_users_week
            },
            'booking_statistics': {
                'total_bookings': sum(booking_stats_dict.values()),  # Sum all booking counts
                'pending': booking_stats_dict.get('pending', 0),
                'confirmed': booking_stats_dict.get('confirmed', 0),
                'in_progress': booking_stats_dict.get('in_progress', 0),
                'completed': booking_stats_dict.get('completed', 0),
                'cancelled': booking_stats_dict.get('cancelled', 0),
                'new_bookings_this_week': new_bookings_week
            },
            'financial_statistics': {
                'total_revenue': float(total_revenue),        # Convert decimal to float for JSON
                'weekly_revenue': float(weekly_revenue),
                'average_booking_value': float(total_revenue / booking_stats_dict.get('completed', 1)) if booking_stats_dict.get('completed', 0) > 0 else 0
            },
            'platform_health': {
                'completion_rate': (booking_stats_dict.get('completed', 0) / sum(booking_stats_dict.values()) * 100) if sum(booking_stats_dict.values()) > 0 else 0,
                'cancellation_rate': (booking_stats_dict.get('cancelled', 0) / sum(booking_stats_dict.values()) * 100) if sum(booking_stats_dict.values()) > 0 else 0
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch dashboard statistics', 'details': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """
    Get all users with pagination and filtering
    Admin-only endpoint for user management
    """
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        role_filter = request.args.get('role')
        search_query = request.args.get('search', '')
        
        # Start with base query for all users
        query = User.query
        
        # Apply role filter if provided
        if role_filter:
            query = query.filter_by(role=RoleEnum(role_filter))
        
        # Apply search filter if provided (search in name or email)
        if search_query:
            query = query.filter(
                db.or_(
                    User.first_name.ilike(f'%{search_query}%'),   # Search in first name
                    User.last_name.ilike(f'%{search_query}%'),    # Search in last name
                    User.email.ilike(f'%{search_query}%')         # Search in email
                )
            )
        
        # Execute query with pagination, ordered by most recent first
        users = query.order_by(User.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Build user list with additional information
        user_list = []
        for user in users.items:
            user_data = user.to_dict()
            # Add provider profile information if user is a provider
            if user.role == RoleEnum.PROVIDER and user.provider_profile:
                user_data['provider_profile'] = user.provider_profile.to_dict()
            user_list.append(user_data)
        
        # Return paginated user list
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

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    """
    Get detailed information about a specific user
    Includes comprehensive user data for admin review
    """
    try:
        # Find user or return 404 if not found
        user = User.query.get_or_404(user_id)
        
        # Build comprehensive user data
        user_data = user.to_dict()
        
        # Add provider-specific data if user is a provider
        if user.role == RoleEnum.PROVIDER:
            if user.provider_profile:
                user_data['provider_profile'] = user.provider_profile.to_dict()
                # Add service category information
                if user.provider_profile.service_category:
                    user_data['provider_profile']['service_category'] = user.provider_profile.service_category.to_dict()
            else:
                user_data['provider_profile'] = None
        
        # Add booking statistics for this user
        if user.role == RoleEnum.CLIENT:
            # Client booking stats
            user_data['booking_stats'] = {
                'total_bookings': Booking.query.filter_by(client_id=user_id).count(),
                'completed_bookings': Booking.query.filter_by(client_id=user_id, status=BookingStatus.COMPLETED).count(),
                'pending_bookings': Booking.query.filter_by(client_id=user_id, status=BookingStatus.PENDING).count()
            }
        elif user.role == RoleEnum.PROVIDER:
            # Provider booking stats
            user_data['booking_stats'] = {
                'total_bookings': Booking.query.filter_by(provider_id=user_id).count(),
                'completed_bookings': Booking.query.filter_by(provider_id=user_id, status=BookingStatus.COMPLETED).count(),
                'pending_bookings': Booking.query.filter_by(provider_id=user_id, status=BookingStatus.PENDING).count()
            }
        
        # Add review statistics
        if user.role == RoleEnum.CLIENT:
            user_data['review_stats'] = {
                'reviews_written': Review.query.filter_by(client_id=user_id).count()
            }
        elif user.role == RoleEnum.PROVIDER and user.provider_profile:
            provider_reviews = Review.query.filter_by(provider_profile_id=user.provider_profile.id)
            user_data['review_stats'] = {
                'reviews_received': provider_reviews.count(),
                'average_rating': db.session.query(func.avg(Review.rating)).filter_by(provider_profile_id=user.provider_profile.id).scalar() or 0
            }
        
        return jsonify({'user': user_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user', 'details': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_role(user_id):
    """
    Update user role (e.g., promote to admin, change to provider)
    Admin-only endpoint for user management
    """
    try:
        # Get the current admin's ID for audit purposes
        current_admin_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate that role is provided
        if 'role' not in data:
            return jsonify({'error': 'role field is required'}), 400
        
        # Find user to update
        user = User.query.get_or_404(user_id)
        
        # Prevent admin from modifying their own role
        if user_id == current_admin_id:
            return jsonify({'error': 'Cannot modify your own role'}), 400
        
        # Get the new role from request data
        new_role = RoleEnum(data['role'])
        
        # Store old role for logging/audit
        old_role = user.role
        
        # Update user role
        user.role = new_role
        
        # If changing from provider to another role, handle provider profile
        if old_role == RoleEnum.PROVIDER and new_role != RoleEnum.PROVIDER:
            # You might want to archive or delete the provider profile
            # For now, we'll just leave it but note the change
            pass
        
        # Save changes to database
        db.session.commit()
        
        # Return success response
        return jsonify({
            'message': f'User role updated from {old_role.value} to {new_role.value}',
            'user': user.to_dict()
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid role value'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user role', 'details': str(e)}), 500

@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
@admin_required
def get_all_bookings():
    """
    Get all bookings with comprehensive filtering options
    Admin-only endpoint for booking management
    """
    try:
        # Get pagination and filter parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        provider_id = request.args.get('provider_id', type=int)
        client_id = request.args.get('client_id', type=int)
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Start with base query
        query = Booking.query
        
        # Apply filters
        if status_filter:
            query = query.filter_by(status=BookingStatus(status_filter))
        
        if provider_id:
            query = query.filter_by(provider_id=provider_id)
        
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        # Date range filtering
        if date_from:
            try:
                from_date = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                query = query.filter(Booking.scheduled_date >= from_date)
            except ValueError:
                return jsonify({'error': 'Invalid date_from format'}), 400
        
        if date_to:
            try:
                to_date = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                query = query.filter(Booking.scheduled_date <= to_date)
            except ValueError:
                return jsonify({'error': 'Invalid date_to format'}), 400
        
        # Execute query with pagination
        bookings = query.order_by(Booking.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Build comprehensive booking data
        booking_list = []
        for booking in bookings.items:
            booking_data = booking.to_dict()
            booking_data['client'] = booking.client.to_dict() if booking.client else None
            booking_data['provider_user'] = booking.provider.to_dict() if booking.provider else None
            booking_data['provider_profile'] = booking.provider_profile.to_dict() if booking.provider_profile else None
            booking_data['service_category'] = booking.service_category.to_dict() if booking.service_category else None
            booking_data['payment'] = booking.payment.to_dict() if booking.payment else None
            booking_data['review'] = booking.review.to_dict() if booking.review else None
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

@admin_bp.route('/service-categories', methods=['POST'])
@jwt_required()
@admin_required
def create_service_category():
    """
    Create a new service category
    Admin-only endpoint for managing service types
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'name' not in data:
            return jsonify({'error': 'name field is required'}), 400
        
        # Check if category already exists
        existing_category = ServiceCategory.query.filter_by(name=data['name']).first()
        if existing_category:
            return jsonify({'error': 'Service category with this name already exists'}), 400
        
        # Create new service category
        category = ServiceCategory(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Service category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create service category', 'details': str(e)}), 500

@admin_bp.route('/service-categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_service_category(category_id):
    """
    Update a service category
    Admin-only endpoint for managing service types
    """
    try:
        data = request.get_json()
        
        # Find category to update
        category = ServiceCategory.query.get_or_404(category_id)
        
        # Update fields if provided
        if 'name' in data:
            # Check if new name already exists (excluding current category)
            existing = ServiceCategory.query.filter(
                ServiceCategory.name == data['name'],
                ServiceCategory.id != category_id
            ).first()
            if existing:
                return jsonify({'error': 'Service category with this name already exists'}), 400
            category.name = data['name']
        
        if 'description' in data:
            category.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Service category updated successfully',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update service category', 'details': str(e)}), 500

@admin_bp.route('/analytics/revenue', methods=['GET'])
@jwt_required()
@admin_required
def get_revenue_analytics():
    """
    Get revenue analytics for business intelligence
    Includes daily, weekly, and monthly revenue trends
    """
    try:
        # Get time period parameter (default to monthly)
        period = request.args.get('period', 'monthly')  # daily, weekly, monthly
        
        # Calculate date ranges based on period
        end_date = datetime.utcnow().date()
        if period == 'daily':
            start_date = end_date - timedelta(days=30)  # Last 30 days
            group_format = '%Y-%m-%d'  # Group by day
        elif period == 'weekly':
            start_date = end_date - timedelta(weeks=12)  # Last 12 weeks
            group_format = '%Y-%U'     # Group by week
        else:  # monthly
            start_date = end_date - timedelta(days=365)  # Last 12 months
            group_format = '%Y-%m'     # Group by month
        
        # Query revenue data grouped by time period
        revenue_data = db.session.query(
            func.strftime(group_format, Payment.created_at).label('period'),
            func.sum(Payment.amount).label('revenue'),
            func.count(Payment.id).label('transactions')
        ).filter(
            and_(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.created_at >= start_date
            )
        ).group_by('period').order_by('period').all()
        
        # Format data for frontend charts
        chart_data = {
            'labels': [row.period for row in revenue_data],
            'revenue': [float(row.revenue) for row in revenue_data],
            'transactions': [row.transactions for row in revenue_data]
        }
        
        return jsonify({
            'period': period,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'chart_data': chart_data,
            'total_revenue': float(sum(row.revenue for row in revenue_data)),
            'total_transactions': sum(row.transactions for row in revenue_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch revenue analytics', 'details': str(e)}), 500