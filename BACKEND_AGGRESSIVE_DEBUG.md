# Backend Ollama Debugging - Aggressive Debug Mode Enabled

## Changes Made

All backend code now has **aggressive print statements** showing exactly what's happening at each step.

### 1. Model Configuration
- ✅ **Model**: `gemma:2b` (confirmed)
- ✅ **Timeout**: 40 seconds (increased from 30 for slower model)
- ✅ **Max tokens**: 70 per response
- ✅ **Stream**: False (full response, not streaming)

### 2. _call_ollama() Method - FULL DEBUG

Now prints **STEP-BY-STEP** debugging information:

```
=========================================================================
🔍 OLLAMA DEBUG - STEP 1: Checking Ollama availability...
   is_available property: True

🔍 OLLAMA DEBUG - STEP 2: Building request...
   URL: http://localhost:11434/api/generate
   Model: gemma:2b
   Max tokens: 70
   Prompt length: 243 chars
   Prompt preview: You are a helpful assistant...

🔍 OLLAMA DEBUG - STEP 3: Sending POST request...
   URL: http://localhost:11434/api/generate
   Timeout: 40 seconds
   Payload size: 487 bytes

🔍 OLLAMA DEBUG - STEP 4: Got response!
   Status code: 200
   Response length: 256 bytes
   Raw response text: {"model":"gemma:2b","created_at":"2026-04-09T...","response":"Hello! How can I help you?","done":true}

🔍 OLLAMA DEBUG - STEP 5: Parsing JSON response...
   JSON parsed successfully!
   JSON keys: ['model', 'created_at', 'response', 'done']
   Full JSON: {...}
   Response field length: 28 chars
   Response field: Hello! How can I help you?

✅ SUCCESS! Got AI response (28 chars)
=========================================================================
```

### 3. chat_answer() Method - DEBUG WRAPPER

Now prints each step of conversation processing:

```
**********************************************************************
💬 CHAT ANSWER - Received message: Hi
🔍 Checking if Ollama available...
   Ollama available: True
🔍 Building prompt...
📝 Final prompt: 243 chars
   Prompt preview: You are a helpful...
🔄 Calling _call_ollama()...
✅ _call_ollama returned: <class 'str'> (value: 'Hello! How...')
✅ Got answer from AI: 28 chars
✅ After cleanup: 28 chars
✅ CHAT SUCCESS - Returning: {'answer': '...', 'follow_up_...'}
**********************************************************************
```

### 4. Flask Endpoint - ENHANCED LOGGING

Flask `/api/chat` endpoint now prints:
```
💬 Chat request: Hi
🔍 Flask: Got ollama_service instance
🔄 Flask: Calling ollama_service.chat_answer()...
✅ Flask: Got response from Ollama
```

## How to Use This

### Step 1: Restart Backend with Visible Output

```bash
cd backend
python app.py
```

You should see backend logs IN THE TERMINAL (not logs file):
```
✅ Ollama Service initialized: gemma:2b model, 40s timeout, 70 tokens max
⚠️  Ollama response check passed!
...
```

### Step 2: Open Another Terminal and Test

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi"}'
```

### Step 3: Watch Backend Terminal

You should see **5 STEPS** of debugging output print to the terminal showing:
- ✅ Ollama is available
- ✅ Request built correctly
- ✅ Request sent with 40s timeout
- ✅ Response received (status 200)
- ✅ JSON parsed successfully
- ✅ Response extracted from "response" field
- ✅ AI response returned to Flask

## What Each Debug Output Means

### Good Signs ✅

**Ollama Available**:
```
🔍 OLLAMA DEBUG - STEP 1: Checking Ollama availability...
   is_available property: True
```
→ Ollama is running and reachable

**Request Sent**:
```
🔍 OLLAMA DEBUG - STEP 3: Sending POST request...
   URL: http://localhost:11434/api/generate
   Timeout: 40 seconds
```
→ Backend is sending request to Ollama

**Response Received**:
```
🔍 OLLAMA DEBUG - STEP 4: Got response!
   Status code: 200
```
→ Ollama responded successfully (200 = OK)

**JSON Parsed**:
```
🔍 OLLAMA DEBUG - STEP 5: Parsing JSON response...
   JSON parsed successfully!
```
→ Response is valid JSON

**Got Answer**:
```
✅ SUCCESS! Got AI response (28 chars)
```
→ AI response extracted and returned

### Bad Signs ❌

**Ollama Not Available**:
```
🔍 OLLAMA DEBUG - STEP 1: Checking Ollama availability...
   is_available property: False
❌ Ollama service NOT available - returning None
```
→ **Fix**: Start Ollama: `ollama serve`

**Connection Error**:
```
❌ CONNECTION ERROR: [Errno 111] Connection refused
   Is Ollama running at http://localhost:11434?
```
→ **Fix**: Start Ollama: `ollama serve`

**Timeout**:
```
❌ TIMEOUT ERROR (40s): HTTPConnectionPool(host='localhost', port=11434): Read timed out.
```
→ **Fix**: Ollama is slow, wait longer or check if stuck

**Status Not 200**:
```
❌ Response status NOT 200: 500
   Response: Error loading model
