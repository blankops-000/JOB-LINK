"""
Tests for Swagger documentation setup
"""
def test_swagger_endpoints_exist(client):
    """Test that Swagger endpoints are accessible"""
    # Test Swagger UI endpoint
    response = client.get('/api/docs')
    assert response.status_code in [200, 302, 301, 308]  # Could be redirect or success
    
    # Test Swagger JSON specification endpoint
    response = client.get('/api/swagger.json')
    assert response.status_code == 200
    assert 'openapi' in response.get_json()
    assert 'paths' in response.get_json()

def test_swagger_spec_structure(client):
    """Test that Swagger specification has correct structure"""
    response = client.get('/api/swagger.json')
    spec = response.get_json()
    
    # Check required OpenAPI fields
    assert spec['openapi'] == '3.0.0'
    assert 'info' in spec
    assert 'paths' in spec
    assert 'components' in spec
    
    # Check that we have some endpoints documented
    assert len(spec['paths']) > 0
    assert '/api/auth/register' in spec['paths']
    assert '/api/auth/login' in spec['paths']