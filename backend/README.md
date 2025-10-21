# JobLink Backend

Flask backend for the JobLink application.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
copy .env.template .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python app.py
```

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/services/` - Get services
- `GET /api/bookings/` - Get bookings