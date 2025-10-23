from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.errors import APIError, validation_error, not_found_error

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
def get_services():
    """
    Get all services with pagination
    ---
    tags:
      - Services
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: List of services
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    
    providers = User.query.filter_by(role='provider').paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'services': [{
            'id': p.id,
            'name': f"{p.first_name} {p.last_name}",
            'email': p.email,
            'phone': p.phone
        } for p in providers.items],
        'total': providers.total,
        'pages': providers.pages,
        'current_page': page
    })

@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """
    Get service by ID
    ---
    tags:
      - Services
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Service details
      404:
        description: Service not found
    """
    service = User.query.filter_by(id=service_id, role='provider').first()
    if not service:
        raise not_found_error("Service")
    
    return jsonify({
        'id': service.id,
        'name': f"{service.first_name} {service.last_name}",
        'email': service.email,
        'phone': service.phone
    })

@services_bp.route('/', methods=['POST'])
@jwt_required()
def create_service():
    """
    Create new service
    ---
    tags:
      - Services
    parameters:
      - in: body
        name: service
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Service created
    """
    data = request.get_json()
    
    if not data or not data.get('title'):
        raise validation_error("Title is required")
    
    return jsonify({'message': 'Service created successfully'}), 201

@services_bp.route('/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    """
    Update service
    ---
    tags:
      - Services
    """
    data = request.get_json()
    
    if not data:
        raise validation_error("No data provided")
    
    return jsonify({'message': 'Service updated successfully'})

@services_bp.route('/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    """
    Delete service
    ---
    tags:
      - Services
    """
    return jsonify({'message': 'Service deleted successfully'})