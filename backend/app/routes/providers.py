from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app import db
from app.models.provider_profile import ProviderProfile
from app.models.service_category import ServiceCategory
from app.models.user import User, RoleEnum
from app.utils.auth import admin_required, provider_required
from app.utils.cloudinary_service import upload_image, delete_image
from app.utils.geo_service import calculate_distance, get_coordinates_from_address

providers_bp = Blueprint('providers', __name__)

@providers_bp.route('', methods=['POST'])
@jwt_required()
@provider_required
def create_provider_profile():
    """Create or update provider profile (for providers only)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['business_name', 'hourly_rate', 'service_category_id']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        # Check if user already has a provider profile
        existing_profile = ProviderProfile.query.filter_by(user_id=current_user_id).first()
        if existing_profile:
            return jsonify({'error': 'Provider profile already exists for this user'}), 400
        
        # Check if service category exists
        service_category = ServiceCategory.query.get(data['service_category_id'])
        if not service_category:
            return jsonify({'error': 'Service category not found'}), 404
        
        # Create provider profile
        provider_profile = ProviderProfile(
            user_id=current_user_id,
            business_name=data['business_name'],
            description=data.get('description', ''),
            hourly_rate=data['hourly_rate'],
            service_category_id=data['service_category_id'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            experience_years=data.get('experience_years', 0)
        )
        
        db.session.add(provider_profile)
        db.session.commit()
        
        return jsonify({
            'message': 'Provider profile created successfully',
            'provider': provider_profile.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create provider profile', 'details': str(e)}), 500

@providers_bp.route('', methods=['GET'])
def get_providers():
    """Get all providers with filtering and pagination"""
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filter parameters
        service_category_id = request.args.get('service_category_id', type=int)
        search_query = request.args.get('search', '')
        min_rate = request.args.get('min_rate', type=float)
        max_rate = request.args.get('max_rate', type=float)
        is_available = request.args.get('is_available', type=bool)
        
        # Geo-location parameters
        user_lat = request.args.get('latitude', type=float)
        user_lon = request.args.get('longitude', type=float)
        max_distance = request.args.get('max_distance', 50, type=float)  # Default 50km
        address = request.args.get('address')
        
        # Base query
        query = ProviderProfile.query.filter_by(is_available=True)
        
        # Apply filters
        if service_category_id:
            query = query.filter_by(service_category_id=service_category_id)
        
        if search_query:
            query = query.join(User).filter(
                or_(
                    ProviderProfile.business_name.ilike(f'%{search_query}%'),
                    ProviderProfile.description.ilike(f'%{search_query}%'),
                    User.first_name.ilike(f'%{search_query}%'),
                    User.last_name.ilike(f'%{search_query}%')
                )
            )
        
        if min_rate is not None:
            query = query.filter(ProviderProfile.hourly_rate >= min_rate)
        
        if max_rate is not None:
            query = query.filter(ProviderProfile.hourly_rate <= max_rate)
        
        if is_available is not None:
            query = query.filter(ProviderProfile.is_available == is_available)
        
        # Execute query with pagination
        providers = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Get coordinates from address if provided
        if address and not (user_lat and user_lon):
            coords = get_coordinates_from_address(address)
            if coords:
                user_lat = coords['latitude']
                user_lon = coords['longitude']
        
        # Get provider details with user information and distance
        provider_list = []
        for provider in providers.items:
            provider_data = provider.to_dict()
            provider_data['user'] = provider.user.to_dict() if provider.user else None
            provider_data['service_category'] = provider.service_category.to_dict() if provider.service_category else None
            
            # Calculate distance if coordinates available
            if user_lat and user_lon and provider.latitude and provider.longitude:
                distance = calculate_distance(user_lat, user_lon, provider.latitude, provider.longitude)
                provider_data['distance_km'] = round(distance, 2) if distance else None
                
                # Filter by distance if specified
                if max_distance and distance and distance > max_distance:
                    continue
            else:
                provider_data['distance_km'] = None
            
            provider_list.append(provider_data)
        
        # Sort by distance if coordinates provided
        if user_lat and user_lon:
            provider_list.sort(key=lambda x: x['distance_km'] if x['distance_km'] is not None else float('inf'))
        
        return jsonify({
            'providers': provider_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': providers.total,
                'pages': providers.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch providers', 'details': str(e)}), 500

@providers_bp.route('/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    """Get specific provider by ID"""
    try:
        provider = ProviderProfile.query.get_or_404(provider_id)
        
        provider_data = provider.to_dict()
        provider_data['user'] = provider.user.to_dict() if provider.user else None
        provider_data['service_category'] = provider.service_category.to_dict() if provider.service_category else None
        
        return jsonify({'provider': provider_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch provider', 'details': str(e)}), 500

@providers_bp.route('/my-profile', methods=['GET'])
@jwt_required()
@provider_required
def get_my_provider_profile():
    """Get current user's provider profile"""
    try:
        current_user_id = get_jwt_identity()
        provider = ProviderProfile.query.filter_by(user_id=current_user_id).first()
        
        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        provider_data = provider.to_dict()
        provider_data['user'] = provider.user.to_dict() if provider.user else None
        provider_data['service_category'] = provider.service_category.to_dict() if provider.service_category else None
        
        return jsonify({'provider': provider_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch provider profile', 'details': str(e)}), 500

@providers_bp.route('/my-profile', methods=['PUT'])
@jwt_required()
@provider_required
def update_my_provider_profile():
    """Update current user's provider profile"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        provider = ProviderProfile.query.filter_by(user_id=current_user_id).first()
        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        # Update fields if provided
        if 'business_name' in data:
            provider.business_name = data['business_name']
        if 'description' in data:
            provider.description = data['description']
        if 'hourly_rate' in data:
            provider.hourly_rate = data['hourly_rate']
        if 'service_category_id' in data:
            # Verify service category exists
            service_category = ServiceCategory.query.get(data['service_category_id'])
            if not service_category:
                return jsonify({'error': 'Service category not found'}), 404
            provider.service_category_id = data['service_category_id']
        if 'latitude' in data:
            provider.latitude = data['latitude']
        if 'longitude' in data:
            provider.longitude = data['longitude']
        if 'is_available' in data:
            provider.is_available = data['is_available']
        if 'experience_years' in data:
            provider.experience_years = data['experience_years']
        
        db.session.commit()
        
        provider_data = provider.to_dict()
        provider_data['user'] = provider.user.to_dict() if provider.user else None
        provider_data['service_category'] = provider.service_category.to_dict() if provider.service_category else None
        
        return jsonify({
            'message': 'Provider profile updated successfully',
            'provider': provider_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update provider profile', 'details': str(e)}), 500

@providers_bp.route('/my-profile/availability', methods=['PUT'])
@jwt_required()
@provider_required
def update_availability():
    """Update provider availability status"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'is_available' not in data:
            return jsonify({'error': 'is_available field is required'}), 400
        
        provider = ProviderProfile.query.filter_by(user_id=current_user_id).first()
        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        provider.is_available = data['is_available']
        db.session.commit()
        
        return jsonify({
            'message': f'Availability updated to {provider.is_available}',
            'is_available': provider.is_available
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update availability', 'details': str(e)}), 500

@providers_bp.route('/categories', methods=['GET'])
def get_service_categories():
    """Get all service categories"""
    try:
        categories = ServiceCategory.query.all()
        
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch service categories', 'details': str(e)}), 500

@providers_bp.route('/my-profile/image', methods=['POST'])
@jwt_required()
@provider_required
def upload_provider_image():
    """Upload provider business image"""
    try:
        current_user_id = get_jwt_identity()
        provider = ProviderProfile.query.filter_by(user_id=current_user_id).first()
        
        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'error': 'Invalid file type. Use PNG, JPG, JPEG, or GIF'}), 400
        
        # Delete old image if exists
        if provider.business_image_public_id:
            delete_image(provider.business_image_public_id)
        
        # Upload new image
        public_id = f"providers/{current_user_id}"
        result = upload_image(file, folder="joblink/providers", public_id=public_id)
        
        if not result['success']:
            return jsonify({'error': 'Failed to upload image', 'details': result['error']}), 500
        
        # Update provider profile
        provider.business_image_url = result['url']
        provider.business_image_public_id = result['public_id']
        db.session.commit()
        
        return jsonify({
            'message': 'Business image uploaded successfully',
            'image_url': result['url']
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upload business image', 'details': str(e)}), 500

@providers_bp.route('/nearby', methods=['GET'])
def get_nearby_providers():
    """Get providers near a specific location"""
    try:
        # Required location parameters
        user_lat = request.args.get('latitude', type=float)
        user_lon = request.args.get('longitude', type=float)
        address = request.args.get('address')
        
        if not (user_lat and user_lon) and not address:
            return jsonify({'error': 'Either latitude/longitude or address is required'}), 400
        
        # Get coordinates from address if needed
        if address and not (user_lat and user_lon):
            coords = get_coordinates_from_address(address)
            if not coords:
                return jsonify({'error': 'Could not geocode address'}), 400
            user_lat = coords['latitude']
            user_lon = coords['longitude']
        
        # Search parameters
        max_distance = request.args.get('max_distance', 25, type=float)  # Default 25km
        service_category_id = request.args.get('service_category_id', type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # Get all available providers
        query = ProviderProfile.query.filter_by(is_available=True)
        
        if service_category_id:
            query = query.filter_by(service_category_id=service_category_id)
        
        providers = query.all()
        
        # Calculate distances and filter
        nearby_providers = []
        for provider in providers:
            if provider.latitude and provider.longitude:
                distance = calculate_distance(user_lat, user_lon, provider.latitude, provider.longitude)
                
                if distance and distance <= max_distance:
                    provider_data = provider.to_dict()
                    provider_data['user'] = provider.user.to_dict() if provider.user else None
                    provider_data['service_category'] = provider.service_category.to_dict() if provider.service_category else None
                    provider_data['distance_km'] = round(distance, 2)
                    nearby_providers.append(provider_data)
        
        # Sort by distance and limit results
        nearby_providers.sort(key=lambda x: x['distance_km'])
        nearby_providers = nearby_providers[:limit]
        
        return jsonify({
            'providers': nearby_providers,
            'search_location': {
                'latitude': user_lat,
                'longitude': user_lon,
                'address': address
            },
            'search_radius_km': max_distance,
            'total_found': len(nearby_providers)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to search nearby providers', 'details': str(e)}), 500