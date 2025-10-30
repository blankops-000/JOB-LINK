from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from app import db
from app.models.reviews import Review
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