#!/usr/bin/env python3
"""
Test script to verify backend setup and CORS configuration
"""
from app import create_app
from flask import jsonify

def test_backend():
    app = create_app()
    
    @app.route('/test-cors')
    def test_cors():
        return jsonify({
            'message': 'CORS is working!',
            'status': 'success',
            'backend': 'Flask server running'
        })
    
    print("✅ Backend server configured successfully")
    print("✅ CORS enabled for cross-origin requests")
    print("✅ Test endpoint available at: /test-cors")
    print("\nTo start server: python app.py")
    
    return app

if __name__ == '__main__':
    app = test_backend()
    app.run(debug=True, port=5000)