#!/usr/bin/env python3
"""
Main application entry point for JobLink backend
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)