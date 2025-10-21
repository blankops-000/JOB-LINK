from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'JobLink Backend is running!',
        'status': 'success',
        'version': '1.0.0',
        'endpoints': {
            'test': '/',
            'auth': '/api/auth/test',
            'services': '/api/services/test',
            'bookings': '/api/bookings/test'
        }
    })

@app.route('/api/auth/test')
def auth_test():
    return jsonify({'message': 'Auth endpoint working', 'status': 'success'})

@app.route('/api/services/test')
def services_test():
    return jsonify({'message': 'Services endpoint working', 'status': 'success'})

@app.route('/api/bookings/test')
def bookings_test():
    return jsonify({'message': 'Bookings endpoint working', 'status': 'success'})

if __name__ == '__main__':
    print("Starting JobLink Backend Server...")
    print("Server running at: http://localhost:5000")
    print("Open your browser and visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)