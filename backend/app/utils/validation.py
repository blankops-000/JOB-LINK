from functools import wraps
from flask import request
from app.utils.errors import validation_error

def validate_json(required_fields=None):
    """Decorator to validate JSON request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                raise validation_error("Content-Type must be application/json")
            
            data = request.get_json()
            if not data:
                raise validation_error("No JSON data provided")
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    raise validation_error(f"Missing required fields: {', '.join(missing_fields)}")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_pagination():
    """Validate pagination parameters"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if page < 1:
        raise validation_error("Page must be >= 1")
    
    if per_page < 1 or per_page > 100:
        raise validation_error("Per page must be between 1 and 100")
    
    return page, per_page

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None