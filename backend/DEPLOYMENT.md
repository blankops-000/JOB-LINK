# JobLink Backend Deployment Guide

## 🚀 Render Deployment

### Prerequisites
- GitHub repository with backend code
- Render account

### Deployment Steps

1. **Connect Repository**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `backend` folder as root directory

2. **Configure Service**
   - **Name**: `joblink-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-random-key>
   JWT_SECRET_KEY=<generate-random-key>
   DATABASE_URL=<postgresql-connection-string>
   CORS_ORIGINS=https://your-frontend-domain.com
   ```

4. **Database Setup**
   - Create PostgreSQL database on Render
   - Copy connection string to `DATABASE_URL`
   - Database migrations run automatically

### Health Check
- Endpoint: `https://your-backend-url.com/health`
- Expected: `{"status": "healthy", "service": "joblink-backend"}`

### API Documentation
- Swagger UI: `https://your-backend-url.com/api/docs`
- OpenAPI Spec: `https://your-backend-url.com/api/swagger.json`

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run migrations
flask db upgrade

# Start development server
python app.py
```

## 📊 Monitoring

- Health endpoint: `/health`
- Logs available in Render dashboard
- Database metrics in PostgreSQL dashboard