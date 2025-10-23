# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .routes.jobs import jobs_bp
import os

def create_app():
    app = Flask(__name__)

    # ✅ PostgreSQL connection (update with your credentials)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        "DATABASE_URL",
        "postgresql://username:password@localhost:5432/joblink_db"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(jobs_bp)

    @app.route('/')
    def home():
        return {"message": "Job Link API is running ✅"}

    return app
