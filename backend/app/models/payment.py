from app import db
import enum

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    mpesa_receipt = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'amount': float(self.amount) if self.amount else None,
            'mpesa_receipt': self.mpesa_receipt,
            'phone_number': self.phone_number,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }