from app import db

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_profile_id = db.Column(db.Integer, db.ForeignKey('provider_profiles.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'client_id': self.client_id,
            'provider_profile_id': self.provider_profile_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }