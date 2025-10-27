from flask import jsonify

class APIError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def validation_error(message):
    return APIError(message, 400)

def not_found_error(resource="Resource"):
    return APIError(f"{resource} not found", 404)

def unauthorized_error():
    return APIError("Unauthorized access", 401)

def forbidden_error():
    return APIError("Forbidden access", 403)

def server_error():
    return APIError("Internal server error", 500)