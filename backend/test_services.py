from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for testing
services = [
    {'id': 1, 'name': 'Plumbing', 'description': 'Water pipe repairs'},
    {'id': 2, 'name': 'Cleaning', 'description': 'House cleaning services'},
    {'id': 3, 'name': 'Electrical', 'description': 'Electrical repairs'}
]

@app.route('/')
def home():
    return jsonify({'message': 'Services API Test Server', 'status': 'running'})

@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify({
        'services': services,
        'total': len(services),
        'message': 'Services retrieved successfully'
    })

@app.route('/api/services', methods=['POST'])
def create_service():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'message': 'Service name is required'}), 400
    
    # Check if exists
    for service in services:
        if service['name'].lower() == data['name'].lower():
            return jsonify({'message': 'Service already exists'}), 409
    
    # Create new service
    new_service = {
        'id': len(services) + 1,
        'name': data['name'],
        'description': data.get('description', '')
    }
    
    services.append(new_service)
    
    return jsonify({
        'message': 'Service created successfully',
        'service': new_service
    }), 201

if __name__ == '__main__':
    print("Services Test API running at http://localhost:5000")
    print("Test endpoints:")
    print("GET  http://localhost:5000/api/services")
    print("POST http://localhost:5000/api/services")
    app.run(debug=True, port=5000)