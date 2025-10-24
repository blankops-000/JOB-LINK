"""
Test to verify the basic app setup works
"""
def test_app_creation(client):
    """Test that we can create an app and make requests"""
    # This should work even if routes have issues
    response = client.get('/')
    # The root path might not exist, but we shouldn't get import errors
    assert response.status_code in [200, 404]  # Either is fine for now

def test_imports():
    """Test that we can import all necessary modules"""
    import app
    from app import db, create_app
    from app.models.user import User
    print("✅ All core imports work")
    assert True
    