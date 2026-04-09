# Integration Testing Guide - AI Health Assistant LLM Features

## Test Environment Setup

### Prerequisites
- Backend running: `python app.py` at `http://localhost:5000`
- OpenAI API key configured in environment
- Frontend running: `npm run dev` at `http://localhost:5173`
- Postman or curl for API testing (optional)

## Test Categories

### 1. Backend LLM Service Tests

#### Test 1.1: Import and Initialize
```python
# File: test_llm_service.py
from ai_module.llm_service import get_ai_service

def test_service_initialization():
    """Test that LLM service initializes correctly"""
    service = get_ai_service()
    assert service is not None
    print("✓ LLM Service initialized successfully")

test_service_initialization()
```

**Expected**: ✓ LLM Service initialized successfully

#### Test 1.2: API Key Configuration
```python
def test_api_key_configuration():
    """Test that API key is properly configured"""
    service = get_ai_service()
    status = service.get_system_status()
    
    assert status['status'] in ['operational', 'error']
    if status['api_key_configured']:
        print("✓ API key configured")
    else:
        print("⚠️ API key not configured - LLM features unavailable")
    
    return status

test_api_key_configuration()
```

**Expected**: One of:
- ✓ API key configured
- ⚠️ API key not configured

---

### 2. Flask Endpoint Tests

#### Automated Test Script
```python
# File: test_all_endpoints.py
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_status():
    """Test /api/ai/status"""
    print("\n1. Testing /api/ai/status...")
    response = requests.get(f"{BASE_URL}/api/ai/status")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Status: {data.get('status')}")
    return data.get('api_key_configured', False)

def test_explain(api_available):
    """Test /api/ai/explain"""
    if not api_available:
        print("\n2. Skipping /api/ai/explain (API key not configured)")
        return
    
    print("\n2. Testing /api/ai/explain...")
    payload = {
        "disease": "Flu",
        "symptoms": ["fever", "cough"],
        "confidence": 72
    }
    response = requests.post(f"{BASE_URL}/api/ai/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'disclaimer' in data['ai_explanation']
    print(f"   ✓ Explanation generated")

def test_chat(api_available):
    """Test /api/chat"""
    if not api_available:
        print("\n3. Skipping /api/chat (API key not configured)")
        return
    
    print("\n3. Testing /api/chat...")
    payload = {
        "message": "Should I see a doctor?",
        "context": {"disease": "Flu", "symptoms": ["fever"]}
    }
    start = time.time()
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    elapsed = time.time() - start
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    print(f"   ✓ Chat response received ({elapsed:.2f}s)")

def test_advanced_analysis(api_available):
    """Test /api/advanced/symptom-analysis"""
    if not api_available:
        print("\n4. Skipping /api/advanced/symptom-analysis (API key not configured)")
        return
    
    print("\n4. Testing /api/advanced/symptom-analysis...")
    payload = {"symptoms": "I have fever, cough, and fatigue"}
    start = time.time()
    response = requests.post(f"{BASE_URL}/api/advanced/symptom-analysis", json=payload)
    elapsed = time.time() - start
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    print(f"   ✓ Advanced analysis completed ({elapsed:.2f}s)")

if __name__ == "__main__":
    print("=" * 50)
    print("LLM ENDPOINTS TEST SUITE")
    print("=" * 50)
    
    try:
        api_available = test_status()
        test_explain(api_available)
        test_chat(api_available)
        test_advanced_analysis(api_available)
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED")
        print("=" * 50)
    
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
```

**Run the tests**:
```bash
cd backend
python test_all_endpoints.py
```

---

### 3. Manual API Testing

#### Test /api/ai/status
```bash
curl -X GET http://localhost:5000/api/ai/status
```

#### Test /api/ai/explain
```bash
curl -X POST http://localhost:5000/api/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "Influenza",
    "symptoms": ["fever", "cough", "fatigue"],
    "confidence": 78
  }'
```

#### Test /api/ai/chat
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Should I see a doctor?",
    "context": {
      "disease": "Common Cold",
      "symptoms": ["cough", "runny nose"],
      "confidence": 65,
      "risk_level": "Low"
    }
  }'
```

#### Test /api/advanced/symptom-analysis
```bash
curl -X POST http://localhost:5000/api/advanced/symptom-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "I have been experiencing fever and cough for two days"
  }'
```

---

### 4. Frontend Tests

#### Test 4.1: Chat Widget
1. Navigate to `http://localhost:5173/chat`
2. Verify ChatWidget appears with:
   - ✓ Message display area
   - ✓ Input field
   - ✓ Send button
   - ✓ Medical disclaimer

#### Test 4.2: Chat Interaction
1. Type: "I have a headache"
2. Click "Send"
3. Verify:
   - ✓ Message appears
   - ✓ Loading spinner shows
   - ✓ Response arrives
   - ✓ Follow-up suggestions appear

#### Test 4.3: Context Preservation
1. Go to Symptom page
2. Enter: "fever, cough"
3. Get results
4. Go to Chat page
5. Verify context is loaded from localStorage

---

### 5. Error Scenarios

#### Missing API Key
```bash
unset OPENAI_API_KEY
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"message": "Hi"}'
```
**Expected**: Error response with "API key not configured"

#### Network Timeout
- Disable network
- Try to send chat message
- **Expected**: Error message in UI

#### Invalid JSON
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d 'invalid'
```
**Expected**: 400 Bad Request

---

## Performance Benchmarks

| Operation | Target | Typical |
|-----------|--------|---------|
| Status Check | <100ms | 50ms |
| Explanation | <3s | 1.5-2s |
| Chat Response | <5s | 2-3s |
| Full Analysis | <10s | 5-7s |

---

## Success Criteria

- ✓ All endpoints return 200 status
- ✓ Responses include medical disclaimer
- ✓ Response times < 5 seconds
- ✓ Chat widget appears and functions
- ✓ Error messages display gracefully
- ✓ No console errors in browser
- ✓ Context preserves between pages

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 5000 is available
netstat -an | grep 5000

# Check for Python errors
python app.py -v
```

### Chat Widget Not Responding
```bash
# Check API status
curl http://localhost:5000/api/ai/status

# Check browser console
# F12 → Console tab for errors
```

### Slow Responses
- Check OpenAI API status: https://status.openai.com/
- Increase timeout in `llm_service.py`
- Check network connection

---

## Deployment Testing

Before production:
1. ✓ Test with fresh API key
2. ✓ Load test with multiple concurrent users
3. ✓ Test error handling thoroughly
4. ✓ Verify medical disclaimers
5. ✓ Test across browsers
6. ✓ Monitor API costs
7. ✓ Set up alerting for failures
