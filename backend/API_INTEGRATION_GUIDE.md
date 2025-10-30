# JobLink API Integration Guide

## External Services Integration

This guide covers the integration of M-Pesa, SendGrid, and Cloudinary APIs in the JobLink platform.

---

## 🔧 Setup Instructions

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your API credentials:

```bash
cp .env.example .env
```

### 2. Required API Keys

#### **M-Pesa (Daraja API)**
1. Register at [Safaricom Developer Portal](https://developer.safaricom.co.ke/)
2. Create an app to get:
   - Consumer Key
   - Consumer Secret
   - Passkey
3. Use sandbox for testing, production for live

#### **SendGrid**
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create an API key with "Mail Send" permissions
3. Verify your sender email address

#### **Cloudinary**
1. Sign up at [Cloudinary](https://cloudinary.com/)
2. Get your credentials from the dashboard:
   - Cloud Name
   - API Key
   - API Secret

---

## 📡 API Endpoints

### **Payment Routes** (`/api/payments`)

#### 1. Initiate Payment
```http
POST /api/payments/initiate
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "booking_id": 1,
  "phone_number": "0712345678"
}
```

**Response:**
```json
{
  "message": "Payment initiated successfully",
  "checkout_request_id": "ws_CO_123456789",
  "customer_message": "Success. Request accepted for processing",
  "payment_id": 1
}
```

#### 2. M-Pesa Callback (Webhook)
```http
POST /api/payments/mpesa/callback
Content-Type: application/json
```

#### 3. Check Payment Status
```http
GET /api/payments/status/<payment_id>
Authorization: Bearer <JWT_TOKEN>
```

#### 4. Get Booking Payment
```http
GET /api/payments/booking/<booking_id>
Authorization: Bearer <JWT_TOKEN>
```

#### 5. Payment History
```http
GET /api/payments/history
Authorization: Bearer <JWT_TOKEN>
```

---

### **Upload Routes** (`/api/uploads`)

#### 1. Upload Profile Image
```http
POST /api/uploads/profile-image
Authorization: Bearer <JWT_TOKEN>
Content-Type: multipart/form-data

image: <file>
```

**Response:**
```json
{
  "message": "Profile image uploaded successfully",
  "image_url": "https://res.cloudinary.com/.../image.jpg",
  "public_id": "joblink/profiles/user_1_profile"
}
```

#### 2. Upload Provider Portfolio Image
```http
POST /api/uploads/provider/portfolio
Authorization: Bearer <JWT_TOKEN>
Content-Type: multipart/form-data

image: <file>
index: 0
```

#### 3. Delete Image
```http
DELETE /api/uploads/delete
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "public_id": "joblink/profiles/user_1_profile"
}
```

---

## 📧 Email Service

### Available Email Templates

1. **Welcome Email** - Sent on user registration
2. **Booking Confirmation** - Sent to client when booking is created
3. **Booking Notification** - Sent to provider for new bookings
4. **Payment Confirmation** - Sent after successful payment
5. **Password Reset** - Sent for password reset requests

### Usage Example

```python
from app.utils.email_service import EmailService

# Send welcome email
EmailService.send_welcome_email(user)

# Send booking confirmation
EmailService.send_booking_confirmation(booking, client, provider)

# Send payment confirmation
EmailService.send_payment_confirmation(payment, booking, user)
```

---

## 🖼️ Image Upload Service

### Supported Formats
- PNG, JPG, JPEG, GIF, WEBP
- Max size: 5MB

### Image Transformations

**Profile Images:**
- Size: 400x400px
- Crop: Fill with face detection
- Quality: Auto
- Format: Auto (WebP when supported)

**Portfolio Images:**
- Max size: 800x600px
- Crop: Limit (maintains aspect ratio)
- Quality: Auto
- Format: Auto

### Usage Example

```python
from app.utils.cloudinary_service import CloudinaryService

# Upload profile image
result = CloudinaryService.upload_profile_image(file, user_id)

# Upload portfolio image
result = CloudinaryService.upload_provider_portfolio_image(file, provider_id, index=0)

# Delete image
CloudinaryService.delete_image(public_id)
```

---

## 💳 M-Pesa Integration

### Payment Flow

1. **Client initiates payment** → `POST /api/payments/initiate`
2. **STK Push sent to phone** → User enters M-Pesa PIN
3. **M-Pesa processes payment** → Sends callback to server
4. **Server updates payment status** → `POST /api/payments/mpesa/callback`
5. **Email confirmation sent** → Client receives receipt

### Testing with Sandbox

**Test Credentials:**
- Phone: 254708374149 (or any Safaricom number)
- Amount: Any amount (e.g., 1 KES for testing)
- Shortcode: 174379

### M-Pesa Response Codes

- `0` - Success
- `1` - Insufficient funds
- `17` - User cancelled
- `26` - System busy
- `1032` - Request cancelled by user

---

## 🔒 Security Best Practices

### API Keys
- Never commit `.env` file to version control
- Use different keys for development and production
- Rotate keys regularly

### M-Pesa Callback
- Validate callback source (IP whitelist)
- Use HTTPS for callback URL
- Verify checkout request ID matches

### Image Uploads
- Validate file types and sizes
- Scan for malware (if handling user uploads at scale)
- Use signed URLs for sensitive images

---

## 🧪 Testing

### Test Payment Integration

```bash
# Test payment initiation
curl -X POST http://localhost:5000/api/payments/initiate \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 1,
    "phone_number": "0712345678"
  }'
```

### Test Email Service

```python
from app import create_app, db
from app.models.user import User
from app.utils.email_service import EmailService

app = create_app()
with app.app_context():
    user = User.query.first()
    EmailService.send_welcome_email(user)
```

### Test Image Upload

```bash
curl -X POST http://localhost:5000/api/uploads/profile-image \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -F "image=@/path/to/image.jpg"
```

---

## 📊 Monitoring & Logging

### M-Pesa Transactions
- Log all payment initiations
- Store checkout request IDs
- Monitor callback failures

### Email Delivery
- Check SendGrid dashboard for delivery stats
- Monitor bounce rates
- Track open/click rates (if enabled)

### Image Storage
- Monitor Cloudinary usage
- Set up transformation quotas
- Enable auto-backup

---

## 🚨 Error Handling

### Common Issues

**M-Pesa:**
- Invalid phone number format → Ensure 254XXXXXXXXX format
- Timeout → Retry with exponential backoff
- Callback not received → Check URL accessibility

**SendGrid:**
- API key invalid → Regenerate key
- Sender not verified → Verify email in SendGrid
- Rate limit exceeded → Upgrade plan or throttle

**Cloudinary:**
- Upload failed → Check file size and format
- Transformation error → Verify transformation parameters
- Quota exceeded → Upgrade plan

---

## 📞 Support

- **M-Pesa:** developer@safaricom.co.ke
- **SendGrid:** support@sendgrid.com
- **Cloudinary:** support@cloudinary.com
