import pytest
import json
from app import create_app, db
from app.models.user import User, RoleEnum
from app.models.provider_profile import ProviderProfile
from app.models.service_category import ServiceCategory

class TestProviderEndpoints:
    """Test cases for provider endpoints"""
    
    def setup_method(self):
        """Setup test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test service category
            category = ServiceCategory(name='Plumbing', description='Test category')
            db.session.add(category)
            db.session.commit()
    
    def teardown_method(self):
        """Cleanup test environment"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_provider_profile(self):
        """Test creating a provider profile"""
        # First create a provider user
        user_data = {
            'email': 'provider@example.com',
            'password': 'password123',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'provider'
        }
        response = self.client.post('/api/auth/register',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        auth_data = json.loads(response.data)
        token = auth_data['access_token']
        
        # Create provider profile
        profile_data = {
            'business_name': 'Test Plumbing',
            'description': 'Professional plumbing services',
            'hourly_rate': 25.50,
            'service_category_id': 1
        }
        
        response = self.client.post('/api/providers',
                                  data=json.dumps(profile_data),
                                  content_type='application/json',
                                  headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data)
        
        assert response.status_code == 201
        assert data['message'] == 'Provider profile created successfully'
        assert data['provider']['business_name'] == 'Test Plumbing'