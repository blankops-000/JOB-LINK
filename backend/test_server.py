from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'JobLink API is running!',
        'status': 'success',
        'version': '1.0.0'
    })

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        'message': 'Test endpoint working',
        'status': 'success'
    })

@app.route('/api/test', methods=['POST'])
def test_post():
    data = request.get_json()
    return jsonify({
        'message': 'POST request received!',
        'status': 'success',
        'received_data': data
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email') if data else None
    password = data.get('password') if data else None
    
    # Debug info
    print(f"Received data: {data}")
    print(f"Email: '{email}'")
    print(f"Password: '{password}'")
    
    if email == 'test@example.com' and password == 'password123':
        return jsonify({
            'message': 'Login successful!',
            'status': 'success',
            'token': 'fake-jwt-token-123'
        })
    else:
        return jsonify({
            'message': 'Invalid credentials',
            'status': 'error',
            'debug': {
                'received_email': email,
                'received_password': password,
                'expected_email': 'test@example.com',
                'expected_password': 'password123'
            }
        }), 401

@app.route('/api/profile', methods=['GET'])
def profile():
    auth_header = request.headers.get('Authorization')
    if auth_header == 'Bearer fake-jwt-token-123':
        return jsonify({
            'message': 'Profile data',
            'status': 'success',
            'user': {
                'name': 'John Doe',
                'email': 'test@example.com',
                'role': 'customer'
            }
        })
    else:
        return jsonify({
            'message': 'Unauthorized - Invalid token',
            'status': 'error'
        }), 401

if __name__ == '__main__':
    print("Server starting at http://localhost:5000")
    app.run(debug=True, port=5000)