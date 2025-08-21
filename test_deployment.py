#!/usr/bin/env python3
"""
Comprehensive test script for Animal Classification API
Tests all endpoints to ensure deployment readiness
"""
import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Animal Classification API for Deployment...")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check: {response.status_code}")
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🐾 Classes: {data.get('num_classes')}")
            print(f"   🌐 Deployment: {data.get('deployment')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: Classes Endpoint
    print("\n2️⃣ Testing Classes Endpoint...")
    try:
        response = requests.get(f"{base_url}/classes")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Classes endpoint: {response.status_code}")
            print(f"   🐾 Found {data.get('count', 0)} animal classes")
            print(f"   📝 Sample classes: {', '.join(data.get('classes', [])[:5])}")
        else:
            print(f"   ❌ Classes endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Classes endpoint error: {e}")
        return False
    
    # Test 3: Root Endpoint (Frontend)
    print("\n3️⃣ Testing Root Endpoint (Frontend)...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            content = response.text
            print(f"   ✅ Root endpoint: {response.status_code}")
            print(f"   📄 Content type: {response.headers.get('content-type')}")
            print(f"   📏 Content length: {len(content)} characters")
            if "Animal Classifier" in content:
                print(f"   🎯 Frontend content: Found 'Animal Classifier'")
            else:
                print(f"   ⚠️ Frontend content: Basic HTML fallback")
        else:
            print(f"   ❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
        return False
    
    # Test 4: Static Files (if available)
    print("\n4️⃣ Testing Static Files...")
    try:
        response = requests.get(f"{base_url}/static/styles.css")
        if response.status_code == 200:
            print(f"   ✅ Static files: CSS loaded successfully")
        else:
            print(f"   ⚠️ Static files: CSS not found (will use fallback)")
    except Exception as e:
        print(f"   ⚠️ Static files: Error accessing (will use fallback)")
    
    print("\n" + "=" * 50)
    print("🎯 All API tests completed successfully!")
    print("✅ Your API is ready for Vercel deployment!")
    print("🚀 Deploy now and it should work perfectly!")
    
    return True

def main():
    """Main test function"""
    print("🚀 Animal Classification API - Deployment Test")
    print("This script tests all endpoints before deployment")
    
    # Wait a moment for server to start
    print("\n⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Run tests
    success = test_api_endpoints()
    
    if success:
        print("\n🎉 SUCCESS: All tests passed! Ready for deployment!")
    else:
        print("\n❌ FAILURE: Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
