"""
Cloudinary Image Upload Service
Handles image uploads for user profiles and provider portfolios
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import current_app
from werkzeug.utils import secure_filename
import os


class CloudinaryService:
    """Service for handling image uploads to Cloudinary"""
    
    @staticmethod
    def configure():
        """Configure Cloudinary with credentials from app config"""
        try:
            cloud_name = current_app.config.get('CLOUDINARY_CLOUD_NAME')
            api_key = current_app.config.get('CLOUDINARY_API_KEY')
            api_secret = current_app.config.get('CLOUDINARY_API_SECRET')
            
            if not all([cloud_name, api_key, api_secret]):
                current_app.logger.warning("Cloudinary credentials not fully configured")
                return False
            
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True
            )
            return True
        except Exception as e:
            current_app.logger.error(f"Cloudinary configuration failed: {str(e)}")
            return False
    
    @staticmethod
    def upload_image(file, folder="joblink", public_id=None, transformation=None):
        """
        Upload an image to Cloudinary
        
        Args:
            file: File object or file path
            folder (str): Cloudinary folder to store the image
            public_id (str, optional): Custom public ID for the image
            transformation (dict, optional): Image transformation options
            
        Returns:
            dict: Upload result with URL and public_id, or None if failed
        """
        try:
            if not CloudinaryService.configure():
                return None
            
            upload_options = {
                'folder': folder,
                'resource_type': 'image',
                'overwrite': True
            }
            
            if public_id:
                upload_options['public_id'] = public_id
            
            if transformation:
                upload_options['transformation'] = transformation
            
            # Upload the file
            result = cloudinary.uploader.upload(file, **upload_options)
            
            return {
                'url': result.get('secure_url'),
                'public_id': result.get('public_id'),
                'width': result.get('width'),
                'height': result.get('height'),
                'format': result.get('format'),
                'resource_type': result.get('resource_type')
            }
            
        except Exception as e:
            current_app.logger.error(f"Image upload failed: {str(e)}")
            return None
    
    @staticmethod
    def upload_profile_image(file, user_id):
        """
        Upload user profile image with automatic optimization
        
        Args:
            file: File object
            user_id: User ID for naming
            
        Returns:
            dict: Upload result or None
        """
        transformation = {
            'width': 400,
            'height': 400,
            'crop': 'fill',
            'gravity': 'face',
            'quality': 'auto',
            'fetch_format': 'auto'
        }
        
        public_id = f"user_{user_id}_profile"
        
        return CloudinaryService.upload_image(
            file,
            folder='joblink/profiles',
            public_id=public_id,
            transformation=transformation
        )
    
    @staticmethod
    def upload_provider_portfolio_image(file, provider_id, index=0):
        """
        Upload provider portfolio image
        
        Args:
            file: File object
            provider_id: Provider ID
            index: Image index in portfolio
            
        Returns:
            dict: Upload result or None
        """
        transformation = {
            'width': 800,
            'height': 600,
            'crop': 'limit',
            'quality': 'auto',
            'fetch_format': 'auto'
        }
        
        public_id = f"provider_{provider_id}_portfolio_{index}"
        
        return CloudinaryService.upload_image(
            file,
            folder='joblink/portfolios',
            public_id=public_id,
            transformation=transformation
        )
    
    @staticmethod
    def delete_image(public_id):
        """
        Delete an image from Cloudinary
        
        Args:
            public_id (str): Public ID of the image to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            if not CloudinaryService.configure():
                return False
            
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
            
        except Exception as e:
            current_app.logger.error(f"Image deletion failed: {str(e)}")
            return False
    
    @staticmethod
    def get_image_url(public_id, transformation=None):
        """
        Get Cloudinary URL for an image with optional transformations
        
        Args:
            public_id (str): Public ID of the image
            transformation (dict, optional): Transformation options
            
        Returns:
            str: Image URL or None
        """
        try:
            if not CloudinaryService.configure():
                return None
            
            if transformation:
                url, options = cloudinary.utils.cloudinary_url(
                    public_id,
                    transformation=transformation,
                    secure=True
                )
            else:
                url, options = cloudinary.utils.cloudinary_url(
                    public_id,
                    secure=True
                )
            
            return url
            
        except Exception as e:
            current_app.logger.error(f"Failed to get image URL: {str(e)}")
            return None
    
    @staticmethod
    def validate_image_file(file):
        """
        Validate uploaded image file
        
        Args:
            file: File object
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not file:
            return False, "No file provided"
        
        if file.filename == '':
            return False, "No file selected"
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = secure_filename(file.filename)
        
        if '.' not in filename:
            return False, "File has no extension"
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in allowed_extensions:
            return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        
        # Check file size (max 5MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        max_size = 5 * 1024 * 1024  # 5MB
        if file_size > max_size:
            return False, "File size exceeds 5MB limit"
        
        return True, None
