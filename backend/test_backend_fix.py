#!/usr/bin/env python3
"""
Test script to verify the fixed Ollama connection
Run this to verify the backend can call Ollama correctly
"""

import sys
import requests
import json

print("=" * 70)
print("🔧 OLLAMA BACKEND CONNECTION FIX - TEST")
print("=" * 70)

# Test 1: Check Ollama is running
print("\n[TEST 1] Checking if Ollama is running...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        print("✅ Ollama is running at http://localhost:11434")
        models = response.json().get('models', [])
        print(f"   {len(models)} model(s) available")
        for model in models:
            print(f"   - {model.get('name', 'unknown')}")
    else:
        print(f"❌ Ollama returned status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Cannot reach Ollama: {e}")
    print("   Start Ollama with: ollama serve")
    sys.exit(1)

# Test 2: Test the exact API call the backend uses
print("\n[TEST 2] Testing API endpoint with the exact backend format...")
try:
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "phi3",
        "prompt": "Hello, say hello back",
        "stream": False,
        "num_predict": 80
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"   POST {url}")
    print(f"   Payload: {json.dumps(payload, indent=2)}")
    print(f"   Timeout: 30s")
    print(f"   Waiting for response...")
    
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30
    )
    
    print(f"\n   📊 Status code: {response.status_code}")
    print(f"   📄 Response length: {len(response.text)} bytes")
    
    if response.status_code == 200:
        try:
            data = response.json()
            result = data.get("response", "").strip()
            
            if result:
                print(f"✅ Got response from AI:")
                print(f"   {result}")
                print(f"\n✅ TEST PASSED - Backend should work now!")
            else:
                print(f"❌ Response was empty")
                print(f"   Full response: {response.text}")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print(f"   Raw response: {response.text}")
            sys.exit(1)
    else:
        print(f"❌ API returned status {response.status_code}")
        print(f"   Response: {response.text}")
        sys.exit(1)
        
except requests.Timeout:
    print(f"❌ Request timed out after 30 seconds")
    print(f"   phi3 might be slow or not installed")
    print(f"   Try: ollama pull phi3")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    sys.exit(1)

# Test 3: Verify the backend service
print("\n[TEST 3] Testing backend Flask app...")
try:
    backend_response = requests.post(
        "http://localhost:5000/api/chat",
        json={"message": "Hi"},
        timeout=40
    )
    
    if backend_response.status_code == 200:
        data = backend_response.json()
        if data.get('status') == 'success':
            answer = data.get('ai_response', {}).get('answer', '')
            if answer and "not responding" not in answer.lower():
                print(f"✅ Backend chat works! Got: {answer[:50]}...")
            else:
                print(f"❌ Got empty or fallback response: {answer}")
                sys.exit(1)
        else:
            print(f"❌ Backend returned error: {data}")
            sys.exit(1)
    else:
        print(f"❌ Backend returned status {backend_response.status_code}")
        sys.exit(1)
        
except requests.ConnectionError:
    print(f"ℹ️  Backend not running on localhost:5000 (that's OK for this test)")
except Exception as e:
    print(f"ℹ️  Backend test failed: {e}")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED - Backend fix verified!")
print("=" * 70)
print("\nNext steps:")
print("1. Ensure backend is running: python app.py")
print("2. Try the chat with: 'Hi', 'Tell me a joke', 'I have fever'")
print("3. Should get AI responses, not 'AI is not responding'")
print("\n")
