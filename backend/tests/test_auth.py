"""
Comprehensive test suite for authentication endpoints
Tests user registration, login, JWT tokens, and error handling
"""
import pytest
import json

class TestAuthEndpoints:
    """
    Test class for authentication endpoints
    Each test method should test one specific functionality
    """
    
    def test_user_registration_success(self, client):
        """
        Test successful user registration with valid data
        Should return 201 status code, user data, and JWT token
        
        Args:
            client: pytest fixture that provides test client for HTTP requests
        """
        print("Testing user registration...")
        
        # Test data for registration
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'client'
        }
        
        # Make POST request to registration endpoint
        response = client.post('/api/auth/register',
                             data=json.dumps(user_data),      # Convert dict to JSON
                             content_type='application/json') # Set content type header
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        
        # Verify response status
        assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.data}"
        
        # Parse JSON response
        data = json.loads(response.data)
        
        # Verify successful registration
        assert data['msg'] == 'user registered'   # Success message
        assert data['user']['email'] == 'test@example.com'         # Correct email
        assert data['user']['first_name'] == 'John'                # Correct first name
        assert data['user']['last_name'] == 'Doe'                  # Correct last name
        assert data['user']['role'] == 'client'                    # Correct role
        assert 'access_token' in data                              # JWT token present
    
    def test_user_registration_duplicate_email(self, client):
        """
        Test registration with duplicate email address
        Should return 409 Conflict status with error message
        
        Args:
            client: pytest fixture for HTTP requests
        """
        # First registration - should succeed
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'client'
        }
        client.post('/api/auth/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Second registration with same email - should fail
        response = client.post('/api/auth/register',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        # Verify conflict error
        assert response.status_code == 409, f"Expected 409, got {response.status_code}"
        
        data = json.loads(response.data)
        assert 'already exists' in data['msg'].lower()          # Error message
    
    def test_user_registration_missing_fields(self, client):
        """
        Test registration with missing required fields
        Should return 400 Bad Request with details of missing fields
        
        Args:
            client: pytest fixture for HTTP requests
        """
        # Missing last_name field
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John'
            # last_name is missing - should cause error
        }
        
        response = client.post('/api/auth/register',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        # Verify bad request error
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = json.loads(response.data)
        assert 'required' in data['msg'].lower() # Error message
        assert 'last_name' in data['required']                    # Lists missing field
    
    def test_user_login_success(self, client):
        """
        Test successful user login with correct credentials
        Should return 200 status with user data and JWT token
        
        Args:
            client: pytest fixture for HTTP requests
        """
        # First register a user
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'client'
        }
        client.post('/api/auth/register',
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Then attempt login with correct credentials
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        print(f"Login response status: {response.status_code}")
        
        # Verify login success
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = json.loads(response.data)
        assert data['message'] == 'Login successful'             # Success message
        assert data['user']['email'] == 'test@example.com'       # Correct user data
        assert 'access_token' in data                            # JWT token present
    
    def test_user_login_invalid_credentials(self, client):
        """
        Test login with incorrect email or password
        Should return 401 Unauthorized with error message
        
        Args:
            client: pytest fixture for HTTP requests
        """
        # Attempt login with non-existent user
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }
        response = client.post('/api/auth/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        # Verify unauthorized error
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        
        data = json.loads(response.data)
        assert 'invalid credentials' in data['msg'].lower() # Error message
    
    def test_get_current_user_with_valid_token(self, client):
        """
        Test accessing protected endpoint with valid JWT token
        Should return 200 with user data
        
        Args:
            client: pytest fixture for HTTP requests
        """
        # Register and login to get token
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'client'
        }
        reg_response = client.post('/api/auth/register',
                                 data=json.dumps(user_data),
                                 content_type='application/json')
        reg_data = json.loads(reg_response.data)
        # Login to get token since registration doesn't return one
        login_data = {'email': 'test@example.com', 'password': 'password123'}
        login_response = client.post('/api/auth/login',
                                   data=json.dumps(login_data),
                                   content_type='application/json')
        login_data = json.loads(login_response.data)
        token = login_data['access_token']  # Extract JWT token
        
        # Access protected endpoint with token
        response = client.get('/api/auth/me',
                            headers={'Authorization': f'Bearer {token}'})
        
        # Verify successful access to protected endpoint
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = json.loads(response.data)
        assert data['user']['email'] == 'test@example.com'      # Correct user data
        assert data['user']['first_name'] == 'John'
    
    def test_get_current_user_without_token(self, client):
        """
        Test accessing protected endpoint without JWT token
        Should return 401 Unauthorized
        
        Args:
            client: pytest fixture for HTTP requests
        """
        # Access protected endpoint without authorization header
        response = client.get('/api/auth/me')
        
        # Verify unauthorized error
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        
        data = json.loads(response.data)
        assert 'missing' in data['msg'].lower()                 # Error message about missing token

    def test_user_registration_different_roles(self, client):
        """
        Test registration with different user roles
        Should accept client, provider, and admin roles
        
        Args:
            client: pytest fixture for HTTP requests
        """
        # Test client registration
        client_data = {
            'email': 'client@example.com',
            'password': 'password123',
            'first_name': 'Client',
            'last_name': 'User',
            'role': 'client'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(client_data),
                             content_type='application/json')
        assert response.status_code == 201, "Client registration failed"
        
        # Test provider registration
        provider_data = {
            'email': 'provider@example.com',
            'password': 'password123',
            'first_name': 'Provider',
            'last_name': 'User',
            'role': 'provider'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(provider_data),
                             content_type='application/json')
        assert response.status_code == 201, "Provider registration failed"
        
        # Test admin registration
        admin_data = {
            'email': 'admin@example.com',
            'password': 'password123',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin'
        }
        response = client.post('/api/auth/register',
                             data=json.dumps(admin_data),
                             content_type='application/json')
        assert response.status_code == 201, "Admin registration failed"