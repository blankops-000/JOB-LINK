from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(required_roles):
    """
    Decorator to require specific user roles for route access
    Usage: @role_required(['admin']) or @role_required(['admin', 'provider'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verify JWT token is present and valid
            verify_jwt_in_request()
            # Get claims from the JWT token
            claims = get_jwt()
            user_role = claims.get('role')
            
            # Check if user has required role
            if user_role not in required_roles:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Required roles: {required_roles}, Your role: {user_role}'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Specific role decorators for convenience
def admin_required(f):
    return role_required(['admin'])(f)

def provider_required(f):
    return role_required(['provider', 'admin'])(f)

def client_required(f):
    return role_required(['client', 'admin'])(f)