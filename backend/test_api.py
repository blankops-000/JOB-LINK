from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'JobLink API is working!',
        'status': 'success',
        'endpoints': {
            'test_user': '/api/test/user',
            'test_provider': '/api/test/provider'
        }
    })

@app.route('/api/test/user')
def test_user():
    return jsonify({
        'user': {
            'id': 1,
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'client'
        },
        'message': 'User data retrieved successfully'
    })

@app.route('/api/test/provider')
def test_provider():
    return jsonify({
        'provider': {
            'id': 2,
            'email': 'provider@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'provider',
            'business_name': 'Jane\'s Cleaning Service'
        },
        'message': 'Provider data retrieved successfully'
    })

if __name__ == '__main__':
    print("Starting JobLink Test API...")
    print("Server running at: http://localhost:5000")
    app.run(debug=True, port=5000)