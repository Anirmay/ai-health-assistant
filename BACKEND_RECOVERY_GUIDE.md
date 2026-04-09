# Backend Not Responding - Complete Recovery Guide

## Current Problem
Frontend shows:
- ❌ "Server error: Internal Server Error" 
- ❌ "AI is not responding right now"

This means the backend Ollama integration is failing.

## Quick Fix (5 minutes)

### Step 1: Run Diagnostic (Find the problem)
```bash
cd backend
python diagnose.py
```

This will check:
- ✅ Is Ollama running?
- ✅ Does gemma:2b model exist?
- ✅ Is Flask running?
- ✅ Are the code changes in place?
- ✅ Can we call Ollama directly?

**Fix issues as shown** before continuing.

### Step 2: Stop Everything

**Terminal 1** (If backend is running):
```bash
CTRL + C
```

**Terminal 2** (If Ollama is running):
```bash
CTRL + C
# Wait 5 seconds for clean shutdown
```

### Step 3: Start Fresh

**Terminal 1 - Start Ollama**:
```bash
ollama serve
# Wait for: "Listening on 127.0.0.1:11434"
```

**Terminal 2 - Verify gemma:2b**:
```bash
ollama list
# Should show: gemma:2b
# If not: ollama pull gemma:2b
```

**Terminal 3 - Start Backend**:
```bash
cd backend
python app.py
```

**YOU SHOULD SEE IN TERMINAL 3**:
```
✅ Ollama Service initialized: gemma:2b model, 40s timeout, 70 tokens max
⚠️  Ollama response check passed!
 * Running on http://127.0.0.1:5000
```

### Step 4: Test Chat in Frontend

Browser: `http://localhost:5173`

Type: "Hi"

**YOU SHOULD SEE IN TERMINAL 3** during chat:

```
======================================================================
🔍 OLLAMA DEBUG - STEP 1: Checking Ollama availability...
   is_available property: True

🔍 OLLAMA DEBUG - STEP 2: Building request...
   URL: http://localhost:11434/api/generate
   Model: gemma:2b

🔍 OLLAMA DEBUG - STEP 3: Sending POST request...
   Timeout: 40 seconds

🔍 OLLAMA DEBUG - STEP 4: Got response!
   Status code: 200

🔍 OLLAMA DEBUG - STEP 5: Parsing JSON response...
   JSON parsed successfully!

✅ SUCCESS! Got AI response (XX chars)
======================================================================
```

### Step 5: If Still Not Working

**Option A: Run Direct Test**
```bash
cd backend
python test_direct_ollama.py
```

Should show:
```
✅ Ollama is reachable
✅ Model gemma:2b is available
✅ Got AI response
✅ ALL TESTS PASSED
```

**Option B: Check Terminal Output**

Look for these in backend terminal:

| Message | Meaning | Fix |
|---------|---------|-----|
| `is_available property: False` | Ollama not running | Start: `ollama serve` |
| `❌ CONNECTION ERROR` | Can't reach Ollama | Check: `ollama serve` |
| `❌ TIMEOUT ERROR (40s)` | Ollama too slow | Wait longer or restart |
| `Status code: 500` | Ollama error | Check model |
| `Response field was EMPTY` | No response from Ollama | Restart Ollama |
| `✅ SUCCESS! Got AI response` | **WORKING!** | Chat should work now |

## Full Installation (If Still Failing)

### 1. Update Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Make sure you have:
- flask
- requests  
- flask-cors
- python-dotenv

### 2. Verify .env Configuration

```bash
cd backend
cat .env
```

Should contain (at minimum):
```
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b
OLLAMA_TIMEOUT=40
```

If not, copy from template:
```bash
cp .env.example .env
```

### 3. Completely Restart Ollama

```bash
# Kill all ollama processes
pkill ollama
sleep 5

# Start fresh
ollama serve

# In another terminal, verify
ollama list

# If gemma:2b not there
ollama pull gemma:2b
```

### 4. Clear Python Cache

```bash
cd backend
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
rm -rf *.pyc
```

### 5. Restart Backend Fresh

```bash
cd backend
python app.py
```

## Testing Checklist

Check each of these **IN ORDER**:

- [ ] Ollama is running: `ollama list` shows gemma:2b
- [ ] Backend is running: Terminal shows initialization logs
- [ ] Debug logs appear: Terminal shows "OLLAMA DEBUG - STEP" when chatting
- [ ] Diagnostic passes: `python diagnose.py` shows all ✅
- [ ] Direct test passes: `python test_direct_ollama.py` says "PASSED"
- [ ] Chat endpoint works: curl test returns 200 with response

## Expected Timeline

1. **0-1 min**: Run diagnosis
2. **1-2 min**: Fix any issues (restart services)
3. **2-5 min**: Start Ollama, verify gemma:2b, start backend
4. **5-10 min**: Watch for debug output, test chat
5. **10+ min**: Everything working!

## Files That Matter

```
backend/
├── app.py                          ← /api/chat endpoint (should handle errors)
├── ai_module/
│   └── ollama_service.py           ← _call_ollama() with debug (40s timeout, gemma:2b)
├── .env                            ← Config (copy from .env.example)
├── diagnose.py                     ← Run this to find problems
├── test_direct_ollama.py           ← Tests Ollama directly
└── requirements.txt                ← Python dependencies
```

## Emergency Debug

If completely stuck, add this to backend/app.py after imports:

```python
import sys

# Force debug output
sys.stdout = sys.stderr
print("DEBUG: Flask starting up...", flush=True)
```

Then run:
```bash
python app.py 2>&1 | tee backend_debug.log
```

This will print all output to both terminal AND save to `backend_debug.log`

## Success Indicators

✅ **YOU'LL KNOW IT'S WORKING WHEN**:

1. **Terminal output**:
   ```
   ✅ Ollama Service initialized
   ✅ SUCCESS! Got AI response
   ```

2. **Chat responses**:
   - "Hi" → Gets AI greeting
   - "Tell me a joke" → Gets AI joke
   - "I have fever" → Gets health advice

3. **No errors**:
   - Frontend shows responses (not error messages)
   - Backend terminal shows "STEP" debug (not error messages)
   - Curl returns 200 status (not 500)

## Final Sanity Check

Run all three at once (three terminals):

```bash
# Terminal 1
ollama serve

# Terminal 2  
cd backend && python app.py

# Terminal 3
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi"}'
```

Should return JSON with real AI response in < 5 seconds.

---

**Still not working?** 
- Check all ✅ in diagnostic output
- Share the debug output from backend terminal
- Verify gemma:2b is installed: `ollama list`
- Make sure ports 11434 (Ollama) and 5000 (Flask) are free
