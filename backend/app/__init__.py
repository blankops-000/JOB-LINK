import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from app.docs.swagger import swaggerui_blueprint, create_swagger_spec

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)
    
    # Load configuration based on environment
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('app.config.ProductionConfig')
    elif env == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', ['http://localhost:3000'])
        }
    })
    
    # Register Swagger UI Blueprint
    app.register_blueprint(swaggerui_blueprint)
    print("[OK] Swagger UI blueprint registered")
    
    # Create Swagger specification
    create_swagger_spec(app)
    print("[OK] Swagger JSON route created")
    
    # Register API blueprints
    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        print("[OK] Auth routes registered")
    except ImportError as e:
        print(f"[WARN] Auth routes import failed: {e}")
        
    try:
        from app.routes.users import users_bp
        app.register_blueprint(users_bp, url_prefix='/api/users')
        print("[OK] User routes registered")
    except ImportError:
        print("[WARN] User routes not yet created - skipping")
        
    try:
        from app.routes.providers import providers_bp
        app.register_blueprint(providers_bp, url_prefix='/api/providers')
        print("[OK] Provider routes registered")
    except ImportError as e:
        print(f"[WARN] Provider routes import failed: {e}")
        
    try:
        from app.routes.services import services_bp
        app.register_blueprint(services_bp, url_prefix='/api/services')
        print("[OK] Services routes registered")
    except ImportError as e:
        print(f"[WARN] Services routes import failed: {e}")

    try:
        from app.routes.bookings import bookings_bp
        app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
        print("[OK] Booking routes registered")
    except ImportError as e:
        print(f"[WARN] Booking routes import failed: {e}")

    try:
        from app.routes.reviews import reviews_bp
        app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
        print("[OK] Review routes registered")
    except ImportError as e:
        print(f"[WARN] Review routes import failed: {e}")

    try:
        from app.routes.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
        print("[OK] Admin routes registered")
    except ImportError as e:
        print(f"[WARN] Admin routes import failed: {e}")
        
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'joblink-backend'}, 200
        
    return app