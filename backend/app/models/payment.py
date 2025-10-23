from app import db
from datetime import datetime
import enum

# Define possible payment statuses
class PaymentStatus(enum.Enum):
    PENDING = "pending"    # Payment initiated but not completed
    COMPLETED = "completed" # Payment successfully processed
    FAILED = "failed"      # Payment failed or was declined
    REFUNDED = "refunded"  # Payment was refunded

class Payment(db.Model):
    __tablename__ = 'payments'  # Table for payment transactions
    
    id = db.Column(db.Integer, primary_key=True)
    # Link to the booking this payment is for
    # 'unique=True' ensures one booking can only have one payment
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    # Amount paid
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    # M-Pesa transaction receipt number
    mpesa_receipt = db.Column(db.String(50))
    # Phone number used for payment
    phone_number = db.Column(db.String(20))
    # Current status of the payment
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': float(self.amount) if self.amount else None,
            'mpesa_receipt': self.mpesa_receipt,
            'phone_number': self.phone_number,
            'status': self.status.value,  # Get string value from enum
            'created_at': self.created_at.isoformat() if self.created_at else None
        }