```
→ **Fix**: Model issue, check: `ollama list`

**JSON Parse Error**:
```
❌ JSON parse error: JSONDecodeError: Expecting value: line 1 column 1
   Raw response was: Connection refused
```
→ **Fix**: Ollama not responding

**Response Field Empty**:
```
❌ Response field was EMPTY - returning None
```
→ **Fix**: Ollama returned but no text in "response" field

## Debugging Workflow

### If You See "AI is not responding right now":

**Step 1 - Check Terminal Output**
- Does backend terminal show 5 STEPS of debugging?
- If no output, endpoint wasn't called or crashed

**Step 2 - Check STEP 1 (Availability)**
- Does it say `is_available property: True`?
- If False → Ollama not running or unreachable

**Step 3 - Check STEP 4 (Response)**
- Does it say `Status code: 200`?
- If not 200 → Ollama error

**Step 4 - Check STEP 5 (JSON Parse)**
- Does it say `JSON parsed successfully!`?
- If error → Response format wrong

**Step 5 - Check SUCCESS**
- Does it say `✅ SUCCESS! Got AI response`?
- If no → Answer is None somewhere

### If You See TIMEOUT Error:

```bash
# Check if Ollama is responding
curl http://localhost:11434/api/tags

# If no response, Ollama is stuck
# SOLUTION: Restart Ollama
pkill ollama
sleep 2
ollama serve
```

### If You See CONNECTION ERROR:

```bash
# Check if Ollama is running
ollama list

# If command fails, Ollama not running
# SOLUTION: Start it
ollama serve
```

### If You See Model Not Found:

```bash
# Check available models
ollama list

# If gemma:2b not listed
# SOLUTION: Pull it
ollama pull gemma:2b
```

## Complete Testing Sequence

### 1. Start Ollama (Terminal 1)
```bash
ollama serve
# Should show: Listening on 127.0.0.1:11434
```

### 2. Verify gemma:2b (Terminal 2)
```bash
ollama list
# Should show: gemma:2b
```

### 3. Start Backend with Debug (Terminal 3)
```bash
cd backend
python app.py
# Should show: ✅ Ollama Service initialized: gemma:2b model, 40s timeout
```

### 4. Test Chat with Curl (Terminal 4)
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi"}'
```

### 5. Watch Backend Terminal (Terminal 3)

Should print 5-step debug flow showing SUCCESS

### 6. Test Frontend (Browser)
```
http://localhost:5173
Chat: "Hi"
Should get instant response!
```

## Environment Variables

Make sure `.env` has correct settings:

```bash
# Required - MUST use gemma:2b
OLLAMA_MODEL=gemma:2b

# Timeout - gemma:2b needs up to 40 seconds
OLLAMA_TIMEOUT=40
LLM_RESPONSE_TIMEOUT=40

# Optional - default values
OLLAMA_API_URL=http://localhost:11434
LLM_TEMPERATURE=0.3
LLM_NUM_PREDICT=70
```

## Common Issues & Fixes

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| "AI is not responding" | Ollama not running | `ollama serve` |
| Connection refused | Wrong port or address | Check `localhost:11434` |
| Timeout (40s) | Ollama stuck or very slow | Restart Ollama |
| Model not found | gemma:2b not pulled | `ollama pull gemma:2b` |
| Status 500 | Backend crash | Check Flask logs for exceptions |
| Empty response | Ollama returned but no text | Model issue, try restarting |
| JSON parse error | Response format wrong | Ollama version issue |

## Files Modified

| File | Changes |
|------|---------|
| `ollama_service.py` | Added 5-step print debug in _call_ollama() |
| `ollama_service.py` | Added wrapper print debug in chat_answer() |
| `ollama_service.py` | Updated timeout to 40s |
| `ollama_service.py` | Updated model references to gemma:2b |
| `app.py` | Added Flask endpoint debug prints |
| `.env.example` | Updated OLLAMA_TIMEOUT to 40 |

## Expected Output Flow

When everything works:

### Terminal 1 (Ollama)
```
Listening on 127.0.0.1:11434
```

### Terminal 3 (Backend)
```
✅ Ollama Service initialized: gemma:2b model, 40s timeout, 70 tokens max
⚠️  Ollama response check passed!

[After curl test]

=========================================================================
🔍 OLLAMA DEBUG - STEP 1: Checking Ollama availability...
   is_available property: True
...5 STEP FLOW...
✅ SUCCESS! Got AI response (28 chars)
=========================================================================
```

### Terminal 4 (Curl/Browser)
```
{"status":"success","user_message":"Hi","ai_response":{"answer":"Hello! How can I help you?","follow_up_suggestions":["Tell me your symptoms","What can I do to help?"]}}
```

## Key Takeaways

✅ **Model**: `gemma:2b` (1.4GB, lightweight)
✅ **Timeout**: 40 seconds (gemma:2b is slow)
✅ **Debug**: FULL print statements showing each step
✅ **Endpoint**: /api/chat always returns 200 + valid JSON
✅ **Fallback**: Only used when answer is genuinely None

---

**Status**: ✅ Aggressive debug mode enabled
**Next**: Restart backend and watch terminal output!
