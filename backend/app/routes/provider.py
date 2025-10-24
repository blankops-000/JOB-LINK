from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.provider_profile import ProviderProfile
from app.utils.schemas import ProviderProfileSchema

provider_bp = Blueprint('providers', __name__, url_prefix='/providers')

schema = ProviderProfileSchema()

# GET all providers (with pagination)
@provider_bp.route('/', methods=['GET'])
def get_providers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = ProviderProfile.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "providers": schema.dump(pagination.items, many=True),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200

# CREATE new provider profile
@provider_bp.route('/', methods=['POST'])
@jwt_required()
def create_provider():
    data = request.get_json() or {}
    errors = schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    provider = ProviderProfile(**data)
    db.session.add(provider)
    db.session.commit()
    return jsonify(schema.dump(provider)), 201

# GET one provider
@provider_bp.route('/<uuid:id>', methods=['GET'])
def get_provider(id):
    provider = ProviderProfile.query.get_or_404(id)
    return jsonify(schema.dump(provider)), 200

# UPDATE provider
@provider_bp.route('/<uuid:id>', methods=['PATCH'])
@jwt_required()
def update_provider(id):
    provider = ProviderProfile.query.get_or_404(id)
    data = request.get_json() or {}
    errors = schema.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for key, value in data.items():
        setattr(provider, key, value)
    db.session.commit()
    return jsonify(schema.dump(provider)), 200

# DELETE provider
@provider_bp.route('/<uuid:id>', methods=['DELETE'])
@jwt_required()
def delete_provider(id):
    provider = ProviderProfile.query.get_or_404(id)
    db.session.delete(provider)
    db.session.commit()
    return jsonify({"message": "Provider deleted successfully"}), 200
