from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
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
            print("⚠️  User routes not yet created - skipping")
    
    return app