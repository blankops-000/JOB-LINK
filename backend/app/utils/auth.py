from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(required_roles):
    """
    Decorator for requiring specific roles
    Usage: @role_required(['admin']) or @role_required(['admin', 'provider'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in required_roles:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Required roles: {required_roles}'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Specific role decorators
def admin_required(f):
    return role_required(['admin'])(f)

def provider_required(f):
    return role_required(['provider', 'admin'])(f)

def client_required(f):
    return role_required(['client', 'admin'])(f)