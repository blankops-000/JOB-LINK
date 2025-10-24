from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.payment import Payment

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')

@payments_bp.route('/', methods=['GET'])
@jwt_required()
def get_payments():
    payments = Payment.query.all()
    return jsonify([p.to_dict() for p in payments]), 200

@payments_bp.route('/', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    payment = Payment(**data)
    db.session.add(payment)
    db.session.commit()
    return jsonify(payment.to_dict()), 201
