"""
Diagnostic test to check if basic setup is working
Run this first to identify where the problem is
"""

def test_basic_setup():
    """Test that basic Python and pytest are working"""
    print("Running diagnostic test...")
    assert 1 == 1
    print("✅ Basic assertion test passed")

def test_imports():
    """Test if we can import the required modules"""
    import sys
    import os
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(current_dir)
    
    print(f"Current directory: {current_dir}")
    print(f"Backend directory: {backend_dir}")
    
    # Add to path
    sys.path.insert(0, backend_dir)
    print("Added backend to Python path")
    
    # Try to import
    try:
        from app import create_app
        print("✅ Successfully imported create_app")
        
        # Test app creation
        app = create_app()
        print("✅ Successfully created app instance")
        
        # Test database
        with app.app_context():
            from app import db
            print("✅ Successfully imported db")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

if __name__ == "__main__":
    # Run diagnostics manually
    test_basic_setup()
    test_imports()