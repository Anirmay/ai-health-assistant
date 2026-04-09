#!/usr/bin/env python3
"""
Test script to verify Ollama connection and phi3 model
Tests the exact API endpoint and request format used by the backend
"""

import requests
import json
import time

print("=" * 60)
print("🧪 OLLAMA CONNECTION TEST")
print("=" * 60)

# Configuration
OLLAMA_URL = "http://localhost:11434"
API_ENDPOINT = f"{OLLAMA_URL}/api/generate"
MODEL = "phi3"
TIMEOUT = 20

print(f"\n📍 Testing connection to: {OLLAMA_URL}")
print(f"🤖 Model: {MODEL}")
print(f"⏱️  Timeout: {TIMEOUT}s\n")

# Test 1: Check if Ollama is running
print("TEST 1: Check if Ollama is running...")
try:
    response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
    if response.status_code == 200:
        print("✅ Ollama is running and responding")
        data = response.json()
        models = data.get('models', [])
        print(f"   Available models: {len(models)}")
        for model in models:
            print(f"   - {model.get('name', 'unknown')}")
    else:
        print(f"❌ Ollama returned status {response.status_code}")
        exit(1)
except Exception as e:
    print(f"❌ Cannot connect to Ollama at {OLLAMA_URL}")
    print(f"   Error: {e}")
    print("\n   Make sure Ollama is running:")
    print("   1. Open terminal")
    print("   2. Run: ollama serve")
    exit(1)

# Test 2: Test API endpoint with a simple prompt
print("\nTEST 2: Test API endpoint /api/generate...")
payload = {
    "model": MODEL,
    "prompt": "What is 2+2?",
    "stream": False,
    "num_predict": 80,
    "temperature": 0.3
}

print(f"   Sending request to: {API_ENDPOINT}")
print(f"   Payload: {json.dumps(payload, indent=2)}")

try:
    start_time = time.time()
    print(f"\n   ⏳ Waiting for response (timeout: {TIMEOUT}s)...")
    
    response = requests.post(
        API_ENDPOINT,
        json=payload,
        timeout=TIMEOUT
    )
    
    elapsed = time.time() - start_time
    print(f"   ⏱️  Response time: {elapsed:.2f}s")
    
    if response.status_code == 200:
        print("✅ API endpoint is working!")
        data = response.json()
        result = data.get("response", "")
        print(f"\n   📝 Response from model:")
        print(f"   {result}")
    else:
        print(f"❌ API returned status {response.status_code}")
        print(f"   Response: {response.text}")
        exit(1)
        
except requests.Timeout:
    print(f"❌ Request timed out after {TIMEOUT}s")
    print("   This means phi3 is too slow or not responding")
    print("   Try increasing OLLAMA_TIMEOUT in .env to 30-40s")
    exit(1)
except requests.ConnectionError as e:
    print(f"❌ Connection error: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    exit(1)

# Test 3: Test health-specific prompt
print("\n" + "=" * 60)
print("TEST 3: Test health-specific prompt...")
print("=" * 60)

health_prompt = """You are a safe health information assistant. CRITICAL RULES:
- ONLY health-related responses
- 2-3 short sentences maximum
- NO diagnosis
- Always end: "Consult a healthcare professional for personalized advice."

User question: I have a fever of 102°F. What should I do?

Answer (2-3 sentences):"""

payload = {
    "model": MODEL,
    "prompt": health_prompt,
    "stream": False,
    "num_predict": 80,
    "temperature": 0.3
}

try:
    start_time = time.time()
    print(f"\n   ⏳ Waiting for health response...")
    
    response = requests.post(
        API_ENDPOINT,
        json=payload,
        timeout=TIMEOUT
    )
    
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        print("✅ Health prompt works!")
        data = response.json()
        result = data.get("response", "")
        print(f"\n   📝 AI Health Response:")
        print(f"   {result}")
    else:
        print(f"❌ Failed: {response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    exit(1)

# Summary
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nYour Ollama setup is working correctly!")
print("The backend should now properly use AI responses.")
print("\nNext steps:")
print("1. Update .env file with: OLLAMA_TIMEOUT=20")
print("2. Restart Flask backend")
print("3. Test the frontend chat")

