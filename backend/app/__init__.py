from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.test import test_bp
    from app.routes.auth import auth_bp
    from app.routes.services import services_bp
    from app.routes.bookings import bookings_bp
    
    app.register_blueprint(test_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    
    return app