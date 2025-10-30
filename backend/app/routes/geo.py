from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.geo_service import calculate_distance, get_coordinates_from_address

geo_bp = Blueprint('geo', __name__)

@geo_bp.route('/geocode', methods=['POST'])
@jwt_required()
def geocode_address():
    """Convert address to coordinates"""
    try:
        data = request.get_json()
        address = data.get('address')
        
        if not address:
            return jsonify({'error': 'address is required'}), 400
        
        coords = get_coordinates_from_address(address)
        
        if coords:
            return jsonify({
                'message': 'Geocoding successful',
                'address': address,
                'coordinates': coords
            }), 200
        else:
            return jsonify({'error': 'Could not geocode address'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@geo_bp.route('/distance', methods=['POST'])
@jwt_required()
def calculate_distance_endpoint():
    """Calculate distance between two points"""
    try:
        data = request.get_json()
        
        required_fields = ['lat1', 'lon1', 'lat2', 'lon2']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'lat1, lon1, lat2, lon2 are required'}), 400
        
        distance = calculate_distance(
            data['lat1'], data['lon1'],
            data['lat2'], data['lon2']
        )
        
        return jsonify({
            'message': 'Distance calculated successfully',
            'distance_km': round(distance, 2) if distance else None,
            'coordinates': {
                'point1': {'lat': data['lat1'], 'lon': data['lon1']},
                'point2': {'lat': data['lat2'], 'lon': data['lon2']}
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500