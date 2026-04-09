#!/usr/bin/env python3
"""
Direct Ollama Connection Test - No Dependencies
Tests exact same endpoint and format as backend
"""

import requests
import json
import sys

print("=" * 70)
print("🔧 DIRECT OLLAMA TEST - Debugging Backend Issues")
print("=" * 70)

# Test parameters
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:2b"
TIMEOUT = 40
PROMPT = "You are a helpful assistant.\n\nUser: Hi\n\nRespond naturally and helpfully."
MAX_TOKENS = 70

print("\n[TEST 1] Checking if Ollama is reachable...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        print(f"✅ Ollama is reachable at http://localhost:11434")
        models = response.json().get('models', [])
        print(f"   Models available: {len(models)}")
        for model in models:
            print(f"   - {model.get('name', 'unknown')}")
    else:
        print(f"❌ Ollama returned status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Cannot reach Ollama: {e}")
    print(f"   Start Ollama with: ollama serve")
    sys.exit(1)

print("\n[TEST 2] Checking if gemma:2b model is available...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    models = [m.get('name', '') for m in response.json().get('models', [])]
    if 'gemma:2b' in models:
        print(f"✅ Model gemma:2b is available")
    else:
        print(f"❌ Model gemma:2b NOT found")
        print(f"   Available models: {models}")
        print(f"   Pull with: ollama pull gemma:2b")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error checking models: {e}")
    sys.exit(1)

print("\n[TEST 3] Testing exact API call (same as backend)...")
print(f"   URL: {OLLAMA_URL}")
print(f"   Model: {MODEL}")
print(f"   Timeout: {TIMEOUT}s")
print(f"   Max tokens: {MAX_TOKENS}")
print(f"   Prompt: {PROMPT[:60]}...")

try:
    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False,
        "num_predict": MAX_TOKENS
    }
    
    print("\n   Sending request...")
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=TIMEOUT
    )
    
    print(f"   ✅ Got response!")
    print(f"   Status code: {response.status_code}")
    print(f"   Response length: {len(response.text)} bytes")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   JSON parsed successfully!")
            print(f"   JSON keys: {list(data.keys())}")
            
            ai_response = data.get("response", "").strip()
            if ai_response:
                print(f"   ✅ Got AI response: {ai_response}")
                print("\n" + "=" * 70)
                print("✅ ALL TESTS PASSED - Backend should work!")
                print("=" * 70)
                print("\nNext steps:")
                print("1. Restart backend: python app.py")
                print("2. Watch backend terminal for DEBUG output")
                print("3. Test frontend at http://localhost:5173")
                sys.exit(0)
            else:
                print(f"❌ Response field was empty")
                print(f"   Full response: {response.text}")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print(f"   Raw response: {response.text}")
            sys.exit(1)
    else:
        print(f"❌ Ollama returned status {response.status_code}")
        print(f"   Response: {response.text}")
        sys.exit(1)

except requests.Timeout:
    print(f"❌ TIMEOUT after {TIMEOUT}s")
    print("   gemma:2b is responding too slowly")
    print("   Try increasing timeout or check system load")
    sys.exit(1)

except requests.ConnectionError as e:
    print(f"❌ Connection error: {e}")
    print("   Is Ollama running? ollama serve")
    sys.exit(1)

except Exception as e:
    print(f"❌ Unexpected error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
