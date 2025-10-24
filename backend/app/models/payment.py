from app import db
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    booking_id = db.Column(db.String, db.ForeignKey('bookings.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50))
    transaction_ref = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)