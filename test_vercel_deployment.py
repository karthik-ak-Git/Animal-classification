#!/usr/bin/env python3
"""
Test script for deployed Animal Classification app on Vercel
Run this to test all endpoints and functionality after deployment
"""

import requests
import json
import time
from pathlib import Path


def test_deployment(base_url):
    """Test the deployed Animal Classification application"""

    print(f"🧪 Testing Animal Classification App at: {base_url}")
    print("=" * 60)

    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data}")
            print(f"   Model Loaded: {data.get('model_loaded', 'Unknown')}")
            print(f"   Classes: {data.get('num_classes', 'Unknown')}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")

    # Test 2: Get Classes
    print("\n2️⃣ Testing Get Classes...")
    try:
        response = requests.get(f"{base_url}/classes", timeout=30)
        if response.status_code == 200:
            data = response.json()
            classes = data.get('classes', [])
            print(f"✅ Classes Retrieved: {len(classes)} classes")
            print(f"   Sample classes: {classes[:5]}...")
        else:
            print(f"❌ Get Classes Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Classes Error: {e}")

    # Test 3: Main Page
    print("\n3️⃣ Testing Main Page...")
    try:
        response = requests.get(base_url, timeout=30)
        if response.status_code == 200:
            print("✅ Main Page: Successfully loaded")
            if "Animal Classifier" in response.text:
                print("   ✅ Contains expected title")
            if "upload" in response.text.lower():
                print("   ✅ Contains upload functionality")
        else:
            print(f"❌ Main Page Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main Page Error: {e}")

    # Test 4: Prediction Endpoint (without actual image)
    print("\n4️⃣ Testing Prediction Endpoint Structure...")
    try:
        # This will fail but shows if endpoint exists
        response = requests.post(f"{base_url}/predict", timeout=30)
        if response.status_code == 422:  # Expected - missing file
            print("✅ Prediction Endpoint: Available (422 = missing file expected)")
        else:
            print(f"⚠️ Prediction Endpoint: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Prediction Endpoint Error: {e}")

    print("\n" + "=" * 60)
    print("🎯 Manual Testing Instructions:")
    print(f"1. Visit: {base_url}")
    print("2. Upload an animal image (dog, cat, bird, etc.)")
    print("3. Verify classification results")
    print("4. Test feedback system if available")
    print("\n✅ Automated tests completed!")


def get_deployment_url():
    """Helper to get deployment URL from user"""
    print("🔗 Enter your Vercel deployment URL:")
    print("   Format: https://animal-classification-xyz.vercel.app")
    print("   (without trailing slash)")

    while True:
        url = input("\n📎 Deployment URL: ").strip()
        if url.startswith("http"):
            return url.rstrip("/")
        else:
            print("❌ Please enter a valid URL starting with http")


if __name__ == "__main__":
    print("🚀 Animal Classification - Deployment Tester")
    print("=" * 50)

    # Option 1: Use provided URL
    # url = "https://your-deployment.vercel.app"  # Replace with actual URL

    # Option 2: Interactive URL entry
    url = get_deployment_url()

    # Run tests
    test_deployment(url)
