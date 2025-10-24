from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.service_category import ServiceCategory

service_bp = Blueprint('services', __name__, url_prefix='/services')

@service_bp.route('/', methods=['GET'])
def get_services():
    services = ServiceCategory.query.all()
    return jsonify([s.to_dict() for s in services]), 200

@service_bp.route('/', methods=['POST'])
@jwt_required()
def create_service():
    data = request.get_json()
    service = ServiceCategory(**data)
    db.session.add(service)
    db.session.commit()
    return jsonify(service.to_dict()), 201

@service_bp.route('/<uuid:id>', methods=['PATCH'])
@jwt_required()
def update_service(id):
    service = ServiceCategory.query.get_or_404(id)
    data = request.get_json()
    for field, value in data.items():
        setattr(service, field, value)
    db.session.commit()
    return jsonify(service.to_dict()), 200

@service_bp.route('/<uuid:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    service = ServiceCategory.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted"}), 200
