import math
import requests
import os

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula"""
    if not all([lat1, lon1, lat2, lon2]):
        return None
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth radius in kilometers
    r = 6371
    return c * r

def get_coordinates_from_address(address):
    """Get coordinates from address using Google Maps API"""
    try:
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if not api_key:
            return None
        
        url = f"https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': address,
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return {
                'latitude': location['lat'],
                'longitude': location['lng']
            }
        return None
    except Exception:
        return None