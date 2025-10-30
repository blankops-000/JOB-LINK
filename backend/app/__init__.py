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
    
    # Add JWT claims loader to include user role in token
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        from app.models.user import User
        # Convert identity back to int for database query
        user = User.query.get(int(identity))
        if user:
            return {'role': user.role.value}
        return {'role': None}
    
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
            print("⚠️  User routes not yet created - skipping")
        try:
            from app.routes.providers import providers_bp
            app.register_blueprint(providers_bp, url_prefix='/api/providers')
        except ImportError:
            print("⚠️  Provider routes not yet created - skipping")

        
    
    try:
        from app.routes.bookings import bookings_bp
        app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    except ImportError:
        print("⚠️  Booking routes not yet created - skipping") 

    try:
        from app.routes.reviews import reviews_bp
        app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    except ImportError:
         print("⚠️  Review routes not yet created - skipping")

    try:
        from app.routes.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
    except ImportError:
        print("⚠️  Admin routes not yet created - skipping")
    
    try:
        from app.routes.payments import payments_bp
        app.register_blueprint(payments_bp, url_prefix='/api/payments')
    except ImportError:
        print("⚠️  Payment routes not yet created - skipping")
    
    try:
        from app.routes.uploads import uploads_bp
        app.register_blueprint(uploads_bp, url_prefix='/api/uploads')
    except ImportError:
        print("⚠️  Upload routes not yet created - skipping")
    
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'joblink-backend'}, 200
    
    return app