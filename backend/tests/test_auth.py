import pytest
import json
import os
import sys

# Get the absolute path to the backend directory
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add backend directory to Python path
sys.path.insert(0, backend_dir)

# Now import your app modules
from app import create_app, db
from app.models.user import User

class TestAuthEndpoints:
    """
    Comprehensive test suite for authentication endpoints
    Tests user registration, login, and token validation
    """
    
    def setup_method(self):
        """
        Initialize test environment before each test
        Creates fresh in-memory database for isolation
        """
        print("Setting up test environment...")
        
        # Create Flask application instance with testing configuration
        self.app = create_app()
        
        # Testing configuration
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['JWT_SECRET_KEY'] = 'test-secret-key'  # Required for JWT
        
        # Create test client for making HTTP requests
        self.client = self.app.test_client()
        
        # Create application context and database tables
        with self.app.app_context():
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully")
    
    def teardown_method(self):
        """
        Clean up test environment after each test
        Ensures tests don't interfere with each other
        """
        print("Cleaning up test environment...")
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_simple_assertion(self):
        """Simple test to verify pytest is working"""
        assert 1 + 1 == 2
    
    def test_app_creation(self):
        """Test that the app can be created successfully"""
        assert self.app is not None
        assert self.app.config['TESTING'] == True
    
    def test_user_registration_success(self):
        """
        Test successful user registration with valid data
        Should return 201 status and user data with JWT token
        """
        print("Testing user registration...")
        
        # Test data for user registration
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'client'
        }
        
        # Make POST request to registration endpoint
        response = self.client.post('/api/auth/register',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        # Parse JSON response data
        data = json.loads(response.data)
        
        # Assertions to verify successful registration
        assert response.status_code == 201  # HTTP 201 Created status
        assert data['message'] == 'User registered successfully'  # Success message
        assert data['user']['email'] == 'test@example.com'  # Correct email in response
        assert 'access_token' in data  # JWT token should be present
    
    def test_user_login_success(self):
        """
        Test successful user login with correct credentials
        Should return 200 status with user data and JWT token
        """
        print("Testing user login...")
        
        # First register a user
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'client'
        }
        self.client.post('/api/auth/register',
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        # Then attempt login with correct credentials
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        
        print(f"Login response status: {response.status_code}")
        
        data = json.loads(response.data)
        
        # Verify login success
        assert response.status_code == 200  # HTTP 200 OK
        assert data['message'] == 'Login successful'  # Success message
        assert 'access_token' in data  # JWT token should be present