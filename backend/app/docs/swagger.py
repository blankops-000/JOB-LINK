# Import Flask and Swagger components
from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI configuration
SWAGGER_URL = '/api/docs'  # URL for accessing Swagger UI
API_URL = '/api/swagger.json'  # URL for serving OpenAPI specification

# Create Swagger UI Blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint
    API_URL,      # OpenAPI specification endpoint
    config={      # Swagger UI configuration
        'app_name': "JobLink API",  # Application name displayed in UI
        'doc_expansion': 'none',    # Collapse all documentation sections by default
        'persistAuthorization': True  # Keep authorization between browser sessions
    }
)

def create_swagger_spec(app):
    """
    Create OpenAPI specification for the JobLink API
    This function generates the swagger.json file dynamically
    """
    
    @app.route(API_URL)
    def swagger_json():
        """Endpoint that serves the OpenAPI specification"""
        # Define OpenAPI specification
        swagger_spec = {
            "openapi": "3.0.0",  # OpenAPI version
            "info": {  # API metadata
                "title": "JobLink API",
                "description": "Service Booking Platform API - Connect clients with service providers",
                "version": "1.0.0",
                "contact": {  # Contact information
                    "name": "JobLink Team",
                    "email": "support@joblink.com"
                },
                "license": {  # License information
                    "name": "MIT",
                    "url": "https://opensource.org/licenses/MIT"
                }
            },
            "servers": [  # API server configurations
                {
                    "url": "http://localhost:5000",  # Development server
                    "description": "Development server"
                },
                {
                    "url": "https://your-production-url.com",  # Production server
                    "description": "Production server"
                }
            ],
            "paths": {  # API endpoints documentation
                "/api/auth/register": {  # Registration endpoint
                    "post": {  # HTTP POST method
                        "summary": "Register a new user",
                        "description": "Create a new user account with client, provider, or admin role",
                        "tags": ["Authentication"],  # Group in Authentication category
                        "requestBody": {  # Request body schema
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {  # Request data structure
                                        "type": "object",
                                        "required": ["email", "password", "first_name", "last_name"],
                                        "properties": {
                                            "email": {
                                                "type": "string",
                                                "format": "email",
                                                "example": "user@example.com"
                                            },
                                            "password": {
                                                "type": "string",
                                                "minLength": 6,
                                                "example": "password123"
                                            },
                                            "first_name": {
                                                "type": "string",
                                                "example": "John"
                                            },
                                            "last_name": {
                                                "type": "string",
                                                "example": "Doe"
                                            },
                                            "phone": {
                                                "type": "string",
                                                "example": "+254712345678"
                                            },
                                            "role": {
                                                "type": "string",
                                                "enum": ["client", "provider", "admin"],
                                                "default": "client"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {  # Possible responses
                            "201": {  # Success response
                                "description": "User created successfully",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "message": "User registered successfully",
                                            "user": {
                                                "id": 1,
                                                "email": "user@example.com",
                                                "first_name": "John",
                                                "last_name": "Doe",
                                                "role": "client"
                                            },
                                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                                        }
                                    }
                                }
                            },
                            "400": {  # Bad request response
                                "description": "Missing required fields or invalid data",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Missing required fields",
                                            "required": ["email", "password", "first_name", "last_name"]
                                        }
                                    }
                                }
                            },
                            "409": {  # Conflict response
                                "description": "User with this email already exists",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "User with this email already exists"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/auth/login": {  # Login endpoint documentation
                    "post": {
                        "summary": "User login",
                        "description": "Authenticate user and return JWT token",
                        "tags": ["Authentication"],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["email", "password"],
                                        "properties": {
                                            "email": {
                                                "type": "string",
                                                "format": "email",
                                                "example": "user@example.com"
                                            },
                                            "password": {
                                                "type": "string",
                                                "example": "password123"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Login successful",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "message": "Login successful",
                                            "user": {
                                                "id": 1,
                                                "email": "user@example.com",
                                                "first_name": "John",
                                                "last_name": "Doe",
                                                "role": "client"
                                            },
                                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "Invalid credentials",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Invalid email or password"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {  # Reusable components
                "securitySchemes": {  # Authentication schemes
                    "BearerAuth": {  # JWT Bearer token authentication
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                },
                "schemas": {  # Data models
                    "User": {  # User model schema
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 1},
                            "email": {"type": "string", "format": "email", "example": "user@example.com"},
                            "first_name": {"type": "string", "example": "John"},
                            "last_name": {"type": "string", "example": "Doe"},
                            "role": {"type": "string", "enum": ["admin", "provider", "client"], "example": "client"},
                            "is_verified": {"type": "boolean", "example": False},
                            "created_at": {"type": "string", "format": "date-time"}
                        }
                    },
                    "Booking": {  # Booking model schema
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "client_id": {"type": "integer"},
                            "provider_id": {"type": "integer"},
                            "scheduled_date": {"type": "string", "format": "date-time"},
                            "duration_hours": {"type": "integer"},
                            "total_amount": {"type": "number", "format": "float"},
                            "status": {"type": "string", "enum": ["pending", "confirmed", "in_progress", "completed", "cancelled"]}
                        }
                    }
                },
                "responses": {  # Reusable responses
                    "Unauthorized": {  # 401 Unauthorized response
                        "description": "Authentication required",
                        "content": {
                            "application/json": {
                                "example": {"error": "Authentication required"}
                            }
                        }
                    },
                    "Forbidden": {  # 403 Forbidden response
                        "description": "Insufficient permissions",
                        "content": {
                            "application/json": {
                                "example": {"error": "Insufficient permissions"}
                            }
                        }
                    },
                    "NotFound": {  # 404 Not Found response
                        "description": "Resource not found", 
                        "content": {
                            "application/json": {
                                "example": {"error": "Resource not found"}
                            }
                        }
                    }
                }
            },
            "security": [  # Default security requirement
                {"BearerAuth": []}  # All endpoints require Bearer token by default
            ]
        }
        
        return jsonify(swagger_spec)