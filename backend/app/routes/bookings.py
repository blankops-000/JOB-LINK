from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models.booking import Booking, BookingStatus
from app.models.provider_profile import ProviderProfile
from app.models.service_category import ServiceCategory
from app.models.user import User
from app.models.payment import Payment, PaymentStatus
from app.utils.auth import admin_required, provider_required, client_required

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('', methods=['POST'])
@jwt_required()
@client_required
def create_booking():
    """Create a new booking (clients only)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['provider_id', 'service_category_id', 'scheduled_date', 'duration_hours', 'address']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        # Check if provider exists and is available
        provider = ProviderProfile.query.filter_by(
            user_id=data['provider_id'],
            is_available=True
        ).first()
        
        if not provider:
            return jsonify({'error': 'Provider not found or not available'}), 404
        
        # Check if service category exists
        service_category = ServiceCategory.query.get(data['service_category_id'])
        if not service_category:
            return jsonify({'error': 'Service category not found'}), 404
        
        # Parse scheduled date
        try:
            scheduled_date = datetime.fromisoformat(data['scheduled_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
        
        # Check if date is in the future
        if scheduled_date <= datetime.utcnow():
            return jsonify({'error': 'Booking date must be in the future'}), 400
        
        # Calculate total amount
        total_amount = provider.hourly_rate * data['duration_hours']
        
        # Create booking
        booking = Booking(
            client_id=current_user_id,
            provider_id=data['provider_id'],
            provider_profile_id=provider.id,
            service_category_id=data['service_category_id'],
            scheduled_date=scheduled_date,
            duration_hours=data['duration_hours'],
            total_amount=total_amount,
            address=data['address'],
            special_requests=data.get('special_requests', '')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create booking', 'details': str(e)}), 500

@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get bookings with filtering (based on user role)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        # Base query depends on user role
        if current_user.role.value == 'admin':
            # Admin can see all bookings
            query = Booking.query
        elif current_user.role.value == 'provider':
            # Providers see their own bookings
            query = Booking.query.filter_by(provider_id=current_user_id)
        else:
            # Clients see their own bookings
            query = Booking.query.filter_by(client_id=current_user_id)
        
        # Filter by status if provided
        if status:
            query = query.filter_by(status=BookingStatus(status))
        
        # Execute query with pagination
        bookings = query.order_by(Booking.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Get booking details with related information
        booking_list = []
        for booking in bookings.items:
            booking_data = booking.to_dict()
            booking_data['client'] = booking.client.to_dict() if booking.client else None
            booking_data['provider_user'] = booking.provider.to_dict() if booking.provider else None
            booking_data['provider_profile'] = booking.provider_profile.to_dict() if booking.provider_profile else None
            booking_data['service_category'] = booking.service_category.to_dict() if booking.service_category else None
            booking_data['payment'] = booking.payment.to_dict() if booking.payment else None
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

@bookings_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """Get specific booking by ID (with authorization)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        booking = Booking.query.get_or_404(booking_id)
        
        # Authorization check
        if (current_user.role.value != 'admin' and 
            booking.client_id != current_user_id and 
            booking.provider_id != current_user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        booking_data = booking.to_dict()
        booking_data['client'] = booking.client.to_dict() if booking.client else None
        booking_data['provider_user'] = booking.provider.to_dict() if booking.provider else None
        booking_data['provider_profile'] = booking.provider_profile.to_dict() if booking.provider_profile else None
        booking_data['service_category'] = booking.service_category.to_dict() if booking.service_category else None
        booking_data['payment'] = booking.payment.to_dict() if booking.payment else None
        
        return jsonify({'booking': booking_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch booking', 'details': str(e)}), 500

@bookings_bp.route('/<int:booking_id>/status', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    """Update booking status (providers and clients have different permissions)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'status field is required'}), 400
        
        booking = Booking.query.get_or_404(booking_id)
        new_status = BookingStatus(data['status'])
        
        # Authorization and business logic checks
        if current_user.role.value == 'provider':
            # Providers can only update their own bookings
            if booking.provider_id != current_user_id:
                return jsonify({'error': 'Access denied'}), 403
            
            # Providers can: confirm, mark in-progress, complete
            allowed_statuses = [BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS, BookingStatus.COMPLETED]
            if new_status not in allowed_statuses:
                return jsonify({'error': 'Provider cannot set this status'}), 400
                
        elif current_user.role.value == 'client':
            # Clients can only update their own bookings
            if booking.client_id != current_user_id:
                return jsonify({'error': 'Access denied'}), 403
            
            # Clients can only cancel
            if new_status != BookingStatus.CANCELLED:
                return jsonify({'error': 'Clients can only cancel bookings'}), 400
                
        else:  # admin
            # Admin can set any status
            pass
        
        # Update status
        booking.status = new_status
        db.session.commit()
        
        return jsonify({
            'message': f'Booking status updated to {new_status.value}',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update booking status', 'details': str(e)}), 500

@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    """Update booking details (clients only, before confirmation)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        booking = Booking.query.filter_by(
            id=booking_id,
            client_id=current_user_id
        ).first_or_404()
        
        # Only allow updates for pending bookings
        if booking.status != BookingStatus.PENDING:
            return jsonify({'error': 'Can only update pending bookings'}), 400
        
        # Update allowed fields
        if 'scheduled_date' in data:
            try:
                scheduled_date = datetime.fromisoformat(data['scheduled_date'].replace('Z', '+00:00'))
                if scheduled_date <= datetime.utcnow():
                    return jsonify({'error': 'Booking date must be in the future'}), 400
                booking.scheduled_date = scheduled_date
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        if 'duration_hours' in data:
            booking.duration_hours = data['duration_hours']
            # Recalculate total amount
            booking.total_amount = booking.provider_profile.hourly_rate * data['duration_hours']
        
        if 'address' in data:
            booking.address = data['address']
        
        if 'special_requests' in data:
            booking.special_requests = data['special_requests']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking updated successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update booking', 'details': str(e)}), 500

@bookings_bp.route('/provider/availability', methods=['GET'])
@jwt_required()
@provider_required
def check_provider_availability():
    """Check if provider is available at a specific time"""
    try:
        current_user_id = get_jwt_identity()
        scheduled_date = request.args.get('scheduled_date')
        duration_hours = request.args.get('duration_hours', 1, type=int)
        
        if not scheduled_date:
            return jsonify({'error': 'scheduled_date parameter is required'}), 400
        
        try:
            check_date = datetime.fromisoformat(scheduled_date.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO format'}), 400
        
        # Check for overlapping bookings
        overlapping_booking = Booking.query.filter(
            Booking.provider_id == current_user_id,
            Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.IN_PROGRESS]),
            Booking.scheduled_date <= check_date,
            Booking.scheduled_date + db.func.make_interval(hours=Booking.duration_hours) >= check_date
        ).first()
        
        is_available = overlapping_booking is None
        
        return jsonify({
            'is_available': is_available,
            'requested_time': check_date.isoformat(),
            'duration_hours': duration_hours,
            'conflicting_booking': overlapping_booking.to_dict() if overlapping_booking else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to check availability', 'details': str(e)}), 500

@bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    """Cancel a booking (both client and provider)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        booking = Booking.query.get_or_404(booking_id)
        
        # Authorization check
        if (current_user.role.value != 'admin' and 
            booking.client_id != current_user_id and 
            booking.provider_id != current_user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        # Business logic checks
        if booking.status in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
            return jsonify({'error': f'Cannot cancel a {booking.status.value} booking'}), 400
        
        # Update status to cancelled
        booking.status = BookingStatus.CANCELLED
        db.session.commit()
        
        return jsonify({
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel booking', 'details': str(e)}), 500