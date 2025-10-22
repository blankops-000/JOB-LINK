from app import db

class ProviderProfile(db.Model):
    __tablename__ = 'provider_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    business_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    service_category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    experience_years = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relationships
    reviews = db.relationship('Review', backref='provider_profile', lazy='dynamic')
    bookings = db.relationship('Booking', backref='provider_profile', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'description': self.description,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'service_category_id': self.service_category_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_available': self.is_available,
            'experience_years': self.experience_years,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }