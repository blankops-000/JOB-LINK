# Import testing framework and Flask test client
import pytest
import json
from app import create_app, db
from app.models.user import User

# Test class for authentication endpoints
class TestAuthEndpoints:
    """Test cases for authentication endpoints"""
    
    # Setup method that runs before each test
    def setup_method(self):
        """Create test application and database"""
        # Create test Flask application
        self.app = create_app()
        # Configure for testing
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        # Create test client
        self.client = self.app.test_client()
        
        # Create application context and database tables
        with self.app.app_context():
            db.create_all()
    
    # Teardown method that runs after each test
    def teardown_method(self):
        """Clean up after tests"""
        with self.app.app_context():
            # Drop all tables and remove session
            db.session.remove()
            db.drop_all()
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        # Test data for registration
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
        
        # Parse response JSON
        data = json.loads(response.data)
        
        # Assertions to verify successful registration
        assert response.status_code == 201  # HTTP 201 Created
        assert data['message'] == 'User registered successfully'
        assert data['user']['email'] == 'test@example.com'
        assert 'access_token' in data  # Should return JWT token
    
    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        # First registration
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
        
        # Second registration with same email
        response = self.client.post('/api/auth/register',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        # Should return conflict error
        assert response.status_code == 409
        assert 'already exists' in data['error']
    
    def test_user_login_success(self):
        """Test successful user login"""
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
        
        # Then attempt login
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        # Verify login success
        assert response.status_code == 200
        assert data['message'] == 'Login successful'
        assert 'access_token' in data
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/login',
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        # Should return unauthorized error
        assert response.status_code == 401
        assert 'Invalid email or password' in data['error']