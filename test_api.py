#!/usr/bin/env python3
"""
Simple test script to verify the API works locally
"""
import requests
import json

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Animal Classification API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test classes endpoint
    try:
        response = requests.get(f"{base_url}/classes")
        print(f"✅ Classes endpoint: {response.status_code}")
        data = response.json()
        print(f"   Found {data.get('count', 0)} classes")
    except Exception as e:
        print(f"❌ Classes endpoint failed: {e}")
    
    print("\n🎯 API test completed!")

if __name__ == "__main__":
    test_api()
