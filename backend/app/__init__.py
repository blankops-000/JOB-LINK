from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Fixed: flask_sqlalchemy not flask.sqlalchemy
from flask_bcrypt import Bcrypt          # Fixed: flask_bcrypt not flask.bcrypt
from flask_jwt_extended import JWTManager  # Fixed: flask_jwt_extended (correct spelling)
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()  # Fixed: JWTManager not JMTManager
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    return app