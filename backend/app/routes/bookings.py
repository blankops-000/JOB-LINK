from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.errors import APIError, validation_error, not_found_error

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['GET'])
@jwt_required()
def get_bookings():
    """
    Get user bookings with pagination
    ---
    tags:
      - Bookings
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: status
        in: query
        type: string
        enum: [pending, confirmed, completed, cancelled]
    responses:
      200:
        description: List of bookings
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    status = request.args.get('status')
    
    # Mock response for now
    return jsonify({
        'bookings': [],
        'total': 0,
        'pages': 0,
        'current_page': page
    })

@bookings_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    """
    Get booking by ID
    ---
    tags:
      - Bookings
    parameters:
      - name: booking_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Booking details
      404:
        description: Booking not found
    """
    return jsonify({'message': 'Booking details'})

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    """
    Create new booking
    ---
    tags:
      - Bookings
    parameters:
      - in: body
        name: booking
        schema:
          type: object
          required:
            - service_id
            - date
          properties:
            service_id:
              type: integer
            date:
              type: string
              format: date-time
            notes:
              type: string
    responses:
      201:
        description: Booking created
    """
    data = request.get_json()
    
    if not data or not data.get('service_id'):
        raise validation_error("Service ID is required")
    
    if not data.get('date'):
        raise validation_error("Date is required")
    
    return jsonify({'message': 'Booking created successfully'}), 201

@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    """
    Update booking
    ---
    tags:
      - Bookings
    """
    data = request.get_json()
    
    if not data:
        raise validation_error("No data provided")
    
    return jsonify({'message': 'Booking updated successfully'})

@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    """
    Cancel booking
    ---
    tags:
      - Bookings
    """
    return jsonify({'message': 'Booking cancelled successfully'})