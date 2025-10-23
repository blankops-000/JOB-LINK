from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config.config import Config
from app.utils.errors import APIError, handle_api_error

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    swagger = Swagger(app, config=swagger_config)
    
    # Register error handlers
    app.register_error_handler(APIError, handle_api_error)
    
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