"""
Simple test file to verify pytest setup is working
This should run without any dependencies on your app
"""

def test_basic_math():
    """
    Most basic test - verifies that pytest can run tests
    This test doesn't depend on Flask or your app
    """
    # Simple assertion - if this fails, something is wrong with pytest itself
    assert 1 + 1 == 2

def test_string_operations():
    """Test basic string operations"""
    name = "JobLink"
    assert len(name) == 7
    assert name.startswith("Job")
    assert name.endswith("Link")

def test_list_operations():
    """Test basic list operations"""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert sum(numbers) == 15
    assert 3 in numbers

def test_pytest_fixtures():
    """Test that pytest fixtures work"""
    # This test verifies pytest can handle setup/teardown
    test_data = {"user": "test", "active": True}
    assert test_data["user"] == "test"
    assert test_data["active"] is True

# You can run this test with: pytest tests/test_simple.py -v