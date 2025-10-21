from flask import Blueprint, jsonify

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
def get_services():
    return jsonify({'message': 'Services endpoint'}), 200