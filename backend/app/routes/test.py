from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__)

@test_bp.route('/', methods=['GET'])
def test():
    return jsonify({
        'message': 'JobLink Backend is running!',
        'status': 'success',
        'endpoints': {
            'auth': '/api/auth/login, /api/auth/register',
            'services': '/api/services/',
            'bookings': '/api/bookings/'
        }
    }), 200