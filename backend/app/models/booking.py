from app import db
from datetime import datetime
import enum

# Define possible booking statuses
class BookingStatus(enum.Enum):
    PENDING = "pending"        # Booking requested but not confirmed
    CONFIRMED = "confirmed"    # Provider accepted the booking
    IN_PROGRESS = "in_progress" # Service is currently being performed
    COMPLETED = "completed"    # Service finished successfully
    CANCELLED = "cancelled"    # Booking was cancelled

class Booking(db.Model):
    __tablename__ = 'bookings'  # Table for service appointments
    
    id = db.Column(db.Integer, primary_key=True)
    # Client who booked the service - references User model
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Provider who will perform the service - references User model
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Link to provider's business profile
    provider_profile_id = db.Column(db.Integer, db.ForeignKey('provider_profiles.id'), nullable=False)
    # Type of service being booked
    service_category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    # When the service is scheduled to occur
    scheduled_date = db.Column(db.DateTime, nullable=False)
    # How long the service will take (in hours)
    duration_hours = db.Column(db.Integer, nullable=False)
    # Total cost (hourly_rate * duration_hours)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    # Current status of the booking
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.PENDING)
    # Any special requirements from the client
    special_requests = db.Column(db.Text)
    # Where the service will be performed
    address = db.Column(db.Text)
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # RELATIONSHIPS
    
    # One-to-one: Each booking can have one review
    # 'uselist=False' makes this a single object, not a list
    # 'cascade' means if booking is deleted, review is automatically deleted
    review = db.relationship('Review', backref='booking', uselist=False, cascade="all, delete-orphan")
    
    # One-to-one: Each booking can have one payment
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
            'status': self.status.value,  # Get string value from enum
            'special_requests': self.special_requests,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }