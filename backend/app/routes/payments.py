"""
Payment Routes
Handles M-Pesa payment processing for bookings
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.booking import Booking, BookingStatus
from app.models.payment import Payment, PaymentStatus
from app.models.user import User
from app.utils.mpesa_service import MpesaService
from app.utils.email_service import EmailService
from app.utils.auth import client_required

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/initiate', methods=['POST'])
@jwt_required()
@client_required
def initiate_payment():
    """
    Initiate M-Pesa STK push payment for a booking
    
    Request body:
    {
        "booking_id": 1,
        "phone_number": "0712345678"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('booking_id') or not data.get('phone_number'):
            return jsonify({'error': 'booking_id and phone_number are required'}), 400
        
        # Get booking
        booking = Booking.query.filter_by(
            id=data['booking_id'],
            client_id=int(current_user_id)
        ).first()
        
        if not booking:
            return jsonify({'error': 'Booking not found or access denied'}), 404
        
        # Check if booking is in pending or confirmed status
        if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            return jsonify({'error': 'Booking cannot be paid at this stage'}), 400
        
        # Check if payment already exists
        existing_payment = Payment.query.filter_by(booking_id=booking.id).first()
        if existing_payment and existing_payment.status == PaymentStatus.COMPLETED:
            return jsonify({'error': 'Payment already completed for this booking'}), 400
        
        # Initialize M-Pesa service
        mpesa = MpesaService()
        
        # Initiate STK push
        result = mpesa.stk_push(
            phone_number=data['phone_number'],
            amount=int(booking.total_amount),
            account_reference=f"BOOKING-{booking.id}",
            transaction_desc=f"Payment for {booking.service_category.name}"
        )
        
        if result.get('success'):
            # Create or update payment record
            if existing_payment:
                payment = existing_payment
                payment.status = PaymentStatus.PENDING
            else:
                payment = Payment(
                    booking_id=booking.id,
                    amount=booking.total_amount,
                    phone_number=data['phone_number'],
                    status=PaymentStatus.PENDING
                )
                db.session.add(payment)
            
            # Store checkout request ID for callback matching
            payment.mpesa_receipt = result.get('checkout_request_id')
            db.session.commit()
            
            return jsonify({
                'message': 'Payment initiated successfully',
                'checkout_request_id': result.get('checkout_request_id'),
                'customer_message': result.get('customer_message'),
                'payment_id': payment.id
            }), 200
        else:
            return jsonify({
                'error': 'Payment initiation failed',
                'details': result.get('error')
            }), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to initiate payment', 'details': str(e)}), 500


@payments_bp.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    """
    M-Pesa callback endpoint
    Receives payment confirmation from Safaricom
    """
    try:
        data = request.get_json()
        
        # Extract callback data
        body = data.get('Body', {})
        stk_callback = body.get('stkCallback', {})
        
        result_code = stk_callback.get('ResultCode')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        
        # Find payment by checkout request ID
        payment = Payment.query.filter_by(mpesa_receipt=checkout_request_id).first()
        
        if not payment:
            return jsonify({'ResultCode': 0, 'ResultDesc': 'Payment not found'}), 200
        
        # Check if payment was successful
        if result_code == 0:
            # Payment successful
            callback_metadata = stk_callback.get('CallbackMetadata', {})
            items = callback_metadata.get('Item', [])
            
            # Extract payment details
            mpesa_receipt = None
            phone_number = None
            
            for item in items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    mpesa_receipt = item.get('Value')
                elif item.get('Name') == 'PhoneNumber':
                    phone_number = item.get('Value')
            
            # Update payment record
            payment.status = PaymentStatus.COMPLETED
            payment.mpesa_receipt = mpesa_receipt or checkout_request_id
            if phone_number:
                payment.phone_number = str(phone_number)
            
            # Update booking status
            booking = payment.booking
            if booking.status == BookingStatus.PENDING:
                booking.status = BookingStatus.CONFIRMED
            
            db.session.commit()
            
            # Send confirmation email
            try:
                user = User.query.get(int(booking.client_id))
                if user:
                    EmailService.send_payment_confirmation(payment, booking, user)
            except Exception as email_error:
                print(f"Email notification failed: {email_error}")
            
            return jsonify({'ResultCode': 0, 'ResultDesc': 'Payment processed successfully'}), 200
        else:
            # Payment failed or cancelled
            payment.status = PaymentStatus.FAILED
            db.session.commit()
            
            return jsonify({'ResultCode': 0, 'ResultDesc': 'Payment failed'}), 200
            
    except Exception as e:
        print(f"M-Pesa callback error: {str(e)}")
        return jsonify({'ResultCode': 1, 'ResultDesc': 'Internal server error'}), 500


@payments_bp.route('/status/<int:payment_id>', methods=['GET'])
@jwt_required()
def check_payment_status(payment_id):
    """Check payment status"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get payment
        payment = Payment.query.get_or_404(payment_id)
        
        # Check authorization
        booking = payment.booking
        if booking.client_id != int(current_user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'payment': payment.to_dict(),
            'booking_status': booking.status.value
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to check payment status', 'details': str(e)}), 500


@payments_bp.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking_payment(booking_id):
    """Get payment details for a booking"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(int(current_user_id))
        
        # Get booking
        booking = Booking.query.get_or_404(booking_id)
        
        # Check authorization
        if (current_user.role.value != 'admin' and 
            booking.client_id != int(current_user_id) and 
            booking.provider_id != int(current_user_id)):
            return jsonify({'error': 'Access denied'}), 403
        
        # Get payment
        payment = Payment.query.filter_by(booking_id=booking_id).first()
        
        if not payment:
            return jsonify({'message': 'No payment found for this booking'}), 404
        
        return jsonify({'payment': payment.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get payment', 'details': str(e)}), 500


@payments_bp.route('/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    """Get payment history for current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get all bookings for this user
        bookings = Booking.query.filter_by(client_id=int(current_user_id)).all()
        booking_ids = [b.id for b in bookings]
        
        # Get payments for these bookings
        payments = Payment.query.filter(Payment.booking_id.in_(booking_ids)).order_by(
            Payment.created_at.desc()
        ).all()
        
        payment_list = []
        for payment in payments:
            payment_data = payment.to_dict()
            payment_data['booking'] = payment.booking.to_dict()
            payment_list.append(payment_data)
        
        return jsonify({'payments': payment_list}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get payment history', 'details': str(e)}), 500
