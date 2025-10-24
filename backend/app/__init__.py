from .routes.provider import provider_bp
from .routes.bookings import bookings_bp
from .routes.reviews import reviews_bp
from .routes.payments import payments_bp
from .routes.service_categories import service_bp

app.register_blueprint(provider_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(service_bp)
