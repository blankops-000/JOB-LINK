from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # load .env from repo root if present
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)

    app.config.from_object('app.config.Config')

    # initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    cors_origins = app.config.get("CORS_ORIGINS", "")
    origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
    CORS(app, origins=origins or None)

    # register core blueprints
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

    # register optional route blueprints if present
    for module_name, prefix in (("providers", "/api/providers"), ("bookings", "/api/bookings")):
        try:
            mod = __import__(f"app.routes.{module_name}", fromlist=[f"{module_name}_bp"])
            app.register_blueprint(getattr(mod, f"{module_name}_bp"), url_prefix=prefix)
        except Exception:
            pass

    # initialize swagger UI + spec if file is present
    try:
        from app.docs.swagger import init_swagger
        init_swagger(app)
    except Exception:
        pass

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200

    return app
# ...existing code...