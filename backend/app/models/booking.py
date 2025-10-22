from app import db
from datetime import datetime
import enum

class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_profile_id = db.Column(db.Integer, db.ForeignKey('provider_profiles.id'), nullable=False)
    service_category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration_hours = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.PENDING)
    special_requests = db.Column(db.Text)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    review = db.relationship('Review', backref='booking', uselist=False, cascade="all, delete-orphan")
    payment = db.relationship('Payment', backref='booking', uselist=False, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'provider_id': self.provider_id,
            'provider_profile_id': self.provider_profile_id,
            'service_category_id': self.service_category_id,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'duration_hours': self.duration_hours,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'status': self.status.value,
            'special_requests': self.special_requests,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }