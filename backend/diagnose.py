#!/usr/bin/env python3
"""
Complete Backend Diagnostic - Find the exact problem
Run this to identify why AI is not responding
"""

import subprocess
import sys
import os
import time

print("=" * 80)
print("🔧 AI HEALTH ASSISTANT - BACKEND DIAGNOSTIC")
print("=" * 80)

# STEP 1: Check system
print("\n[STEP 1] System Check")
print("-" * 80)

print("1.1 Checking Python version...")
try:
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    print(f"✅ {result.stdout.strip()}")
except:
    print("❌ Cannot check Python version")

print("\n1.2 Checking current directory...")
cwd = os.getcwd()
print(f"   Current: {cwd}")
if "backend" in cwd:
    print("✅ In backend directory")
else:
    print("⚠️  Not in backend directory, need to cd backend first")

print("\n1.3 Checking backend structure...")
backend_files = [
    "app.py",
    "ai_module/ollama_service.py",
    "requirements.txt",
    ".env.example"
]
for f in backend_files:
    path = os.path.join(cwd, f)
    if os.path.exists(path):
        print(f"✅ {f}")
    else:
        print(f"❌ MISSING: {f}")

# STEP 2: Check Ollama
print("\n[STEP 2] Ollama Service Check")
print("-" * 80)

print("2.1 Testing if Ollama is running...")
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        print("✅ Ollama service is RUNNING at http://localhost:11434")
        models = response.json().get('models', [])
        print(f"   Available models: {len(models)}")
        for model in models[:5]:
            name = model.get('name', 'unknown')
            size = model.get('size', 0) / (1024**3)  # Convert to GB
            print(f"   - {name} ({size:.1f} GB)")
        
        if any('gemma:2b' in m.get('name', '') for m in models):
            print("✅ gemma:2b model is AVAILABLE")
        else:
            print("❌ gemma:2b model NOT FOUND")
            print("   Need to run: ollama pull gemma:2b")
    else:
        print(f"❌ Ollama returned status {response.status_code}")
except requests.ConnectionError:
    print("❌ CANNOT REACH OLLAMA")
    print("   Need to start: ollama serve")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# STEP 3: Check backend code
print("\n[STEP 3] Backend Code Check")
print("-" * 80)

print("3.1 Checking ollama_service.py for gemma:2b...")
with open("ai_module/ollama_service.py", "r") as f:
    content = f.read()
    if 'gemma:2b' in content:
        print("✅ Code contains 'gemma:2b'")
    else:
        print("❌ Code does NOT contain 'gemma:2b' - MODEL NOT CONFIGURED!")
    
    if 'timeout=40' in content:
        print("✅ Code has 40-second timeout")
    else:
        print("⚠️  Code may not have 40-second timeout")
    
    if 'OLLAMA DEBUG - STEP' in content:
        print("✅ Aggressive debug logging is present")
    else:
        print("❌ Debug logging NOT FOUND - code may not be updated!")

print("\n3.2 Checking app.py for error handling...")
with open("app.py", "r") as f:
    content = f.read()
    if 'always return 200' in content.lower() or '200' in content:
        print("✅ Error handling appears to be updated")
    else:
        print("⚠️  May have old error handling")

# STEP 4: Test direct API call
print("\n[STEP 4] Direct Ollama API Test")
print("-" * 80)

print("4.1 Testing direct API call to gemma:2b...")
try:
    import requests
    import json
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma:2b",
        "prompt": "Say hello",
        "stream": False,
        "num_predict": 20
    }
    
    print(f"   URL: {url}")
    print(f"   Model: gemma:2b")
    print(f"   Timeout: 40s")
    
    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=40
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        ai_response = data.get("response", "").strip()
        if ai_response:
            print(f"✅ Got response: {ai_response[:50]}...")
        else:
            print("❌ Response was empty")
    else:
        print(f"❌ Status {response.status_code}: {response.text}")
        
except requests.Timeout:
    print("❌ TIMEOUT (40s) - Ollama too slow or stuck")
except requests.ConnectionError:
    print("❌ CONNECTION ERROR - Ollama not running")
except Exception as e:
    print(f"❌ Error: {e}")

# STEP 5: Check Flask backend
print("\n[STEP 5] Flask Backend Check")
print("-" * 80)

print("5.1 Testing Flask health endpoint...")
try:
    import requests
    response = requests.get("http://localhost:5000/api/health", timeout=5)
    if response.status_code == 200:
        print(f"✅ Flask backend is RUNNING")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Flask returned status {response.status_code}")
except requests.ConnectionError:
    print("❌ FLASK NOT RUNNING at http://localhost:5000")
    print("   Need to start: cd backend && python app.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")

# STEP 6: Test chat endpoint
print("\n[STEP 6] Chat Endpoint Test")
print("-" * 80)

print("6.1 Testing /api/chat endpoint...")
try:
    import requests
    response = requests.post(
        "http://localhost:5000/api/chat",
        json={"message": "Hi"},
        timeout=45
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")
        
        if 'ai_response' in data:
            answer = data.get('ai_response', {}).get('answer', '')
            if 'not responding' in answer.lower():
                print("⚠️  Got fallback message (Ollama call failed)")
            elif answer:
                print(f"✅ Got real AI response: {answer[:60]}...")
            else:
                print("❌ Empty response")
        else:
            print("❌ No ai_response field")
    else:
        print(f"❌ Status {response.status_code}")
        print(f"   Response: {response.text}")
        
except requests.Timeout:
    print("❌ TIMEOUT (45s)")
except requests.ConnectionError:
    print("❌ FLASK NOT RUNNING")
except Exception as e:
    print(f"❌ Error: {e}")

# STEP 7: Summary
print("\n[STEP 7] Summary & Next Steps")
print("=" * 80)

print("""
If you see ✅ for all checks above, the system should work!

Common Issues & Fixes:

1. "❌ CANNOT REACH OLLAMA"
   → Fix: Open terminal, run: ollama serve

2. "❌ gemma:2b model NOT FOUND"
   → Fix: Run: ollama pull gemma:2b

3. "❌ FLASK NOT RUNNING"
   → Fix: cd backend && python app.py

4. "⚠️  Got fallback message"
   → Check backend terminal for debug output
   → Look for: "OLLAMA DEBUG - STEP" messages
   → Check for error messages

5. Code not updated (❌ on STEP 3)
   → Make sure backend was edited correctly
   → Run: python test_direct_ollama.py first

Next Steps:
1. Fix any ❌ issues above
2. Restart backend: python app.py
3. Watch backend terminal for "OLLAMA DEBUG" output
4. Test chat again in frontend
5. Share the debug output if still failing
""")

print("=" * 80)
