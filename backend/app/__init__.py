
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# initialize extensions (module-level so models/routes can import them)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    """Application factory"""
    # load .env from repo root if present (so app.config can read env vars)
    root_env = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(root_env):
        load_dotenv(root_env)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.Config')

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # configure CORS using CORS_ORIGINS (comma separated) or allow all if empty
    cors_origins = app.config.get("CORS_ORIGINS", "")
    origins = [o.strip() for o in (cors_origins or "").split(",") if o.strip()]
    CORS(app, origins=origins or None)

    # register blueprints safely (missing route modules won't break app)
    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
    except Exception:
        pass

    try:
        from app.routes.users import users_bp
        app.register_blueprint(users_bp, url_prefix='/api/users')
    except Exception:
        pass

    for module_name, prefix in (("providers", "/api/providers"), ("bookings", "/api/bookings")):
        try:
            mod = __import__(f"app.routes.{module_name}", fromlist=[f"{module_name}_bp"])
            bp = getattr(mod, f"{module_name}_bp")
            app.register_blueprint(bp, url_prefix=prefix)
        except Exception:
            pass

    # optional docs swagger init (if present)
    try:
        from app.docs.swagger import init_swagger
        init_swagger(app)
    except Exception:
        pass

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200

    return app
