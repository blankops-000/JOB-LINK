from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.utils.errors import forbidden_error, unauthorized_error

def require_role(*allowed_roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            if not current_user_id:
                raise unauthorized_error()
            
            user = User.query.get(current_user_id)
            if not user:
                raise unauthorized_error()
            
            if user.role not in allowed_roles:
                raise forbidden_error()
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin(f):
    """Decorator to require admin role"""
    return require_role('admin')(f)

def require_provider(f):
    """Decorator to require provider role"""
    return require_role('provider')(f)

def require_customer(f):
    """Decorator to require customer role"""
    return require_role('customer')(f)

def require_provider_or_admin(f):
    """Decorator to require provider or admin role"""
    return require_role('provider', 'admin')(f)