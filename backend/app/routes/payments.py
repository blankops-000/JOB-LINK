from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.booking import Booking
from app.models.payment import Payment, PaymentStatus
from app.models.user import User
from app.utils.mpesa_service import MpesaService

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/initiate', methods=['POST'])
@jwt_required()
def initiate_payment():
    """Initiate M-Pesa payment for a booking"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        booking_id = data.get('booking_id')
        phone_number = data.get('phone_number')
        
        if not booking_id or not phone_number:
            return jsonify({'error': 'Booking ID and phone number are required'}), 400
        
        # Get booking
        booking = Booking.query.filter_by(
            id=booking_id, 
            client_id=current_user_id
        ).first_or_404()
        
        # Check if payment already exists
        existing_payment = Payment.query.filter_by(booking_id=booking_id).first()
        if existing_payment:
            return jsonify({'error': 'Payment already exists for this booking'}), 400
        
        # Initiate M-Pesa payment
        mpesa = MpesaService()
        result = mpesa.stk_push(
            phone_number=phone_number,
            amount=int(booking.total_amount),
            account_reference=f"BOOKING{booking_id}",
            transaction_desc=f"Payment for booking #{booking_id}"
        )
        
        if result['success']:
            # Create payment record
            payment = Payment(
                booking_id=booking_id,
                amount=booking.total_amount,
                phone_number=phone_number,
                status=PaymentStatus.PENDING
            )
            db.session.add(payment)
            db.session.commit()
            
            return jsonify({
                'message': 'Payment initiated successfully',
                'checkout_request_id': result['checkout_request_id'],
                'customer_message': result['customer_message'],
                'payment_id': payment.id
            }), 200
        else:
            return jsonify({'error': 'Payment initiation failed', 'details': result['error']}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Payment initiation failed', 'details': str(e)}), 500

@payments_bp.route('/mpesa-callback', methods=['POST'])
def mpesa_callback():
    """Handle M-Pesa payment callback"""
    try:
        callback_data = request.get_json()
        
        # Log the callback for debugging
        print("M-Pesa Callback:", json.dumps(callback_data, indent=2))
        
        # Extract relevant data from callback
        result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        result_desc = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultDesc')
        checkout_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        
        # Find payment by checkout_request_id (you might need to store this)
        payment = Payment.query.filter_by(...).first()  # You'll need to adjust this
        
        if payment:
            if result_code == 0:
                # Payment successful
                payment.status = PaymentStatus.COMPLETED
                # Update booking status
                payment.booking.status = 'confirmed'
            else:
                # Payment failed
                payment.status = PaymentStatus.FAILED
            
            db.session.commit()
        
        return jsonify({'ResultCode': 0, 'ResultDesc': 'Success'}), 200
        
    except Exception as e:
        print(f"Callback error: {str(e)}")
        return jsonify({'ResultCode': 1, 'ResultDesc': 'Failed'}), 500