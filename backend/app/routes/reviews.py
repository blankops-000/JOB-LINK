# Import Flask components for creating routes and handling HTTP requests
from flask import Blueprint, request, jsonify
# Import JWT components for authentication and authorization
from flask_jwt_extended import jwt_required, get_jwt_identity
# Import SQLAlchemy for database operations and aggregate functions
from sqlalchemy import func, desc
# Import database instance and models
from app import db
from backend.app.models.reviews import Review
from app.models.booking import Booking, BookingStatus
from app.models.provider_profile import ProviderProfile
from app.models.user import User
from app.models.service_category import ServiceCategory
from app.utils.auth import admin_required, client_required

# Create a Blueprint to group all review-related routes
reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('', methods=['POST'])
@jwt_required()
@client_required
def create_review():
    """
    Create a new review for a completed booking
    Only clients can create reviews, and only for their completed bookings
    """
    try:
        # Get the current user's ID from the JWT token
        current_user_id = get_jwt_identity()
        # Parse JSON data from the request body
        data = request.get_json()
        
        # Validate that required fields are provided
        required_fields = ['booking_id', 'rating', 'comment']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required': required_fields
            }), 400  # HTTP 400 Bad Request
        
        # Validate rating is between 1 and 5
        if data['rating'] < 1 or data['rating'] > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Find the booking and verify it belongs to the current user
        booking = Booking.query.filter_by(
            id=data['booking_id'],
            client_id=current_user_id,
            status=BookingStatus.COMPLETED  # Only allow reviews for completed bookings
        ).first()
        
        # Check if booking was found and is eligible for review
        if not booking:
            return jsonify({'error': 'Booking not found, not completed, or access denied'}), 404
        
        # Check if review already exists for this booking
        existing_review = Review.query.filter_by(booking_id=data['booking_id']).first()
        if existing_review:
            return jsonify({'error': 'Review already exists for this booking'}), 400
        
        # Create new review object
        review = Review(
            booking_id=data['booking_id'],
            client_id=current_user_id,
            provider_profile_id=booking.provider_profile_id,
            rating=data['rating'],
            comment=data['comment']
        )
        
        # Add review to database session and save
        db.session.add(review)
        db.session.commit()
        
        # Return success response with review details
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201  # HTTP 201 Created
        
    except Exception as e:
        # Rollback database changes in case of error
        db.session.rollback()
        return jsonify({'error': 'Failed to create review', 'details': str(e)}), 500

