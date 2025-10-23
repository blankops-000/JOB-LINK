# ...existing code...
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def _normalize_roles(required_roles):
    if isinstance(required_roles, str):
        return [required_roles]
    return list(required_roles or [])

def role_required(required_roles):
    """
    Decorator for requiring specific roles
    Usage: @role_required('admin') or @role_required(['admin', 'provider'])
    """
    allowed = _normalize_roles(required_roles)
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # will raise a proper error if no/invalid token
            verify_jwt_in_request()
            claims = get_jwt() or {}
            user_role = claims.get('role')

            if not user_role or user_role not in allowed:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'Required roles: {allowed}'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Specific role decorators
def admin_required(f):
    return role_required('admin')(f)

def provider_required(f):
    return role_required(['provider', 'admin'])(f)

def client_required(f):
    return role_required(['client', 'admin'])(f)
# ...existing code...