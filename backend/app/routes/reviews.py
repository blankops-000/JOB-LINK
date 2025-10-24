from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.review import Review

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([r.to_dict() for r in reviews]), 200

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    data = request.get_json()
    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201

@reviews_bp.route('/<uuid:id>', methods=['PATCH'])
@jwt_required()
def update_review(id):
    review = Review.query.get_or_404(id)
    data = request.get_json()
    for field, value in data.items():
        setattr(review, field, value)
    db.session.commit()
    return jsonify(review.to_dict()), 200

@reviews_bp.route('/<uuid:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200
