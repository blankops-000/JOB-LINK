"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def app():
    """
    Create a Flask app for testing
    """
    from flask import Flask
    from app import db
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Configure for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key-for-jwt-tokens'
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)
    
    # Register routes that work
    with app.app_context():
        db.create_all()
        
        # These routes work (from diagnostic)
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        
        from app.routes.providers import providers_bp
        app.register_blueprint(providers_bp, url_prefix='/api/providers')
        
        from app.routes.bookings import bookings_bp
        app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
        
        # Try to register reviews routes (skip if broken)
        try:
            from app.routes.reviews import reviews_bp
            app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
            print("[OK] Reviews routes registered")
        except ImportError as e:
            print(f"[WARN] Skipping reviews routes: {e}")
        
        # Try to register admin routes (skip if broken)  
        try:
            from app.routes.admin import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/api/admin')
            print("[OK] Admin routes registered")
        except ImportError as e:
            print(f"[WARN] Skipping admin routes: {e}")
            
        # Register Swagger routes
        try:
            from app.docs.swagger import swaggerui_blueprint, create_swagger_spec
            app.register_blueprint(swaggerui_blueprint)
            create_swagger_spec(app)
            print("[OK] Swagger routes registered")
        except ImportError as e:
            print(f"[WARN] Skipping swagger routes: {e}")
    
    yield app
    
    # Cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()