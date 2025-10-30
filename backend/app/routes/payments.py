from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.payment import Payment, PaymentStatus
from app.models.booking import Booking
from app.models.user import User
from app.utils.mpesa_api import MpesaService

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/mpesa/stk-push', methods=['POST'])
@jwt_required()
def initiate_mpesa_payment():
    """Initiate M-Pesa STK Push payment"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['booking_id', 'phone_number']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'booking_id and phone_number are required'}), 400
        
        # Get booking
        booking = Booking.query.filter_by(
            id=data['booking_id'],
            client_id=current_user_id
        ).first()
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if payment already exists
        existing_payment = Payment.query.filter_by(booking_id=booking.id).first()
        if existing_payment and existing_payment.status == PaymentStatus.COMPLETED:
            return jsonify({'error': 'Payment already completed'}), 400
        
        # Initialize M-Pesa service
        mpesa = MpesaService()
        
        # Initiate STK push
        result = mpesa.stk_push(
            phone_number=data['phone_number'],
            amount=booking.total_amount,
            account_reference=f"BOOKING_{booking.id}",
            transaction_desc=f"Payment for booking #{booking.id}"
        )
        
        if result['success']:
            # Create or update payment record
            if existing_payment:
                payment = existing_payment
            else:
                payment = Payment(
                    booking_id=booking.id,
                    amount=booking.total_amount,
                    payment_method='mpesa'
                )
                db.session.add(payment)
            
            payment.mpesa_checkout_request_id = result['checkout_request_id']
            payment.status = PaymentStatus.PENDING
            db.session.commit()
            
            return jsonify({
                'message': 'STK push initiated successfully',
                'checkout_request_id': result['checkout_request_id'],
                'customer_message': result['customer_message']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    """Handle M-Pesa callback"""
    try:
        data = request.get_json()
        
        # Extract callback data
        callback_data = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = callback_data.get('CheckoutRequestID')
        result_code = callback_data.get('ResultCode')
        
        if not checkout_request_id:
            return jsonify({'error': 'Invalid callback data'}), 400
        
        # Find payment record
        payment = Payment.query.filter_by(
            mpesa_checkout_request_id=checkout_request_id
        ).first()
        
        if not payment:
            return jsonify({'error': 'Payment record not found'}), 404
        
        # Update payment status based on result code
        if result_code == 0:  # Success
            payment.status = PaymentStatus.COMPLETED
            
            # Extract transaction details
            callback_metadata = callback_data.get('CallbackMetadata', {}).get('Item', [])
            for item in callback_metadata:
                if item.get('Name') == 'MpesaReceiptNumber':
                    payment.mpesa_receipt = item.get('Value')
                elif item.get('Name') == 'TransactionDate':
                    payment.transaction_date = item.get('Value')
        else:
            payment.status = PaymentStatus.FAILED
        
        db.session.commit()
        
        return jsonify({'message': 'Callback processed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/test-mpesa', methods=['POST'])
@jwt_required()
def test_mpesa():
    """Test M-Pesa integration"""
    try:
        data = request.get_json()
        
        if not data.get('phone_number'):
            return jsonify({'error': 'phone_number is required'}), 400
        
        mpesa = MpesaService()
        
        result = mpesa.stk_push(
            phone_number=data['phone_number'],
            amount=data.get('amount', 1),
            account_reference='TEST_PAYMENT',
            transaction_desc='Test M-Pesa payment'
        )
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500