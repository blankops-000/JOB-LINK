from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.service_category import ServiceCategory
from app.models.user import User

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
def get_services():
    """Get all service categories with optional filtering"""
    try:
        # Get query parameters for filtering
        search = request.args.get('search', '')
        
        # Build query
        query = ServiceCategory.query
        
        # Apply search filter if provided
        if search:
            query = query.filter(ServiceCategory.name.ilike(f'%{search}%'))
        
        # Execute query
        services = query.all()
        
        # Convert to dict format
        services_data = [service.to_dict() for service in services]
        
        return jsonify({
            'services': services_data,
            'total': len(services_data),
            'message': 'Services retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Error retrieving services',
            'error': str(e)
        }), 500

@services_bp.route('/', methods=['POST'])
@jwt_required()
def create_service():
    """Create a new service category (Admin only)"""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        # Check if user is admin (for now, allow all authenticated users)
        # TODO: Add proper role checking when admin role is implemented
        
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name'):
            return jsonify({'message': 'Service name is required'}), 400
            
        # Check if service already exists
        existing = ServiceCategory.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'message': 'Service category already exists'}), 409
            
        # Create new service category
        service = ServiceCategory(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'message': 'Service category created successfully',
            'service': service.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error creating service category',
            'error': str(e)
        }), 500

@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id):
    """Get a specific service category by ID"""
    try:
        service = ServiceCategory.query.get(service_id)
        
        if not service:
            return jsonify({
                'message': 'Service category not found'
            }), 404
            
        return jsonify({
            'service': service.to_dict(),
            'message': 'Service retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Error retrieving service',
            'error': str(e)
        }), 500

@services_bp.route('/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    """Update an existing service category (Admin only)"""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        # Find the service to update
        service = ServiceCategory.query.get(service_id)
        if not service:
            return jsonify({'message': 'Service category not found'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        # Update fields if provided
        if 'name' in data:
            # Check if new name already exists (excluding current service)
            existing = ServiceCategory.query.filter(
                ServiceCategory.name == data['name'],
                ServiceCategory.id != service_id
            ).first()
            
            if existing:
                return jsonify({'message': 'Service name already exists'}), 409
                
            service.name = data['name']
            
        if 'description' in data:
            service.description = data['description']
            
        db.session.commit()
        
        return jsonify({
            'message': 'Service category updated successfully',
            'service': service.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error updating service category',
            'error': str(e)
        }), 500

@services_bp.route('/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    """Delete a service category (Admin only)"""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        # Find the service to delete
        service = ServiceCategory.query.get(service_id)
        if not service:
            return jsonify({'message': 'Service category not found'}), 404
            
        # Check if service has associated providers (optional safety check)
        # Uncomment if you want to prevent deletion of services with providers
        # if service.providers.count() > 0:
        #     return jsonify({'message': 'Cannot delete service with active providers'}), 409
            
        # Store service data for response
        service_data = service.to_dict()
        
        # Delete the service
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({
            'message': 'Service category deleted successfully',
            'deleted_service': service_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error deleting service category',
            'error': str(e)
        }), 500