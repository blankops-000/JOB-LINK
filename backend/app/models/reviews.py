from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'  # Table for customer reviews and ratings
    
    id = db.Column(db.Integer, primary_key=True)
    # Each review is for one specific booking
    # 'unique=True' ensures one booking can only have one review
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    # Which client wrote this review
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Which provider (user) this review is about
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Which provider profile this review is about
    provider_profile_id = db.Column(db.Integer, db.ForeignKey('provider_profiles.id'), nullable=False)
    # Rating from 1-5 stars
    rating = db.Column(db.Integer, nullable=False)
    # Optional text comment
    comment = db.Column(db.Text)
    # When the review was written
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'client_id': self.client_id,
            'provider_id': self.provider_id,
            'provider_profile_id': self.provider_profile_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }