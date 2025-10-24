from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.booking import Booking

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bookings_bp.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([b.to_dict() for b in bookings]), 200

@bookings_bp.route('/<uuid:id>', methods=['GET'])
@jwt_required()
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify(booking.to_dict()), 200

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.get_json()
    booking = Booking(**data)
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201

@bookings_bp.route('/<uuid:id>', methods=['PATCH'])
@jwt_required()
def update_booking(id):
    booking = Booking.query.get_or_404(id)
    data = request.get_json()
    for field, value in data.items():
        setattr(booking, field, value)
    db.session.commit()
    return jsonify(booking.to_dict()), 200

@bookings_bp.route('/<uuid:id>', methods=['DELETE'])
@jwt_required()
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200
