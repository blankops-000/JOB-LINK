from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from app import db
from app.models.review import Review
from app.models.booking import Booking, BookingStatus
from app.models.provider_profile import ProviderProfile
from app.models.user import User
from app.utils.auth import admin_required, client_required

# Create blueprint - make sure this line exists
reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('', methods=['POST'])
@jwt_required()
@client_required
def create_review():
    """Create a new review for a completed booking"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}

        # Validate required fields
        required_fields = ['booking_id', 'rating', 'comment']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required': required_fields
            }), 400

        # Validate rating type and range
        try:
            rating = int(data['rating'])
        except (TypeError, ValueError):
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400

        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        # Find the booking that belongs to current client and is completed
        booking = Booking.query.filter_by(
            id=data['booking_id'],
            client_id=current_user_id,
            status=BookingStatus.COMPLETED
        ).first()

        if not booking:
            return jsonify({'error': 'Booking not found, not completed, or access denied'}), 404

        # Check if review already exists
        existing_review = Review.query.filter_by(booking_id=booking.id).first()
        if existing_review:
            return jsonify({'error': 'Review for this booking already exists'}), 400

        # Create the review
        review = Review(
            booking_id=booking.id,
            provider_id=getattr(booking, 'provider_id', None),
            client_id=current_user_id,
            rating=rating,
            comment=data['comment']
        )

        db.session.add(review)
        db.session.commit()

        # Recalculate provider aggregates (average rating and count) if provider exists
        provider_id = getattr(booking, 'provider_id', None)
        if provider_id is not None:
            agg = db.session.query(
                func.avg(Review.rating).label('avg_rating'),
                func.count(Review.id).label('count')
            ).filter(Review.provider_id == provider_id).first()

            avg_rating = float(agg.avg_rating) if agg and agg.avg_rating is not None else None
            count = int(agg.count) if agg and agg.count is not None else 0

            provider_profile = ProviderProfile.query.filter_by(provider_id=provider_id).first()
            if provider_profile:
                provider_profile.average_rating = avg_rating
                # If your ProviderProfile uses a different field name for count, adjust accordingly
                provider_profile.review_count = count
                db.session.commit()

        # Prepare response data (avoid exposing internal fields if necessary)
        review_data = {
            'id': review.id,
            'booking_id': review.booking_id,
            'provider_id': review.provider_id,
            'client_id': review.client_id,
            'rating': review.rating,
            'comment': review.comment
        }

        return jsonify({'message': 'Review created', 'review': review_data}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@reviews_bp.route('/provider/<int:provider_id>', methods=['GET'])
def get_provider_reviews(provider_id):
    """Get all reviews for a specific provider"""
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Check if provider exists
        provider = ProviderProfile.query.filter_by(user_id=provider_id).first()
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        
        # Get reviews with pagination
        reviews = Review.query.filter_by(provider_id=provider_id).order_by(
            desc(Review.created_at)
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Get review details with client information
        review_list = []
        for review in reviews.items:
            review_data = {
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'client': {
                    'id': review.client.id,
                    'first_name': review.client.first_name,
                    'last_name': review.client.last_name
                } if review.client else None
            }
            review_list.append(review_data)
        
        # Calculate rating summary
        rating_summary = db.session.query(
            func.avg(Review.rating).label('average'),
            func.count(Review.id).label('total'),
            func.sum(func.case((Review.rating == 5, 1), else_=0)).label('five_star'),
            func.sum(func.case((Review.rating == 4, 1), else_=0)).label('four_star'),
            func.sum(func.case((Review.rating == 3, 1), else_=0)).label('three_star'),
            func.sum(func.case((Review.rating == 2, 1), else_=0)).label('two_star'),
            func.sum(func.case((Review.rating == 1, 1), else_=0)).label('one_star')
        ).filter(Review.provider_id == provider_id).first()
        
        return jsonify({
            'reviews': review_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': reviews.total,
                'pages': reviews.pages
            },
            'rating_summary': {
                'average': float(rating_summary.average) if rating_summary.average else 0,
                'total': int(rating_summary.total) if rating_summary.total else 0,
                'breakdown': {
                    '5': int(rating_summary.five_star) if rating_summary.five_star else 0,
                    '4': int(rating_summary.four_star) if rating_summary.four_star else 0,
                    '3': int(rating_summary.three_star) if rating_summary.three_star else 0,
                    '2': int(rating_summary.two_star) if rating_summary.two_star else 0,
                    '1': int(rating_summary.one_star) if rating_summary.one_star else 0
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch reviews', 'details': str(e)}), 500

@reviews_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_reviews(user_id):
    """Get reviews written by a specific user (clients only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Authorization: users can only see their own reviews, admins can see all
        if current_user.role.value != 'admin' and current_user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get reviews with pagination
        reviews = Review.query.filter_by(client_id=user_id).order_by(
            desc(Review.created_at)
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Get review details with provider information
        review_list = []
        for review in reviews.items:
            review_data = {
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'provider': {
                    'id': review.provider.id,
                    'first_name': review.provider.first_name,
                    'last_name': review.provider.last_name
                } if review.provider else None,
                'booking_id': review.booking_id
            }
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