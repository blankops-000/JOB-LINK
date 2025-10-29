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
    app.config.from_object('app.config.Config')
      # Register Swagger UI Blueprint
    app.register_blueprint(swaggerui_blueprint)
    
    # Create Swagger specification
    create_swagger_spec(app)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', ['http://localhost:3000'])
        }
    })
    
    with app.app_context():
        try:
            from app.routes.auth import auth_bp
            app.register_blueprint(auth_bp, url_prefix='/api/auth')
        except ImportError:
            print("⚠️  Auth routes not yet created - skipping")
            
        try:
            from app.routes.users import users_bp
            app.register_blueprint(users_bp, url_prefix='/api/users')
        except ImportError:
            print("User routes not yet created - skipping")
        try:
            from app.routes.providers import providers_bp
            app.register_blueprint(providers_bp, url_prefix='/api/providers')
        except ImportError:
            print("Provider routes not yet created - skipping")
            
        try:
            from app.routes.services import services_bp
            app.register_blueprint(services_bp, url_prefix='/api/services')
        except ImportError:
            print("Services routes not yet created - skipping")

        
    
    try:
        from app.routes.bookings import bookings_bp
        app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    except ImportError:
        print("Booking routes not yet created - skipping") 

    try:
        from app.routes.reviews import reviews_bp
        app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    except ImportError:
         print("Review routes not yet created - skipping")

    try:
        from app.routes.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
        print("Admin routes registered successfully")
    except ImportError:
        print("Admin routes not yet created - skipping")
        # Add to imports
    return app