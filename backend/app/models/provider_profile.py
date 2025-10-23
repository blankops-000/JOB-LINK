from app import db
from datetime import datetime

class ProviderProfile(db.Model):
    __tablename__ = 'provider_profiles'  # Business profiles for service providers
    
    id = db.Column(db.Integer, primary_key=True)
    # Links to the User model - each provider profile belongs to one user
    # 'unique=True' ensures one user can only have one provider profile
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    # The business name for this provider
    business_name = db.Column(db.String(200), nullable=False)
    # Description of services offered
    description = db.Column(db.Text)
    # Hourly rate charged by this provider
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)  # 10 digits, 2 decimal places
    # Which service category this provider belongs to
    service_category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    # Location coordinates for geo-search functionality
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # Whether provider is currently accepting new bookings
    is_available = db.Column(db.Boolean, default=True)
    # Years of experience in this field
    experience_years = db.Column(db.Integer, default=0)
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # RELATIONSHIPS
    
    # One-to-many: A provider can have many reviews
    reviews = db.relationship('Review', backref='provider_profile', lazy='dynamic')
    
    # One-to-many: A provider can have many bookings
    bookings = db.relationship('Booking', backref='provider_profile', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'business_name': self.business_name,
            'description': self.description,
            # Convert decimal to float for JSON serialization
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'service_category_id': self.service_category_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_available': self.is_available,
            'experience_years': self.experience_years,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }