from app import db
from datetime import datetime

class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'  # Table name for service categories
    
    id = db.Column(db.Integer, primary_key=True)
    # Category name must be unique (only one "Plumbing" category)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # Optional description of the service category
    description = db.Column(db.Text)
    # When this category was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # RELATIONSHIPS
    
    # One-to-many: One category can have many provider profiles
    # 'lazy=dynamic' allows querying like: category.providers.filter_by(...)
    providers = db.relationship('ProviderProfile', backref='service_category', lazy='dynamic')
    
    # One-to-many: One category can have many bookings
    bookings = db.relationship('Booking', backref='service_category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }