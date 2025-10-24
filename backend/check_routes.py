"""
Diagnostic script to check route blueprint exports
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.routes.auth import auth_bp
    print("✅ auth_bp imported successfully from app.routes.auth")
    print(f"Blueprint name: {auth_bp.name}")
except ImportError as e:
    print(f"❌ Error importing auth_bp: {e}")
    
    # Let's see what's actually in the auth module
    try:
        import app.routes.auth as auth_module
        print("✅ app.routes.auth module imported successfully")
        print("Available names in auth module:")
        for name in dir(auth_module):
            if not name.startswith('_'):
                print(f"  - {name}")
    except ImportError as e2:
        print(f"❌ Error importing auth module: {e2}")

try:
    from app.routes.providers import providers_bp
    print("✅ providers_bp imported successfully")
except ImportError as e:
    print(f"❌ Error importing providers_bp: {e}")

try:
    from app.routes.bookings import bookings_bp
    print("✅ bookings_bp imported successfully")
except ImportError as e:
    print(f"❌ Error importing bookings_bp: {e}")

try:
    from app.routes.reviews import reviews_bp
    print("✅ reviews_bp imported successfully")
except ImportError as e:
    print(f"❌ Error importing reviews_bp: {e}")

try:
    from app.routes.admin import admin_bp
    print("✅ admin_bp imported successfully")
except ImportError as e:
    print(f"❌ Error importing admin_bp: {e}")