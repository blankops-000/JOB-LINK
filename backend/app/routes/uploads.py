"""
Upload Routes
Handles image uploads using Cloudinary
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.provider_profile import ProviderProfile
from app.utils.cloudinary_service import CloudinaryService
from app.utils.auth import provider_required

uploads_bp = Blueprint('uploads', __name__)


@uploads_bp.route('/profile-image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    """
    Upload user profile image
    
    Form data:
    - image: Image file (jpg, png, gif, webp)
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Validate file
        is_valid, error_message = CloudinaryService.validate_image_file(file)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Upload to Cloudinary
        result = CloudinaryService.upload_profile_image(file, current_user_id)
        
        if not result:
            return jsonify({'error': 'Failed to upload image'}), 500
        
        # Update user profile with image URL
        user = User.query.get(int(current_user_id))
        if user:
            # Add profile_image_url field to user model if needed
            # For now, just return the URL
            pass
        
        return jsonify({
            'message': 'Profile image uploaded successfully',
            'image_url': result['url'],
            'public_id': result['public_id']
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to upload image', 'details': str(e)}), 500


@uploads_bp.route('/provider/portfolio', methods=['POST'])
@jwt_required()
@provider_required
def upload_portfolio_image():
    """
    Upload provider portfolio image
    
    Form data:
    - image: Image file
    - index: Image index (optional, default 0)
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        index = request.form.get('index', 0)
        
        # Validate file
        is_valid, error_message = CloudinaryService.validate_image_file(file)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Get provider profile
        provider = ProviderProfile.query.filter_by(user_id=int(current_user_id)).first()
        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        # Upload to Cloudinary
        result = CloudinaryService.upload_provider_portfolio_image(file, provider.id, index)
        
        if not result:
            return jsonify({'error': 'Failed to upload image'}), 500
        
        return jsonify({
            'message': 'Portfolio image uploaded successfully',
            'image_url': result['url'],
            'public_id': result['public_id'],
            'index': index
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to upload portfolio image', 'details': str(e)}), 500


@uploads_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_image():
    """
    Delete an image from Cloudinary
    
    Request body:
    {
        "public_id": "joblink/profiles/user_1_profile"
    }
    """
    try:
        data = request.get_json()
        
        if not data.get('public_id'):
            return jsonify({'error': 'public_id is required'}), 400
        
        # Delete from Cloudinary
        success = CloudinaryService.delete_image(data['public_id'])
        
        if success:
            return jsonify({'message': 'Image deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete image'}), 500
            
    except Exception as e:
        return jsonify({'error': 'Failed to delete image', 'details': str(e)}), 500
