from flask_swagger_ui import get_swaggerui_blueprint
from flask import jsonify

SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "JobLink API",
        'doc_expansion': 'none',
        'persistAuthorization': True
    }
)

def create_swagger_spec(app):
    @app.route(API_URL)
    def swagger_json():
        return jsonify({
            "openapi": "3.0.0",
            "info": {
                "title": "JobLink API",
                "description": "Service Booking Platform API",
                "version": "1.0.0",
                "contact": {
                    "name": "JobLink Team",
                    "email": "support@joblink.com"
                }
            },
            "servers": [
                {
                    "url": "http://localhost:5000",
                    "description": "Development server"
                }
            ],
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                },
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "email": {"type": "string"},
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "role": {"type": "string", "enum": ["admin", "provider", "client"]}
                        }
                    }
                }
            },
            "security": [{"BearerAuth": []}]
        })