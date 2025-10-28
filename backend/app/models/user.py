# Import necessary modules and dependencies
from app import db, bcrypt  # Import database instance and bcrypt for password hashing
from datetime import datetime  # For timestamp fields
import enum  # For creating enumerated types (fixed set of values)

# Define user roles as an enumeration - ensures only valid roles can be assigned
class RoleEnum(enum.Enum):
    ADMIN = "admin"      # Platform administrator with full access
    PROVIDER = "provider" # Service provider who offers services
    CLIENT = "client"    # Regular customer who books services

# Main User model class that represents the 'users' table in database
class User(db.Model):
    __tablename__ = 'users'  # Explicitly set table name to 'users'
    
    # Primary key - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    # Email must be unique and indexed for fast lookups, cannot be null
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    # Store hashed password, not plain text (security)
    password_hash = db.Column(db.String(255), nullable=False)
    # User's first and last name - required fields
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # Optional phone number field
    phone = db.Column(db.String(20))
    # Role field using our enum - defaults to 'client', cannot be null
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.CLIENT)
    # Track if user has verified their email address
    is_verified = db.Column(db.Boolean, default=False)
    # Automatic timestamps for record creation and updates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # RELATIONSHIPS will be added when other models are created
    
    # METHOD: Hash and store password securely
    def set_password(self, password):
        # bcrypt hashes the password and we decode to store as string
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # METHOD: Verify if provided password matches stored hash
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    # METHOD: Convert user object to dictionary for JSON responses
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role.value,  # Get the string value from enum
            'is_verified': self.is_verified,
            # Convert datetime to ISO format string for JSON compatibility
            'created_at': self.created_at.isoformat() if self.created_at else None
        }