"""
Swagger/OpenAPI documentation for JobLink API
This file creates automatic API documentation that developers can use
to understand all available endpoints, parameters, and responses
"""
from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI configuration
# These URLs define where the Swagger UI will be accessible and where it gets its specification
SWAGGER_URL = '/api/docs'  # The URL where users can access the Swagger UI interface
API_URL = '/api/swagger.json'  # The URL that serves the OpenAPI specification file

# Create Swagger UI Blueprint
# This integrates Swagger UI into your Flask application
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint in your app
    API_URL,      # OpenAPI specification endpoint
    config={      # Swagger UI configuration options
        'app_name': "JobLink API",  # Display name in the Swagger UI
        'doc_expansion': 'none',    # Collapse all documentation sections by default for cleaner view
        'persistAuthorization': True  # Keep JWT tokens between browser sessions
    }
)

def create_swagger_spec(app):
    """
    Create OpenAPI specification for the JobLink API
    This function dynamically generates the swagger.json file that describes your entire API
    """
    
    @app.route(API_URL)
    def swagger_json():
        """
        Endpoint that serves the OpenAPI specification in JSON format
        Swagger UI reads this file to generate the interactive documentation
        """
        # Define the complete OpenAPI specification
        swagger_spec = {
            # OpenAPI version - 3.0.0 is the current standard
            "openapi": "3.0.0",
            
            # API metadata for documentation
            "info": {
                "title": "JobLink API",
                "description": "Service Booking Platform API - Connect clients with service providers\n\n"
                             "## Overview\n"
                             "JobLink is a platform that connects service providers with clients.\n"
                             "Cliens can search for providers, book services, and leave reviews.\n\n"
                             "## Authentication\n"
                             "This API uses JWT (JSON Web Tokens) for authentication.\n"
                             "Register a user first, then use the login endpoint to get a token.\n"
                             "Include the token in the Authorization header as: `Bearer {token}`\n\n"
                             "## User Roles\n"
                             "- **Clients**: Can book services and write reviews\n"
                             "- **Providers**: Can create service profiles and manage bookings\n"
                             "- **Admins**: Can manage users and view platform analytics",
                "version": "1.0.0",
                "contact": {
                    "name": "JobLink Team",
                    "email": "support@joblink.com"
                },
                "license": {
                    "name": "MIT",
                    "url": "https://opensource.org/licenses/MIT"
                }
            },
            
            # Server configurations - where the API is hosted
            "servers": [
                {
                    "url": "http://localhost:5000",
                    "description": "Development server"
                },
                {
                    "url": "https://your-production-url.com",
                    "description": "Production server"
                }
            ],
            
            # API endpoints documentation - this is the core of the specification
            "paths": {
                # Authentication endpoints
                "/api/auth/register": {
                    "post": {
                        "summary": "Register a new user",
                        "description": "Create a new user account with client, provider, or admin role",
                        "tags": ["Authentication"],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["email", "password", "first_name", "last_name"],
                                        "properties": {
                                            "email": {
                                                "type": "string",
                                                "format": "email",
                                                "example": "user@example.com",
                                                "description": "User's email address (must be unique)"
                                            },
                                            "password": {
                                                "type": "string",
                                                "minLength": 6,
                                                "example": "password123",
                                                "description": "User's password (min 6 characters)"
                                            },
                                            "first_name": {
                                                "type": "string",
                                                "example": "John",
                                                "description": "User's first name"
                                            },
                                            "last_name": {
                                                "type": "string", 
                                                "example": "Doe",
                                                "description": "User's last name"
                                            },
                                            "phone": {
                                                "type": "string",
                                                "example": "+254712345678",
                                                "description": "User's phone number (optional)"
                                            },
                                            "role": {
                                                "type": "string",
                                                "enum": ["client", "provider", "admin"],
                                                "default": "client",
                                                "description": "User role - determines permissions"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "201": {
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
                                                "role": "client",
                                                "is_verified": False,
                                                "created_at": "2024-01-01T00:00:00Z"
                                            },
                                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                                        }
                                    }
                                }
                            },
                            "400": {
                                "description": "Bad Request - Missing required fields or invalid data",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Missing required fields",
                                            "required": ["email", "password", "first_name", "last_name"]
                                        }
                                    }
                                }
                            },
                            "409": {
                                "description": "Conflict - User with this email already exists",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "User with this email already exists"
                                        }
                                    }
                                }
                            },
                            "500": {
                                "description": "Internal Server Error",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Registration failed",
                                            "details": "Database connection error"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                
                "/api/auth/login": {
                    "post": {
                        "summary": "User login",
                        "description": "Authenticate user and return JWT token for accessing protected endpoints",
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
                            "400": {
                                "description": "Bad Request - Missing email or password",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Email and password required"
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "Unauthorized - Invalid credentials",
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
                },
                
                "/api/auth/me": {
                    "get": {
                        "summary": "Get current user profile",
                        "description": "Get the profile of the currently authenticated user",
                        "tags": ["Authentication"],
                        "security": [{"BearerAuth": []}],
                        "responses": {
                            "200": {
                                "description": "User profile retrieved successfully",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "user": {
                                                "id": 1,
                                                "email": "user@example.com",
                                                "first_name": "John",
                                                "last_name": "Doe",
                                                "role": "client",
                                                "is_verified": False,
                                                "created_at": "2024-01-01T00:00:00Z"
                                            }
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "Unauthorized - Missing or invalid token",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "msg": "Missing Authorization Header"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                
                # Providers endpoints
                "/api/providers": {
                    "get": {
                        "summary": "Get all providers",
                        "description": "Get a paginated list of service providers with optional filtering",
                        "tags": ["Providers"],
                        "parameters": [
                            {
                                "name": "page",
                                "in": "query",
                                "required": False,
                                "schema": {"type": "integer", "default": 1},
                                "description": "Page number for pagination"
                            },
                            {
                                "name": "per_page", 
                                "in": "query",
                                "required": False,
                                "schema": {"type": "integer", "default": 10},
                                "description": "Number of items per page"
                            },
                            {
                                "name": "search",
                                "in": "query", 
                                "required": False,
                                "schema": {"type": "string"},
                                "description": "Search in business names and descriptions"
                            },
                            {
                                "name": "service_category_id",
                                "in": "query",
                                "required": False,
                                "schema": {"type": "integer"},
                                "description": "Filter by service category ID"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Providers retrieved successfully",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "providers": [
                                                {
                                                    "id": 1,
                                                    "business_name": "Expert Plumbing",
                                                    "description": "Professional plumbing services",
                                                    "hourly_rate": 25.50,
                                                    "is_available": True,
                                                    "user": {
                                                        "first_name": "Jane",
                                                        "last_name": "Smith"
                                                    }
                                                }
                                            ],
                                            "pagination": {
                                                "page": 1,
                                                "per_page": 10,
                                                "total": 50,
                                                "pages": 5
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "summary": "Create provider profile",
                        "description": "Create a service provider profile (provider role required)",
                        "tags": ["Providers"],
                        "security": [{"BearerAuth": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["business_name", "hourly_rate", "service_category_id"],
                                        "properties": {
                                            "business_name": {
                                                "type": "string",
                                                "example": "Expert Plumbing Services",
                                                "description": "Name of the business"
                                            },
                                            "description": {
                                                "type": "string",
                                                "example": "Professional plumbing and pipe services",
                                                "description": "Business description"
                                            },
                                            "hourly_rate": {
                                                "type": "number",
                                                "format": "float", 
                                                "example": 25.50,
                                                "description": "Hourly rate in local currency"
                                            },
                                            "service_category_id": {
                                                "type": "integer",
                                                "example": 1,
                                                "description": "ID of the service category"
                                            },
                                            "experience_years": {
                                                "type": "integer",
                                                "example": 5,
                                                "description": "Years of experience (optional)"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Provider profile created successfully",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "message": "Provider profile created successfully",
                                            "provider": {
                                                "id": 1,
                                                "business_name": "Expert Plumbing Services",
                                                "hourly_rate": 25.50,
                                                "is_available": True
                                            }
                                        }
                                    }
                                }
                            },
                            "403": {
                                "description": "Forbidden - User is not a provider",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "error": "Insufficient permissions"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                
                # Services endpoints
                "/api/services": {
                    "get": {
                        "summary": "Get all service categories",
                        "description": "Get paginated list of service categories with search",
                        "tags": ["Services"],
                        "parameters": [
                            {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}},
                            {"name": "per_page", "in": "query", "schema": {"type": "integer", "default": 10}},
                            {"name": "search", "in": "query", "schema": {"type": "string"}}
                        ],
                        "responses": {
                            "200": {
                                "description": "Services retrieved successfully",
                                "content": {"application/json": {"example": {"services": [], "pagination": {}}}}
                            }
                        }
                    },
                    "post": {
                        "summary": "Create service category",
                        "description": "Create new service category (admin only)",
                        "tags": ["Services"],
                        "security": [{"BearerAuth": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["name"],
                                        "properties": {
                                            "name": {"type": "string", "example": "Plumbing"},
                                            "description": {"type": "string", "example": "Professional plumbing services"}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"201": {"description": "Service created successfully"}}
                    }
                },
                
                # Bookings endpoints
                "/api/bookings": {
                    "get": {
                        "summary": "Get user bookings",
                        "description": "Get bookings for current user (client sees their bookings, provider sees bookings for them)",
                        "tags": ["Bookings"],
                        "security": [{"BearerAuth": []}],
                        "parameters": [
                            {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}},
                            {"name": "status", "in": "query", "schema": {"type": "string", "enum": ["pending", "confirmed", "in_progress", "completed", "cancelled"]}}
                        ],
                        "responses": {
                            "200": {"description": "Bookings retrieved successfully"}
                        }
                    },
                    "post": {
                        "summary": "Create a new booking",
                        "description": "Create a service booking (client role required)",
                        "tags": ["Bookings"],
                        "security": [{"BearerAuth": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["provider_id", "service_category_id", "scheduled_date", "duration_hours", "address"],
                                        "properties": {
                                            "provider_id": {"type": "integer", "example": 2},
                                            "service_category_id": {"type": "integer", "example": 1},
                                            "scheduled_date": {"type": "string", "format": "date-time", "example": "2024-12-25T10:00:00Z"},
                                            "duration_hours": {"type": "integer", "example": 2},
                                            "address": {"type": "string", "example": "123 Main Street, Nairobi"},
                                            "special_requests": {"type": "string", "example": "Please bring tools"}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"201": {"description": "Booking created successfully"}}
                    }
                },
                
                "/api/bookings/{booking_id}": {
                    "get": {
                        "summary": "Get booking details",
                        "tags": ["Bookings"],
                        "security": [{"BearerAuth": []}],
                        "parameters": [{"name": "booking_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                        "responses": {"200": {"description": "Booking details retrieved"}}
                    },
                    "put": {
                        "summary": "Update booking status",
                        "tags": ["Bookings"],
                        "security": [{"BearerAuth": []}],
                        "parameters": [{"name": "booking_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string", "enum": ["confirmed", "in_progress", "completed", "cancelled"]}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "Booking updated successfully"}}
                    }
                },
                
                # Reviews endpoints
                "/api/reviews": {
                    "post": {
                        "summary": "Create a review",
                        "description": "Create review for completed booking (client only)",
                        "tags": ["Reviews"],
                        "security": [{"BearerAuth": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["booking_id", "rating"],
                                        "properties": {
                                            "booking_id": {"type": "integer", "example": 1},
                                            "rating": {"type": "integer", "minimum": 1, "maximum": 5, "example": 5},
                                            "comment": {"type": "string", "example": "Excellent service!"}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"201": {"description": "Review created successfully"}}
                    }
                },
                
                "/api/reviews/provider/{provider_id}": {
                    "get": {
                        "summary": "Get provider reviews",
                        "tags": ["Reviews"],
                        "parameters": [
                            {"name": "provider_id", "in": "path", "required": True, "schema": {"type": "integer"}},
                            {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}}
                        ],
                        "responses": {"200": {"description": "Reviews retrieved successfully"}}
                    }
                },
                
                # Admin endpoints
                "/api/admin/stats": {
                    "get": {
                        "summary": "Get platform statistics",
                        "description": "Get comprehensive platform analytics (admin only)",
                        "tags": ["Admin"],
                        "security": [{"BearerAuth": []}],
                        "responses": {
                            "200": {
                                "description": "Statistics retrieved successfully",
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "users": {"total": 150, "clients": 120, "providers": 25, "admins": 5},
                                            "bookings": {"total": 89, "pending": 12, "completed": 67},
                                            "revenue": {"total": 15420.50, "this_month": 3240.75}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                
                "/api/admin/users": {
                    "get": {
                        "summary": "Get all users",
                        "description": "Get paginated list of all users (admin only)",
                        "tags": ["Admin"],
                        "security": [{"BearerAuth": []}],
                        "parameters": [
                            {"name": "page", "in": "query", "schema": {"type": "integer", "default": 1}},
                            {"name": "role", "in": "query", "schema": {"type": "string", "enum": ["client", "provider", "admin"]}}
                        ],
                        "responses": {"200": {"description": "Users retrieved successfully"}}
                    }
                },
                
                "/api/admin/users/{user_id}": {
                    "put": {
                        "summary": "Update user",
                        "description": "Update user details (admin only)",
                        "tags": ["Admin"],
                        "security": [{"BearerAuth": []}],
                        "parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "first_name": {"type": "string"},
                                            "last_name": {"type": "string"},
                                            "is_verified": {"type": "boolean"}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "User updated successfully"}}
                    },
                    "delete": {
                        "summary": "Delete user",
                        "description": "Delete user account (admin only)",
                        "tags": ["Admin"],
                        "security": [{"BearerAuth": []}],
                        "parameters": [{"name": "user_id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                        "responses": {"200": {"description": "User deleted successfully"}}
                    }
                }
            },
            
            # Reusable components that can be referenced throughout the specification
            "components": {
                # Authentication schemes
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "description": "JWT token obtained from login endpoint"
                    }
                },
                
                # Data models/schemas
                "schemas": {
                    "User": {
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
                    "Provider": {
                        "type": "object", 
                        "properties": {
                            "id": {"type": "integer"},
                            "business_name": {"type": "string"},
                            "description": {"type": "string"},
                            "hourly_rate": {"type": "number", "format": "float"},
                            "is_available": {"type": "boolean"},
                            "experience_years": {"type": "integer"}
                        }
                    },
                    "Booking": {
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
                
                # Reusable response definitions
                "responses": {
                    "Unauthorized": {
                        "description": "Authentication required",
                        "content": {
                            "application/json": {
                                "example": {"error": "Authentication required"}
                            }
                        }
                    },
                    "Forbidden": {
                        "description": "Insufficient permissions", 
                        "content": {
                            "application/json": {
                                "example": {"error": "Insufficient permissions"}
                            }
                        }
                    },
                    "NotFound": {
                        "description": "Resource not found",
                        "content": {
                            "application/json": {
                                "example": {"error": "Resource not found"}
                            }
                        }
                    },
                    "ValidationError": {
                        "description": "Validation failed",
                        "content": {
                            "application/json": {
                                "example": {"error": "Validation failed", "details": {}}
                            }
                        }
                    }
                }
            },
            
            # Tags for organizing endpoints in Swagger UI
            "tags": [
                {"name": "Authentication", "description": "User authentication and profile management"},
                {"name": "Services", "description": "Service category management"},
                {"name": "Providers", "description": "Service provider profiles and search"},
                {"name": "Bookings", "description": "Service booking management"},
                {"name": "Reviews", "description": "Rating and review system"},
                {"name": "Admin", "description": "Administrative functions and analytics"}
            ]
        }
        
        return jsonify(swagger_spec)

# You can add more functions here to generate dynamic documentation
# based on your actual route definitions if needed