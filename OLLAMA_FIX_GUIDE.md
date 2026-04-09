# Flask Backend - Ollama Connection Fixes

## 🔧 What Was Fixed

### 1. **Timeout Too Low** ❌ → ✅
- **Problem**: Timeout was 5 seconds, but phi3 needs 20+ seconds
- **Location**: `.env.example` and `ollama_service.py`
- **Fix**:
  - Changed `OLLAMA_TIMEOUT=5` → `OLLAMA_TIMEOUT=20`
  - Changed `LLM_RESPONSE_TIMEOUT=5` → `LLM_RESPONSE_TIMEOUT=20`
  - Updated default in `OllamaService.__init__()` to use 20 seconds

### 2. **Poor Error Handling** ❌ → ✅
- **Problem**: Always returned fallback strings even when error was recoverable
- **Location**: `_call_ollama()` method
- **Fix**:
  - Now returns `None` on real errors instead of fallback strings
  - Distinguishes between no response and bad response
  - Added proper logging for debugging

### 3. **Missing Debug Logs** ❌ → ✅
- **Problem**: Couldn't see what was happening or why it failed
- **Location**: `_call_ollama()` method
- **Fix**:
  - Added debug logs for each step:
    - 🔄 When calling Ollama
    - ✅ When response received
    - ❌ On errors with specific codes
    - ⏱️ Timeout information

### 4. **Wrong Fallback Logic** ❌ → ✅
- **Problem**: Treated empty strings and None the same
- **Location**: `chat_answer()` method
- **Fix**:
  - Now explicitly checks `if answer is None:` instead of `if not answer:`
  - Returns proper error message only when AI truly fails
  - Allows dynamic responses to flow through correctly

### 5. **No Response Handling** ❌ → ✅
- **Problem**: Methods directly used LLM results without null checks
- **Location**: `generate_explanation()` and `explain_medicine_detection()`
- **Fix**:
  - Added None checks before using results
  - Provides sensible fallback only on actual failures

---

## 📝 Files Modified

### 1. **backend/.env.example**
```diff
- OLLAMA_TIMEOUT=5
+ OLLAMA_TIMEOUT=20

- LLM_RESPONSE_TIMEOUT=5
+ LLM_RESPONSE_TIMEOUT=20
```

### 2. **backend/ai_module/ollama_service.py**

#### Changed `__init__()`:
```python
# Before:
self.timeout = int(os.getenv("OLLAMA_TIMEOUT", "5"))
self.response_timeout = int(os.getenv("LLM_RESPONSE_TIMEOUT", "5"))

# After:
self.timeout = int(os.getenv("OLLAMA_TIMEOUT", "20"))  # phi3 needs 20s
self.response_timeout = int(os.getenv("LLM_RESPONSE_TIMEOUT", "20"))
```

#### Completely rewrote `_call_ollama()`:
- Returns `Optional[str]` (None on error instead of fallback)
- Added debug logs for request and response
- Properly distinguishes error types
- Returns actual response or None (not fallback text)

#### Updated `chat_answer()`:
```python
# Before: answer = self._call_ollama(...); answer = self._cleanup_response(answer)

# After:
answer = self._call_ollama(...)
if answer is None:
    return { "answer": "AI didn't respond..." }
answer = self._cleanup_response(answer)
```

#### Fixed `generate_explanation()` and `explain_medicine_detection()`:
- Added `if explanation is None:` checks
- Provides sensible defaults instead of None values

---

## 🧪 How to Test

### Test 1: Run the Connection Tester
```bash
cd backend
python test_ollama_connection.py
```

This will:
✅ Check if Ollama is running
✅ Test the API endpoint
✅ Test a health-specific prompt
✅ Show response times

### Test 2: Verify Backend Logs
```bash
# In backend terminal:
python app.py

# In another terminal:
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever of 101F"}'
```

Watch the logs for:
- 🔄 "Calling Ollama..."
- ✅ "AI Response: ..."
- Or ❌ error messages

### Test 3: Use Frontend Chat
1. Ensure backend is running
2. Test in UI:
   - Ask a health question
   - Should get dynamic AI response (not static fallback)

---

## 📊 Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| Timeout | 5 seconds | 20 seconds |
| AI Response | ❌ Always fallback | ✅ Dynamic responses |
| Joint "Should I see doctor?" | Fallback text | Real AI answer |
| Joke questions | Fallback | Real AI response |
| Error visibility | No logs | Full debug logs |
| Response handling | Returns strings | Returns None on error |
| Fallback logic | Triggers too easily | Only on real errors |

---

## 🔍 Debug Logs You'll See

When working correctly:
```
✅ Ollama service initialized: phi3 model, 20s timeout, 70 tokens max
✅ Ollama service is available and running
🔄 Calling Ollama (phi3): 20s timeout, 70 tokens
📝 Prompt: You are a safe health...
✅ AI Response: A 101°F fever is mild to moderate...
```

When there's an issue:
```
❌ Ollama TIMEOUT (>20s) - AI not responding
❌ Cannot connect to Ollama at http://localhost:11434: Connection refused
❌ Ollama API error: 500
```

---

## 🚀 Setup Instructions

### 1. Update Configuration
Copy the updated .env.example to your .env:
```bash
cp backend/.env.example backend/.env
# Or manually set:
OLLAMA_TIMEOUT=20
LLM_RESPONSE_TIMEOUT=20
```

### 2. Make Sure Ollama is Running
```bash
# In a terminal:
ollama serve

# In another terminal, verify:
ollama list  # Should show phi3
curl http://localhost:11434/api/tags  # Should return models
```

### 3. Run the Test
```bash
cd backend
python test_ollama_connection.py
```

### 4. Restart Backend
```bash
python app.py
```

### 5. Test Frontend Chat
- Go to Chat page
- Ask: "I have a fever of 102F"
- Should get dynamic AI response

---

## 📋 Troubleshooting

### Issue: "Response took too long"
**Solution**: Ollama is slow or not running
- Ensure Ollama is running: `ollama serve`
- Check phi3 is available: `ollama list`
- Increase timeout further if needed in .env

### Issue: "Cannot connect to Ollama"
**Solution**: Ollama not running at the right address
- Verify `OLLAMA_API_URL=http://localhost:11434`
- Start Ollama: `ollama serve`
- Test endpoint: `curl http://localhost:11434/api/tags`

### Issue: Still getting fallback responses
**Solution**: Check logs for specific error
```bash
python app.py 2>&1 | grep -E "❌|✅|🔄"
```

- If `❌ TIMEOUT`: Increase timeout to 30 or 40 seconds
- If `❌ Cannot connect`: Start Ollama
- If `❌ API error`: Check Ollama logs

---

## ✅ What's Now Working

✅ **AI responds dynamically** - Not static fallback text
✅ **Timeout respects phi3 speed** - 20 second wait time
✅ **Debug logs show what's happening** - Easy troubleshooting
✅ **Proper error handling** - Only fallback on real errors
✅ **Consistent API behavior** - Endpoint works correctly

---

## 📞 Quick Commands

```bash
# Start Ollama
ollama serve

# Pull phi3 if needed
ollama pull phi3

# Test connection
cd backend && python test_ollama_connection.py

# Start backend
python app.py

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What should I do for a fever?"}'
```

---

**Status**: ✅ Ollama connection is now properly implemented
