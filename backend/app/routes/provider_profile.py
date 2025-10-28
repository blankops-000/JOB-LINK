from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import ProviderProfile, User, ServiceCategory

provider_bp = Blueprint('provider', __name__)

# ----- CREATE PROVIDER PROFILE -----
@provider_bp.route('/create', methods=['POST'])
@jwt_required()
def create_provider_profile():
    user_id = get_jwt_identity()  # current logged-in user
    data = request.get_json()

    # Check if this user already has a profile
    if ProviderProfile.query.filter_by(user_id=user_id).first():
        return jsonify({'message': 'Provider profile already exists for this user'}), 400

    business_name = data.get('business_name')
    description = data.get('description')
    hourly_rate = data.get('hourly_rate')
    service_category_id = data.get('service_category_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    experience_years = data.get('experience_years', 0)

    # Validate required fields
    if not business_name or not hourly_rate or not service_category_id:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check that the service category exists
    if not ServiceCategory.query.get(service_category_id):
        return jsonify({'message': 'Invalid service category ID'}), 400

    new_profile = ProviderProfile(
        user_id=user_id,
        business_name=business_name,
        description=description,
        hourly_rate=hourly_rate,
        service_category_id=service_category_id,
        latitude=latitude,
        longitude=longitude,
        experience_years=experience_years
    )

    db.session.add(new_profile)
    db.session.commit()

    return jsonify({'message': 'Provider profile created successfully', 'profile': new_profile.to_dict()}), 201


# ----------------- GET ALL PROVIDER PROFILES -----------------
@provider_bp.route('/providers', methods=['GET'])
def get_all_providers():
    providers = ProviderProfile.query.all()
    return jsonify([p.to_dict() for p in providers]), 200


# ----------------- GET SINGLE PROVIDER BY ID -----------------
@provider_bp.route('/providers/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    provider = ProviderProfile.query.get(provider_id)
    if not provider:
        return jsonify({'message': 'Provider not found'}), 404
    return jsonify(provider.to_dict()), 200


# ----------------- UPDATE PROVIDER PROFILE -----------------
@provider_bp.route('/providers/<int:provider_id>', methods=['PUT'])
@jwt_required()
def update_provider(provider_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    provider = ProviderProfile.query.get(provider_id)
    if not provider:
        return jsonify({'message': 'Provider not found'}), 404

    # Ensure provider belongs to the logged-in user
    if provider.user_id != user_id:
        return jsonify({'message': 'Unauthorized to update this profile'}), 403

    provider.business_name = data.get('business_name', provider.business_name)
    provider.description = data.get('description', provider.description)
    provider.hourly_rate = data.get('hourly_rate', provider.hourly_rate)
    provider.service_category_id = data.get('service_category_id', provider.service_category_id)
    provider.latitude = data.get('latitude', provider.latitude)
    provider.longitude = data.get('longitude', provider.longitude)
    provider.is_available = data.get('is_available', provider.is_available)
    provider.experience_years = data.get('experience_years', provider.experience_years)

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully', 'profile': provider.to_dict()}), 200


# ----------------- DELETE PROVIDER PROFILE -----------------
@provider_bp.route('/providers/<int:provider_id>', methods=['DELETE'])
@jwt_required()
def delete_provider(provider_id):
    user_id = get_jwt_identity()
    provider = ProviderProfile.query.get(provider_id)

    if not provider:
        return jsonify({'message': 'Provider not found'}), 404

    if provider.user_id != user_id:
        return jsonify({'message': 'Unauthorized to delete this profile'}), 403

    db.session.delete(provider)
    db.session.commit()
    return jsonify({'message': 'Provider profile deleted successfully'}), 200
