# React Chat UI - Quick Start Guide

## ⚡ Get Started in 5 Minutes

### Step 1: Setup Environment

```bash
cd frontend
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_URL=http://localhost:5000
```

### Step 2: Verify Backend is Running

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Flask API
cd backend
python chat_app.py

# You should see:
# 🏥 AI Health Assistant Backend API
# 🚀 Starting Flask server on port 5000
```

### Step 3: Update Your App

Replace your chat component with the improved version:

**Before:**
```jsx
import ChatWidget from './components/ChatWidget';

function App() {
  return <ChatWidget />;
}
```

**After:**
```jsx
import ChatWidgetImproved from './components/ChatWidgetImproved';

function App() {
  return <ChatWidgetImproved />;
}
```

### Step 4: Run Frontend

```bash
npm run dev

# Visit http://localhost:5173
```

### Step 5: Test Chat

1. Type a message: "I have a fever"
2. Click "Send" or press Enter
3. Wait for AI response
4. See response appear with response time

Done! 🎉

---

## 🔄 Migration from Old ChatWidget

If you're currently using the old `ChatWidget`, here's how to migrate:

### What Changed

| Aspect | Old | New |
|--------|-----|-----|
| API Endpoint | `/api/chat` (broken) | `http://localhost:5000/api/chat` (fixed) |
| Error Handling | Basic | Comprehensive with helpful messages |
| Loading State | Simple spinner | Spinner + cancel button |
| Message Duplicates | Possible | Prevented |
| Error Messages | Hardcoded | User-friendly, contextual |
| Hardcoded Responses | Yes, some | No, all real API responses |

### Migration Steps

1. **Backup old file:**
   ```bash
   cp src/components/ChatWidget.jsx src/components/ChatWidget.jsx.bak
   ```

2. **Replace import:**
   ```jsx
   // Old
   import ChatWidget from './components/ChatWidget';
   
   // New
   import ChatWidgetImproved from './components/ChatWidgetImproved';
   ```

3. **Update JSX:**
   ```jsx
   // Old
   <ChatWidget disease="Flu" symptoms={[...]} />
   
   // New
   <ChatWidgetImproved disease="Flu" symptoms={[...]} />
   ```

4. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

5. **Test everything works**

### What's Compatible

- ✅ Same component props (disease, symptoms, confidence, etc.)
- ✅ Same visual location in your UI
- ✅ Same styling context (Tailwind)
- ✅ Improved functionality, same interface

### What's Different

- ❌ Fewer hardcoded responses (only real API now)
- ❌ Better error messages
- ✅ Actual API connection working
- ✅ Auto-scroll that works properly
- ✅ No duplicate messages

---

## 📋 File Checklist

After setup, you should have:

```
frontend/
├── .env                              (✅ Created from .env.example)
├── .env.example                      (✅ Updated)
├── src/
│   ├── components/
│   │   ├── ChatListener.jsx          (existing)
│   │   ├── ChatWidget.jsx            (old - can keep as backup)
│   │   └── ChatWidgetImproved.jsx    (✅ NEW - use this!)
│   ├── hooks/
│   │   ├── useScrollToTop.js         (existing)
│   │   └── useHealthChat.js          (✅ NEW)
│   ├── services/
│   │   └── apiService.js             (✅ NEW)
│   ├── App.jsx                       (update to use ChatWidgetImproved)
│   └── main.jsx
├── package.json
├── vite.config.js
└── CHAT_UI_GUIDE.md                  (✅ NEW - detailed guide)
```

---

## 🧪 Quick Test

### Method 1: Browser Console

```javascript
// Open browser F12 → Console

// Test 1: Check API connection
const apiUrl = new URL('/api/chat', 'http://localhost:5000');
console.log('Testing:', apiUrl.toString());

// Test 2: Send test message
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello' })
})
.then(r => r.json())
.then(d => console.log('Response:', d))
.catch(e => console.error('Error:', e));
```

### Method 2: Inside React Component

```jsx
import { useEffect } from 'react';
import { checkAPIStatus } from './services/apiService';

export function TestComponent() {
  useEffect(() => {
    async function test() {
      const isRunning = await checkAPIStatus();
      console.log('API running:', isRunning);
    }
    test();
  }, []);

  return <div>Check console</div>;
}
```

### Method 3: From Terminal

```bash
# Test API is running
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","service":"AI Health Assistant",...}
```

---

## 🐛 Troubleshooting

### Issue: "Cannot reach API"

**Most Common Cause:** Backend isn't running

**Fix:**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Flask
cd ai-health-assistant/backend
python chat_app.py

# Check it's running
curl http://localhost:5000/api/health
```

### Issue: CORS Error

**Cause:** API URL is wrong
**Fix:**
1. Check `.env` file exists
2. Check `VITE_API_URL=http://localhost:5000`
3. Restart dev server: `npm run dev`

### Issue: Messages Aren't Sending

**Cause:** Input form issue
**Fix:**
1. Check browser console for errors (F12)
2. Check Network tab to see if request is sent
3. Check backend logs for response

### Issue: AI Isn't Responding

**Cause:** Ollama not running
**Fix:**
```bash
# Check Ollama
ollama serve

# Check model is loaded
ollama ps

# Should show llama3 in use
```

### Issue: Very Slow Responses

**Cause:** Model is loading (first request) or system under load
**Fix:**
1. First request may take 5-10 seconds
2. Subsequent requests are faster (2-4 seconds)
3. Close other applications
4. Check CPU/memory usage

---

## 📚 Next Steps

### For Basic Setup
✅ Just want it to work?
- Follow "Step 1-5" above
- Everything else is optional

### For Customization
- Read `CHAT_UI_GUIDE.md` for detailed customization
- Modify colors, timeout, messages, etc.

### For Advanced Integration
- Use `useHealthChat` hook in custom components
- Use `apiService` functions directly
- Build your own UI around the hook

### For Troubleshooting
- Check `CHAT_UI_GUIDE.md` Debugging section
- Check backend logs: `python chat_app.py`
- Check browser console: F12 → Console
- Check network requests: F12 → Network → XHR

---

## ✨ You're All Set!

The improved chat UI is ready to use. It:
- ✅ Connects to the real API
- ✅ Handles errors properly
- ✅ Shows real AI responses (no hardcoding)
- ✅ Has modern UI
- ✅ Auto-scrolls correctly
- ✅ Prevents duplicates

**Start chatting!** 💬🏥

---

## 💡 Pro Tips

1. **First request is slow** - The Ollama model needs to load (5-10s)
2. **Use keyboard** - Press Enter to send, Shift+Enter for new line
3. **View response time** - Shown in AI messages (⏱️ 2.45s)
4. **Check stats** - Visit `http://localhost:5000/api/stats` to see API usage
5. **Read errors** - Error messages are helpful, don't ignore them

---

**Questions?** Check:
- `CHAT_UI_GUIDE.md` - Full documentation
- Backend guide: `ai-health-assistant/backend/CHAT_API_SETUP.md`
- Flask API code: `ai-health-assistant/backend/chat_app.py`

Happy building! 🚀
