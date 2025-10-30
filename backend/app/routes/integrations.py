from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.cloudinary_service import upload_image
from app.utils.email_service import send_email

integrations_bp = Blueprint('integrations', __name__)

@integrations_bp.route('/test-cloudinary', methods=['POST'])
@jwt_required()
def test_cloudinary():
    """Test Cloudinary image upload"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        result = upload_image(file, folder="joblink/test")
        
        if result['success']:
            return jsonify({
                'message': 'Image uploaded successfully',
                'url': result['url'],
                'public_id': result['public_id']
            }), 200
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@integrations_bp.route('/test-email', methods=['POST'])
@jwt_required()
def test_email():
    """Test SendGrid email sending"""
    try:
        data = request.get_json()
        
        if not data or not data.get('to_email'):
            return jsonify({'error': 'to_email is required'}), 400
        
        result = send_email(
            to_email=data['to_email'],
            subject=data.get('subject', 'Test Email from JobLink'),
            html_content=data.get('content', '<h1>Test Email</h1><p>This is a test email from JobLink API.</p>')
        )
        
        if result['success']:
            return jsonify({
                'message': 'Email sent successfully',
                'status_code': result['status_code']
            }), 200
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500