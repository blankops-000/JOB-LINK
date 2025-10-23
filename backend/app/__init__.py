from flask import Flask, jsonify
from flask_cors import CORS
from .extensions import db, migrate
from .config import Config

# Import your blueprints
from .routes.auth import auth_bp
from .routes.jobs import jobs_bp
from .routes.providers import providers_bp
from .routes.bookings import bookings_bp
from .routes.reviews import reviews_bp
from .routes.payments import payments_bp
from .routes.notifications import notifications_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend requests
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
    app.register_blueprint(providers_bp, url_prefix="/api/providers")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")
    app.register_blueprint(reviews_bp, url_prefix="/api/reviews")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")

    # Basic route
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to Job-Link API"}), 200

    # ---------- Error Handling ----------
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app
