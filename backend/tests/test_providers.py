import pytest
import json
import os
import sys

# Add the backend directory to Python path so pytest can find the app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import your app modules
from app import create_app, db
from app.models.user import User, RoleEnum
from app.models.provider_profile import ProviderProfile
from app.models.service_category import ServiceCategory

class TestProviderEndpoints:
    """Test suite for provider profile endpoints"""
    
    def setup_method(self):
        """Setup test environment with necessary data"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from flask_jwt_extended import JWTManager
            jwt = JWTManager(self.app)
            
            db.create_all()
            # Create test service categories (check if they exist first)
            existing_plumbing = ServiceCategory.query.filter_by(name='Plumbing').first()
            if not existing_plumbing:
                categories = [
                    ServiceCategory(name='Plumbing', description='Pipe services'),
                    ServiceCategory(name='Electrical', description='Wiring services')
                ]
                for category in categories:
                    db.session.add(category)
                db.session.commit()
    
    def teardown_method(self):
        """Cleanup test environment"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_provider_profile_success(self):
        """Test successful provider profile creation"""
        # Register a provider user first
        user_data = {
            'email': 'provider@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'provider'
        }
        self.client.post('/api/auth/register',
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        # Login to get token
        login_data = {'email': 'provider@example.com', 'password': 'password123'}
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(login_data),
                                        content_type='application/json')
        auth_data = json.loads(login_response.data)
        token = auth_data['access_token']
        
        # Create provider profile
        profile_data = {
            'business_name': 'Test Plumbing Services',
            'description': 'Professional plumbing services',
            'hourly_rate': 25.50,
            'service_category_id': 1,
            'experience_years': 5
        }
        
        response = self.client.post('/api/providers',
                                  data=json.dumps(profile_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data)
        
        # Verify successful creation
        assert response.status_code == 201
        assert data['message'] == 'Provider profile created successfully'
        assert data['provider']['business_name'] == 'Test Plumbing Services'
        assert data['provider']['hourly_rate'] == 25.50
    
    def test_get_providers_list(self):
        """Test retrieving list of providers"""
        # Create a provider with profile first
        user_data = {
            'email': 'provider@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'provider'
        }
        self.client.post('/api/auth/register',
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        # Login to get token
        login_data = {'email': 'provider@example.com', 'password': 'password123'}
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(login_data),
                                        content_type='application/json')
        auth_data = json.loads(login_response.data)
        token = auth_data['access_token']
        
        # Create provider profile
        profile_data = {
            'business_name': 'Test Plumbing',
            'hourly_rate': 25.50,
            'service_category_id': 1
        }
        self.client.post('/api/providers',
                        data=json.dumps(profile_data),
                        content_type='application/json',
                        headers={'Authorization': f'Bearer {token}'})
        
        # Get providers list
        response = self.client.get('/api/providers?page=1&per_page=10')
        data = json.loads(response.data)
        
        # Verify successful retrieval
        assert response.status_code == 200
        assert 'providers' in data
        assert 'pagination' in data
        assert len(data['providers']) > 0
    
    def test_get_provider_by_id(self):
        """Test retrieving specific provider by ID"""
        # Create provider first
        user_data = {
            'email': 'provider@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'provider'
        }
        self.client.post('/api/auth/register',
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        # Login to get token
        login_data = {'email': 'provider@example.com', 'password': 'password123'}
        login_response = self.client.post('/api/auth/login',
                                        data=json.dumps(login_data),
                                        content_type='application/json')
        auth_data = json.loads(login_response.data)
        token = auth_data['access_token']
        
        profile_data = {
            'business_name': 'Test Plumbing',
            'hourly_rate': 25.50,
            'service_category_id': 1
        }
        self.client.post('/api/providers',
                        data=json.dumps(profile_data),
                        content_type='application/json',
                        headers={'Authorization': f'Bearer {token}'})
        
        # Get provider by ID (ID 1 since it's the first one)
        response = self.client.get('/api/providers/1')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['provider']['business_name'] == 'Test Plumbing'