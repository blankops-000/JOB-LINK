from app import db
from datetime import datetime

class ProviderProfile(db.Model):
    __tablename__ = 'provider_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    hourly_rate = db.Column(db.Float)
    location = db.Column(db.String(200))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='provider_profile')
    bookings = db.relationship('Booking', backref='provider')
    reviews = db.relationship('Review', backref='provider')