# 🌍 JobLink Geo-Location Features

## 📍 Provider Location Search

### Get Nearby Providers
```
GET /api/providers/nearby?latitude=-1.286389&longitude=36.817223&max_distance=25
GET /api/providers/nearby?address=Nairobi,Kenya&max_distance=50

Query Parameters:
- latitude: User latitude (required if no address)
- longitude: User longitude (required if no address)  
- address: User address (alternative to lat/lon)
- max_distance: Search radius in km (default: 25)
- service_category_id: Filter by service category
- limit: Max results (default: 20)
```

### Enhanced Provider Search with Distance
```
GET /api/providers?latitude=-1.286389&longitude=36.817223&max_distance=30

Query Parameters:
- All existing filters (search, category, rate, etc.)
- latitude: User latitude
- longitude: User longitude
- address: User address (geocoded automatically)
- max_distance: Filter radius in km (default: 50)
```

## 🧭 Geo Utilities

### Geocode Address
```
POST /api/geo/geocode
Authorization: Bearer <token>
Content-Type: application/json

Body:
{
  "address": "Nairobi, Kenya"
}

Response:
{
  "message": "Geocoding successful",
  "address": "Nairobi, Kenya",
  "coordinates": {
    "latitude": -1.286389,
    "longitude": 36.817223
  }
}
```

### Calculate Distance
```
POST /api/geo/distance
Authorization: Bearer <token>
Content-Type: application/json

Body:
{
  "lat1": -1.286389,
  "lon1": 36.817223,
  "lat2": -1.292066,
  "lon2": 36.821946
}

Response:
{
  "message": "Distance calculated successfully",
  "distance_km": 1.23,
  "coordinates": {
    "point1": {"lat": -1.286389, "lon": 36.817223},
    "point2": {"lat": -1.292066, "lon": 36.821946}
  }
}
```

## 🔧 Environment Setup

Add to your `.env` file:
```env
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

## 📋 Features Implemented

✅ **Distance Calculation**
- Haversine formula for accurate distance
- Works without external API calls
- Returns distance in kilometers

✅ **Address Geocoding**
- Google Maps Geocoding API integration
- Converts addresses to coordinates
- Fallback for manual coordinate entry

✅ **Provider Search**
- Search by coordinates or address
- Filter by distance radius
- Sort results by proximity
- Combine with existing filters

✅ **Enhanced Endpoints**
- `/api/providers/nearby` - Dedicated location search
- `/api/providers` - Enhanced with geo-filtering
- `/api/geo/geocode` - Address to coordinates
- `/api/geo/distance` - Distance calculation

## 🧪 Testing Examples

**Search providers near Nairobi:**
```bash
GET /api/providers/nearby?address=Nairobi,Kenya&max_distance=25&service_category_id=1
```

**Calculate distance between two points:**
```bash
POST /api/geo/distance
{
  "lat1": -1.286389, "lon1": 36.817223,
  "lat2": -1.292066, "lon2": 36.821946
}
```