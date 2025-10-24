from app import db
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class ProviderProfile(db.Model):
    __tablename__ = 'provider_profiles'

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.String)
    service_area_id = db.Column(db.String)
    bio = db.Column(db.Text)
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    average_rating = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)

    bookings = db.relationship('Booking', backref='provider', foreign_keys='Booking.provider_id')
    reviews = db.relationship('Review', backref='provider', foreign_keys='Review.provider_id')