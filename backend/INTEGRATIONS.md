# 🔌 JobLink External API Integrations

## 📸 Cloudinary REST API

### Upload User Profile Image
```
POST /api/users/profile/image
Authorization: Bearer <token>
Content-Type: multipart/form-data

Body:
- image: (file) Image file (PNG, JPG, JPEG, GIF)
```

### Upload Provider Business Image
```
POST /api/providers/my-profile/image
Authorization: Bearer <token>
Content-Type: multipart/form-data

Body:
- image: (file) Image file (PNG, JPG, JPEG, GIF)
```

### Test Cloudinary Upload
```
POST /api/integrations/test-cloudinary
Authorization: Bearer <token>
Content-Type: multipart/form-data

Body:
- image: (file) Test image upload
```

## 📧 SendGrid Mail API v3

### Automatic Email Triggers
- **User Registration**: Verification email sent automatically
- **Booking Created**: Confirmation email to client + notification to provider
- **Booking Status Changes**: Updates sent to relevant parties

### Test Email Sending
```
POST /api/integrations/test-email
Authorization: Bearer <token>
Content-Type: application/json

Body:
{
  "to_email": "test@example.com",
  "subject": "Test Subject",
  "content": "<h1>Test HTML Content</h1>"
}
```

## 💳 M-Pesa Daraja API

### Initiate STK Push Payment
```
POST /api/payments/mpesa/stk-push
Authorization: Bearer <token>
Content-Type: application/json

Body:
{
  "booking_id": 1,
  "phone_number": "0712345678"
}
```

### Test M-Pesa Integration
```
POST /api/payments/test-mpesa
Authorization: Bearer <token>
Content-Type: application/json

Body:
{
  "phone_number": "0712345678",
  "amount": 100
}
```

## 🌍 Google Maps Geocoding API

### Convert Address to Coordinates
```
POST /api/geo/geocode
Authorization: Bearer <token>
Content-Type: application/json

Body:
{
  "address": "Nairobi, Kenya"
}
```

### Calculate Distance Between Points
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
```

## 🔧 Environment Setup

Add these API keys to your `.env` file:

```env
# Cloudinary REST API
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# SendGrid Mail API v3
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@joblink.com
FRONTEND_URL=http://localhost:3000

# M-Pesa Daraja API
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=your-passkey
MPESA_CALLBACK_URL=https://your-domain.com/api/payments/mpesa/callback
MPESA_BASE_URL=https://sandbox.safaricom.co.ke

# Google Maps Geocoding API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

## 📋 External API Integration Status

✅ **Cloudinary REST API**
- Profile image uploads for users
- Business image uploads for providers
- Automatic image optimization (500x500, auto quality)
- Image deletion when updating

✅ **SendGrid Mail API v3**
- Email verification on registration
- Booking confirmation emails
- Provider notification emails
- Test email endpoint

✅ **M-Pesa Daraja API**
- STK Push payments for bookings
- Payment status callbacks
- Test payment functionality

✅ **Google Maps Geocoding API**
- Address to coordinates conversion
- Distance calculation between points
- Location-based provider search

## 🧪 API Testing

1. **Test Cloudinary API**: Use `/api/integrations/test-cloudinary` with any image
2. **Test SendGrid API**: Use `/api/integrations/test-email` with valid email
3. **Test M-Pesa API**: Use `/api/payments/test-mpesa` with phone number
4. **Test Google Maps API**: Use `/api/geo/geocode` with address
5. **Test Full Flow**: Register → Upload image → Create booking → Pay with M-Pesa → Check emails