#!/usr/bin/env python3
"""
Test script to verify Swagger imports work correctly
"""

try:
    from app.docs.swagger import swaggerui_blueprint, create_swagger_spec
    print("✅ Swagger imports successful")
    print(f"Blueprint name: {swaggerui_blueprint.name}")
    print(f"Blueprint URL prefix: {swaggerui_blueprint.url_prefix}")
except ImportError as e:
    print(f"❌ Swagger import failed: {e}")

try:
    from flask_swagger_ui import get_swaggerui_blueprint
    print("✅ flask-swagger-ui import successful")
except ImportError as e:
    print(f"❌ flask-swagger-ui import failed: {e}")