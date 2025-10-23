swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "JobLink API",
        "description": "API for JobLink - Local Services Finder",
        "version": "1.0.0",
        "contact": {
            "name": "JobLink Team",
            "email": "support@joblink.com"
        }
    },
    "host": "localhost:5000",
    "basePath": "/api",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}