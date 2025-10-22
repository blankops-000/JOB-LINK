# app/__init__.py
from flask import Flask, jsonify
from .extensions import db, migrate
from .routes.job_routes import job_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yourpassword@localhost/joblink_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    app.register_blueprint(job_bp, url_prefix="/api/jobs")

    # Error handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Server error'}), 500

    return app
