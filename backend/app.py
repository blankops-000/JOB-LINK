"""
Main application entry point
Run this file to start the Flask development server
"""
from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the development server
    print("=" * 60)
    print("🚀 Starting JobLink Backend Server")
    print("=" * 60)
    print("📡 Server running at: http://localhost:5000")
    print("📖 API Documentation: http://localhost:5000/api/docs")
    print("🔧 Environment: Development")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )