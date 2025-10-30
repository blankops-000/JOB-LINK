import cloudinary
import cloudinary.uploader
import os
from flask import current_app

def configure_cloudinary():
    """Configure Cloudinary with environment variables"""
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET')
    )

def upload_image(file, folder="joblink", public_id=None):
    """Upload image to Cloudinary"""
    try:
        configure_cloudinary()
        
        upload_options = {
            'folder': folder,
            'resource_type': 'image',
            'format': 'jpg',
            'quality': 'auto:good',
            'width': 500,
            'height': 500,
            'crop': 'fill'
        }
        
        if public_id:
            upload_options['public_id'] = public_id
            
        result = cloudinary.uploader.upload(file, **upload_options)
        return {
            'success': True,
            'url': result['secure_url'],
            'public_id': result['public_id']
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def delete_image(public_id):
    """Delete image from Cloudinary"""
    try:
        configure_cloudinary()
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception:
        return False