@reviews_bp.route('', methods=['GET'])
def get_reviews():
    """
    Get reviews with filtering and pagination
    Public endpoint - no authentication required
    """
    try:
        # Get pagination parameters from query string with defaults
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get filter parameters from query string
        provider_profile_id = request.args.get('provider_profile_id', type=int)
        min_rating = request.args.get('min_rating', type=int)
        max_rating = request.args.get('max_rating', type=int)
        
        # Start with base query for all reviews
        query = Review.query
        
        # Apply filters if provided
        if provider_profile_id:
            # Filter by specific provider
            query = query.filter_by(provider_profile_id=provider_profile_id)
        
        if min_rating:
            # Filter by minimum rating
            query = query.filter(Review.rating >= min_rating)
        
        if max_rating:
            # Filter by maximum rating
            query = query.filter(Review.rating <= max_rating)
        
        # Execute query with pagination, ordered by most recent first
        reviews = query.order_by(Review.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False  # Don't throw error if page doesn't exist
        )
        
        # Build response with review details and related information
        review_list = []
        for review in reviews.items:
            review_data = review.to_dict()
            # Add client information to review data
            review_data['client'] = review.author.to_dict() if review.author else None
            # Add provider profile information
            review_data['provider_profile'] = review.provider_profile.to_dict() if review.provider_profile else None
            # Add booking information
            review_data['booking'] = review.booking.to_dict() if review.booking else None
            review_list.append(review_data)
        
        # Return paginated response
        return jsonify({
            'reviews': review_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': reviews.total,
                'pages': reviews.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch reviews', 'details': str(e)}), 500

@reviews_bp.route('/provider/<int:provider_profile_id>', methods=['GET'])
def get_provider_reviews(provider_profile_id):
    """
    Get reviews for a specific provider with rating statistics
    Public endpoint - no authentication required
    """
    try:
        # Verify provider profile exists
        provider = ProviderProfile.query.get_or_404(provider_profile_id)
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query reviews for this specific provider
        reviews = Review.query.filter_by(
            provider_profile_id=provider_profile_id
        ).order_by(Review.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Calculate rating statistics using SQL aggregate functions
        stats = db.session.query(
            func.count(Review.id).label('total_reviews'),           # Count total reviews
            func.avg(Review.rating).label('average_rating'),        # Calculate average rating
            func.min(Review.rating).label('min_rating'),            # Find minimum rating
            func.max(Review.rating).label('max_rating')             # Find maximum rating
        ).filter_by(provider_profile_id=provider_profile_id).first()
        
        # Count ratings by star (1-5)
        rating_distribution = db.session.query(
            Review.rating,
            func.count(Review.id).label('count')
        ).filter_by(provider_profile_id=provider_profile_id).group_by(Review.rating).all()
        
        # Convert rating distribution to dictionary for easier frontend use
        distribution_dict = {str(i): 0 for i in range(1, 6)}  # Initialize with zeros
        for rating, count in rating_distribution:
            distribution_dict[str(rating)] = count
        
        # Build review list with client information
        review_list = []
        for review in reviews.items:
            review_data = review.to_dict()
            review_data['client'] = review.author.to_dict() if review.author else None
            review_list.append(review_data)
        
        # Return reviews with comprehensive statistics
        return jsonify({
            'provider': provider.to_dict(),
            'reviews': review_list,
            'statistics': {
                'total_reviews': stats.total_reviews or 0,
                'average_rating': round(float(stats.average_rating or 0), 2),  # Round to 2 decimal places
                'min_rating': stats.min_rating or 0,
                'max_rating': stats.max_rating or 0,
                'rating_distribution': distribution_dict
            },
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': reviews.total,
                'pages': reviews.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch provider reviews', 'details': str(e)}), 500

@reviews_bp.route('/analytics/top-providers', methods=['GET'])
@jwt_required()
@admin_required
def get_top_providers():
    """
    Get top-rated providers for admin analytics
    Admin-only endpoint for business intelligence
    """
    try:
        # Get limit parameter or default to 10
        limit = request.args.get('limit', 10, type=int)
        # Complex query to get providers with their review statistics
        top_providers = (
            db.session.query(
                ProviderProfile,                                  # Select provider profile
                User,                                            # Select user information
                func.avg(Review.rating).label('avg_rating'),     # Calculate average rating
                func.count(Review.id).label('review_count'),     # Count total reviews
                ServiceCategory                                   # Select service category
            )
            .join(Review, ProviderProfile.id == Review.provider_profile_id)  # Join with reviews
            .join(User, ProviderProfile.user_id == User.id)      # Join with users
            .join(ServiceCategory, ProviderProfile.service_category_id == ServiceCategory.id)  # Join with service categories
            .group_by(ProviderProfile.id)                        # Group by provider
            .having(func.count(Review.id) >= 1)                  # Only providers with at least 1 review
            .order_by(desc('avg_rating'))                        # Order by highest rating first
            .limit(limit)                                        # Limit results
            .all()
        )
        
        # Build response data
        providers_data = []
        for provider, user, avg_rating, review_count, category in top_providers:
            provider_data = provider.to_dict()
            provider_data['user'] = user.to_dict()
            provider_data['service_category'] = category.to_dict()
            provider_data['statistics'] = {
                'average_rating': round(float(avg_rating), 2),
                'total_reviews': review_count
            }
            providers_data.append(provider_data)
            providers_data.append(provider_data)
        
        return jsonify({
            'top_providers': providers_data,
            'limit': limit
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch top providers', 'details': str(e)}), 500

@reviews_bp.route('/analytics/platform-stats', methods=['GET'])
@jwt_required()
@admin_required
def get_platform_stats():
    """
    Get platform-wide statistics for admin dashboard
    Provides comprehensive business metrics
    """
    try:
        # Calculate total number of reviews across platform
        total_reviews = db.session.query(func.count(Review.id)).scalar() or 0
        
        # Calculate platform-wide average rating
        platform_avg_rating = db.session.query(func.avg(Review.rating)).scalar() or 0
        
        # Count total number of providers
        total_providers = db.session.query(func.count(ProviderProfile.id)).scalar() or 0
        
        # Count providers with at least one review
        providers_with_reviews = db.session.query(
            func.count(func.distinct(Review.provider_profile_id))
        ).scalar() or 0
        
        # Calculate rating distribution across entire platform
        platform_distribution = db.session.query(
            Review.rating,
            func.count(Review.id).label('count')
        ).group_by(Review.rating).all()
        
        # Convert to dictionary format
        platform_distribution_dict = {str(i): 0 for i in range(1, 6)}
        for rating, count in platform_distribution:
            platform_distribution_dict[str(rating)] = count
        
        # Get recent reviews for activity monitoring
        recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()
        recent_reviews_data = []
        for review in recent_reviews:
            review_data = review.to_dict()
            review_data['client'] = review.author.to_dict() if review.author else None
            review_data['provider_profile'] = review.provider_profile.to_dict() if review.provider_profile else None
            recent_reviews_data.append(review_data)
        
        # Return comprehensive platform statistics
        return jsonify({
            'platform_statistics': {
                'total_reviews': total_reviews,
                'average_rating': round(float(platform_avg_rating), 2),
                'total_providers': total_providers,
                'providers_with_reviews': providers_with_reviews,
                'review_coverage_percentage': round((providers_with_reviews / total_providers * 100) if total_providers > 0 else 0, 2),
                'rating_distribution': platform_distribution_dict
            },
            'recent_activity': {
                'recent_reviews': recent_reviews_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch platform statistics', 'details': str(e)}), 500

@reviews_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """
    Get a specific review by ID
    Public endpoint - no authentication required
    """
    try:
        # Find review or return 404 if not found
        review = Review.query.get_or_404(review_id)
        
        # Build comprehensive review data with related information
        review_data = review.to_dict()
        review_data['client'] = review.author.to_dict() if review.author else None
        review_data['provider_profile'] = review.provider_profile.to_dict() if review.provider_profile else None
        review_data['booking'] = review.booking.to_dict() if review.booking else None
        
        return jsonify({'review': review_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch review', 'details': str(e)}), 500

@reviews_bp.route('/my-reviews', methods=['GET'])
@jwt_required()
def get_my_reviews():
    """
    Get current user's reviews (both as client and provider)
    Clients see reviews they wrote, providers see reviews about them
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Different query based on user role
        if current_user.role.value == 'provider':
            # Providers see reviews about their services
            query = Review.query.join(ProviderProfile).filter(
                ProviderProfile.user_id == current_user_id
            )
        else:
            # Clients and admins see reviews they wrote
            query = Review.query.filter_by(client_id=current_user_id)
        
        # Execute query with pagination
        reviews = query.order_by(Review.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Build response data
        review_list = []
        for review in reviews.items:
            review_data = review.to_dict()
            review_data['client'] = review.author.to_dict() if review.author else None
            review_data['provider_profile'] = review.provider_profile.to_dict() if review.provider_profile else None
            review_data['booking'] = review.booking.to_dict() if review.booking else None
            review_list.append(review_data)
        
        return jsonify({
            'reviews': review_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': reviews.total,
                'pages': reviews.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user reviews', 'details': str(e)}), 500