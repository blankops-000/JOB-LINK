#!/usr/bin/env python3
"""
Direct test of Swagger functionality
"""

from app import create_app
import json

app = create_app()

with app.test_client() as client:
    print("[TEST] Testing Swagger JSON endpoint...")
    
    # Test swagger.json endpoint
    response = client.get('/api/swagger.json')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.get_json()
            print(f"[OK] Valid JSON response")
            print(f"[OK] OpenAPI version: {data.get('openapi', 'Not found')}")
            print(f"[OK] API title: {data.get('info', {}).get('title', 'Not found')}")
            print(f"[OK] Number of endpoints: {len(data.get('paths', {}))}")
            print(f"[OK] Tags: {[tag['name'] for tag in data.get('tags', [])]}")
        except Exception as e:
            print(f"[ERROR] JSON parsing failed: {e}")
    else:
        print(f"[ERROR] Request failed: {response.data.decode()}")
    
    # Test swagger UI endpoint
    print(f"\n[TEST] Testing Swagger UI endpoint...")
    response = client.get('/api/docs/')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("[OK] Swagger UI accessible")
    else:
        print(f"[ERROR] Swagger UI failed: {response.data.decode()}")