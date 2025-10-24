from app import db
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    booking_id = db.Column(db.String, db.ForeignKey('bookings.id'), nullable=False)
    customer_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.String, db.ForeignKey('provider_profiles.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)