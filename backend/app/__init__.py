from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.config')

    # Register blueprints
    from app.routes import auth, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)

    return app

app = create_app()