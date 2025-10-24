from app import db
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    customer_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.String, db.ForeignKey('provider_profiles.id'), nullable=False)
    service_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payments = db.relationship('Payment', backref='booking', lazy=True)
    reviews = db.relationship('Review', backref='booking', lazy=True)
    notifications = db.relationship('Notification', backref='booking', lazy=True)