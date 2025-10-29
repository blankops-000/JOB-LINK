#!/usr/bin/env python3
"""
Test script to verify Flask routes are registered correctly
"""

from app import create_app

app = create_app()

print("[INFO] Registered Routes:")
print("=" * 50)

for rule in app.url_map.iter_rules():
    methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
    print(f"{rule.rule:<30} [{methods}]")

print("=" * 50)
print(f"Total routes: {len(list(app.url_map.iter_rules()))}")

# Check specifically for swagger routes
swagger_routes = [rule for rule in app.url_map.iter_rules() if 'swagger' in rule.rule or 'docs' in rule.rule]
print(f"\n[SWAGGER] Swagger-related routes: {len(swagger_routes)}")
for route in swagger_routes:
    methods = ','.join(route.methods - {'HEAD', 'OPTIONS'})
    print(f"  {route.rule} [{methods}]")