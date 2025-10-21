from flask import Blueprint, jsonify

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['GET'])
def get_bookings():
    return jsonify({'message': 'Bookings endpoint'}), 200