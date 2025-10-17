#!/usr/bin/env python3
"""
Test script for Google Colab TFLite API
Run this to test your API endpoints
"""

import requests
import base64
import json

# Replace with your actual ngrok URL
API_URL = "https://your-ngrok-url.ngrok.io"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_analyze():
    """Test analyze endpoint with sample image"""
    try:
        # Create a simple test image (1x1 pixel)
        from PIL import Image
        import io
        
        # Create a simple test image
        img = Image.new('RGB', (160, 160), color='green')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Convert to base64
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # Send to API
        response = requests.post(f"{API_URL}/analyze", json={
            "image": img_base64,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        print(f"Analyze Test: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Analyze test failed: {e}")
        return False

def test_test_endpoint():
    """Test test endpoint"""
    try:
        response = requests.get(f"{API_URL}/test")
        print(f"Test Endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Test endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Google Colab TFLite API...")
    print(f"API URL: {API_URL}")
    print("-" * 50)
    
    # Test all endpoints
    health_ok = test_health()
    test_ok = test_test_endpoint()
    analyze_ok = test_analyze()
    
    print("-" * 50)
    print("📊 Test Results:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Test Endpoint: {'✅ PASS' if test_ok else '❌ FAIL'}")
    print(f"Analyze Endpoint: {'✅ PASS' if analyze_ok else '❌ FAIL'}")
    
    if all([health_ok, test_ok, analyze_ok]):
        print("\n🎉 All tests passed! Your API is working correctly!")
    else:
        print("\n❌ Some tests failed. Check your API setup.")
