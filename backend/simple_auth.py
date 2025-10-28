from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_joblink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Simple User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='client')

@app.route('/')
def home():
    return jsonify({'message': 'JobLink Simple Auth API', 'status': 'working'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        first_name=data['first_name'],
        last_name=data['last_name'],
        role=data.get('role', 'client').lower()
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'access_token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'message': 'Token missing'}), 401
    
    try:
        token = token.split(' ')[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(data['user_id'])
        
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        })
    except:
        return jsonify({'message': 'Invalid token'}), 401

# Service Category Model
class ServiceCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/api/services', methods=['GET', 'POST'])
def services():
    """Handle both GET and POST for services"""
    if request.method == 'GET':
        # GET: List all service categories
        search = request.args.get('search', '')
        
        query = ServiceCategory.query
        if search:
            query = query.filter(ServiceCategory.name.ilike(f'%{search}%'))
        
        services = query.all()
        
        return jsonify({
            'services': [{
                'id': s.id,
                'name': s.name,
                'description': s.description,
                'created_at': s.created_at.isoformat()
            } for s in services],
            'total': len(services),
            'message': 'Services retrieved successfully'
        })
    
    elif request.method == 'POST':
        # POST: Create new service category
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Token required'}), 401
        
        try:
            token = token.split(' ')[1]
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid token'}), 401
        
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'message': 'Service name is required'}), 400
        
        existing = ServiceCategory.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'message': 'Service already exists'}), 409
        
        service = ServiceCategory(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'message': 'Service created successfully',
            'service': {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'created_at': service.created_at.isoformat()
            }
        }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Add sample services if none exist
        if ServiceCategory.query.count() == 0:
            services = [
                {'name': 'Plumbing', 'description': 'Water pipe repairs and installations'},
                {'name': 'Cleaning', 'description': 'House and office cleaning services'},
                {'name': 'Electrical', 'description': 'Electrical repairs and installations'},
                {'name': 'Tutoring', 'description': 'Academic tutoring services'},
                {'name': 'Cooking', 'description': 'Personal chef and meal prep services'}
            ]
            
            for service_data in services:
                service = ServiceCategory(
                    name=service_data['name'],
                    description=service_data['description']
                )
                db.session.add(service)
            
            db.session.commit()
            print("Sample services added!")
    
    print("Simple JobLink Auth API running at http://localhost:5000")
    app.run(debug=True, port=5000)