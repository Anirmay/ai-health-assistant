# Chat API - Complete System Guide

## 📋 What is This?

This is a **production-ready REST API** for health-related chat conversations using:
- **Flask** - Lightweight, fast web framework
- **Ollama** - Local LLM running Llama3 model
- **Python** - Clean, maintainable code
- **CORS** - Enabled for React frontend

---

## 🎯 What Problem Does It Solve?

### Before (Without Chat API)
- Complex app.py with multiple features mixed together
- Hard to maintain and debug
- Difficult to integrate with React frontend
- Unclear dependencies between features
- Slow startup time due to loading all ML models

### After (With Chat API)
- ✅ Focused, single-purpose Chat API
- ✅ Easy to understand and maintain
- ✅ Clean REST endpoints
- ✅ Fast startup time
- ✅ Easy to integrate with React
- ✅ Scalable architecture

---

## 🏗️ Architecture

### Two Parallel Systems

```
┌─────────────────────────────────────┐
│   AI Health Assistant Backend       │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────┐                   │
│  │  chat_app.py │ (Focused)         │
│  │  /api/chat   │ REST API          │
│  │  Fast & Simple                   │
│  └──────┬───────┘                   │
│         │                           │
│         ├─→ ollama_chat.py          │
│         │   (Clean Service)         │
│         │                           │
│         └─→ Ollama API              │
│            localhost:11434          │
│                                     │
│  ┌──────────────┐                   │
│  │   app.py     │ (Comprehensive)   │
│  │  /api/sympt  │ Full Application  │
│  │  /api/verif  │ ML + Analysis     │
│  │  Slower      │                   │
│  └──────────────┘                   │
│                                     │
└─────────────────────────────────────┘
           │
           ├─→ React Frontend (5173)
           │
           └─→ Database (SQLite)
```

### File Structure

```
backend/
├── 📄 chat_app.py                    ◄── NEW: Chat API (start here!)
├── 📄 ollama_chat.py                 ◄── NEW: Ollama integration
├── 📄 app.py                         ◄── Original: Full app
│
├── 📖 CHAT_API_SETUP.md              ◄── NEW: Complete setup guide
├── 📖 IMPLEMENTATION_SUMMARY.md      ◄── NEW: What & why
├── 📖 QUICK_REFERENCE.md            ◄── NEW: Quick commands
│
├── 🧪 test_chat_api.py              ◄── NEW: Test suite
│
├── 🚀 start.sh                       ◄── NEW: Linux/macOS launcher
├── 🚀 start.bat                      ◄── NEW: Windows CMD launcher
├── 🚀 start.ps1                      ◄── NEW: Windows PowerShell launcher
│
├── ⚙️ requirements.txt                ▲ Updated: Added dependencies
├── 🔧 .env.example                   ▲ Updated: New chat settings
│
├── ai_module/
│   ├── ollama_service.py             (Existing: Legacy)
│   ├── health_ai.py                  (Existing)
│   └── llm_service.py                (Existing)
│
├── ml_models/                        (Existing: Symptom analysis)
└── database.py                       (Existing: Database models)
```

---

## 🎓 Which API Should I Use?

### Use `chat_app.py` if you:
✅ Want simple, fast health chat  
✅ Just need conversation interface  
✅ Care about speed and simplicity  
✅ Integrating with React frontend  
✅ Running on limited resources  

### Use `app.py` if you:
✅ Need symptom analysis  
✅ Want medicine verification  
✅ Need disease prediction  
✅ Want full feature suite  
✅ Have adequate resources (ML models)  

### Use Both if you:
✅ Want chat + detailed analysis  
✅ Have resources for both  
✅ Need flexibility  

---

## 🚀 Getting Started

### 1. Setup (One Time)

```bash
# Install Ollama
# Download from https://ollama.ai

# Pull the model
ollama pull llama3

# Install Python dependencies
pip install -r requirements.txt

# Copy configuration
cp .env.example .env

# Edit .env if needed (optional)
# Default settings are good for most cases
```

### 2. Start the API

**Windows:**
```cmd
start.bat
```

**Linux/macOS:**
```bash
bash start.sh
```

**Manual (Any OS):**
```bash
# Terminal 1
ollama serve

# Terminal 2
python chat_app.py
```

### 3. Test It

```bash
# Run full test suite
python test_chat_api.py

# Or test individually
curl http://localhost:5000/api/health
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever"}'
```

---

## 💡 Core Concepts

### The Prompt

The system prompt in `ollama_chat.py` controls how the AI behaves:

```python
system_prompt = """You are a smart, helpful health assistant. Your role is to:
1. Provide SHORT, PRACTICAL health advice (3-5 lines only)
2. Never repeat the user's question back to them
3. Suggest possible causes and simple home remedies
4. Recommend seeing a doctor if the condition seems serious
..."""
```

This ensures:
- Concise responses
- No repetition
- Practical advice
- Medical safety

### The Request Flow

```
User Message
    ↓
[chat_app.py]
    ↓
Parse JSON: {"message": "user input"}
    ↓
[ollama_chat.py]
    ↓
Build system prompt + user message
    ↓
POST to Ollama API
    ↓
Wait for response (30s timeout)
    ↓
Parse response
    ↓
Return to frontend
    ↓
React displays: { "reply": "AI advice" }
```

### Error Handling

All errors return helpful messages:

```json
{
  "reply": "I can't connect to the AI service...",
  "status": "error",
  "error": "connection_failed"
}
```

Never returns HTTP 500 - always HTTP 200 with status in JSON.

---

## 🔌 Integration with React

### Basic Setup

```javascript
// api.js
const API_URL = 'http://localhost:5000/api';

export async function chatWithAI(message) {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message })
  });
  
  if (!response.ok) {
    throw new Error('API request failed');
  }
  
  return response.json();
}
```

### React Hook

```javascript
// useHealthChat.js
import { useState } from 'react';
import { chatWithAI } from './api';

export function useHealthChat() {
  const [reply, setReply] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const sendMessage = async (message) => {
    setLoading(true);
    setError('');
    
    try {
      const result = await chatWithAI(message);
      
      if (result.status === 'success') {
        setReply(result.reply);
      } else {
        setError(result.reply);
      }
    } catch (err) {
      setError('Failed to connect to API');
    } finally {
      setLoading(false);
    }
  };

  return { sendMessage, reply, loading, error };
}
```

### React Component

```javascript
import { useState } from 'react';
import { useHealthChat } from './useHealthChat';

function HealthChat() {
  const [input, setInput] = useState('');
  const { sendMessage, reply, loading, error } = useHealthChat();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      await sendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="chat-container">
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me a health question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
      
      {error && <div className="error">{error}</div>}
      {reply && <div className="reply">{reply}</div>}
     
    </div>
  );
}

export default HealthChat;
```

---

## ⚙️ Configuration Guide

### Performance Tuning

**For Faster Responses:**
```env
OLLAMA_TIMEOUT=20           # Reduce wait time
OLLAMA_TEMPERATURE=0.7      # Less creativity = faster
```

**For Better Quality:**
```env
OLLAMA_TIMEOUT=40           # Give more time
OLLAMA_TEMPERATURE=0.95     # More creativity
```

**For No Repetition:**
```env
OLLAMA_REPEAT_PENALTY=1.5   # Increase penalty
```

### Model Selection

Each Ollama model has trade-offs:

| Model | Speed | Quality | Size | RAM |
|-------|-------|---------|------|-----|
| mistral | Fast | Good | 4GB | 8GB |
| neural-chat | Fast | Good | 5GB | 8GB |
| llama3 | Medium | Excellent | 5GB | 8GB |
| llama2 | Medium | Good | 4GB | 8GB |

```bash
# Try different models
ollama pull mistral
ollama pull neural-chat

# Update .env
OLLAMA_MODEL=mistral
```

---

## 📊 Monitoring & Debug

### Check Status
```bash
# API health
curl http://localhost:5000/api/health

# Ollama status
curl http://localhost:5000/api/status

# API configuration
curl http://localhost:5000/api/config

# Usage statistics
curl http://localhost:5000/api/stats
```

### View Logs

Logs appear in terminal where you started `python chat_app.py`:

```
✅ Ollama service is available
🔄 [Request #1] User: I have a fever...
📤 Sending request to http://localhost:11434/api/generate
✅ [Request #1] Response received in 2.45s (256 chars)
💬 AI Reply: Here are some steps...
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Cannot connect" | Start Ollama: `ollama serve` |
| "Very slow" (>10s) | Close other apps, more RAM |
| "Empty responses" | Check Ollama is responding |
| "Repetitive answers" | Increase `REPEAT_PENALTY` |
| "Generic answers" | Increase `TEMPERATURE` |

---

## 🧪 Testing Strategy

### Unit Tests (Provided)
```bash
# Run all 8 tests
python test_chat_api.py

# Tests: health check, status, config, chat, errors, stats, CORS
```

### Manual Testing
```bash
# Simple test
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a sore throat"}'
```

### Load Testing (If needed)
```bash
# Using Apache Bench
ab -n 10 -c 2 http://localhost:5000/api/chat

# Using Python requests
python -c "
import requests
import concurrent.futures

def test_chat():
    return requests.post(
        'http://localhost:5000/api/chat',
        json={'message': 'Test'},
        timeout=35
    )

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as e:
    futures = [e.submit(test_chat) for _ in range(10)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
    print(f'Success: {sum(1 for r in results if r.status_code == 200)}/10')
"
```

---

## 🚢 Production Deployment

### Server Setup
```bash
# Install on server
pip install -r requirements.txt
pip install gunicorn

# Create .env with production settings
FLASK_DEBUG=False
OLLAMA_TIMEOUT=30
```

### Run with Gunicorn
```bash
# Single worker
gunicorn --bind 0.0.0.0:5000 chat_app:app

# Multiple workers
gunicorn --workers 4 --bind 0.0.0.0:5000 chat_app:app

# With gevent for async
gunicorn --workers 4 --worker-class gevent \
  --bind 0.0.0.0:5000 chat_app:app
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker (Optional)
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "chat_app:app"]
```

---

## 📚 Documentation Map

| Document | Purpose |
|----------|---------|
| **CHAT_API_SETUP.md** | Complete setup guide (8000+ words) |
| **IMPLEMENTATION_SUMMARY.md** | What was created and why |
| **QUICK_REFERENCE.md** | Quick commands and examples |
| **README.md** (This file) | System overview |

---

## 🎯 Common Tasks

### Change response style
Edit `_build_health_prompt()` in `ollama_chat.py`

### Adjust response length
Change "3-5 lines" to your preference in the prompt

### Add conversation history
Extend chat() method to accept context parameter

### Cache responses
Add Redis or in-memory cache for repeated questions

### Add authentication
Use JWT tokens or API keys

### Monitor performance
Set up logging to file and use `/api/stats` endpoint

---

## 🔗 Real-World Example

### Health Check Flow
```
React Component
    ↓
Button Click: "Ask AI"
    ↓
Input: "I have a sore throat"
    ↓
Fetch: POST /api/chat
    ↓
Flask receives JSON
    ↓
OllamaChatService.chat()
    ↓
Build prompt with system message
    ↓
POST to Ollama at localhost:11434/api/generate
    ↓
Ollama processes with llama3 model
    ↓
Returns response (~2-4 seconds)
    ↓
Clean up response
    ↓
Return JSON with "reply" field
    ↓
React receives response
    ↓
Display in UI: "Here's what I suggest..."
```

---

## ✨ Key Features Summary

- **Smart Prompting** - System message controls AI behavior
- **Fast & Lightweight** - No heavy ML models loaded
- **Error Resilient** - Graceful handling of all failures
- **Fully Logged** - Track requests and responses
- **CORS Enabled** - Easy React integration
- **Stateful** - Track API statistics
- **Production Ready** - Deployable with Gunicorn
- **Well Documented** - 9000+ words of docs
- **Fully Tested** - 8 test modules included
- **Easy Setup** - Automated startup scripts

---

## 🎓 Learning Path

1. **Start Here:** Read this README
2. **Quick Setup:** Follow QUICK_REFERENCE.md
3. **Deep Dive:** Read CHAT_API_SETUP.md
4. **Understand Implementation:** Review ollama_chat.py code
5. **See Examples:** Check test_chat_api.py
6. **Run Tests:** `python test_chat_api.py`
7. **Integrate Frontend:** Use React examples
8. **Deploy:** Follow production guide

---

## 💬 Get Help

### Common Questions

**Q: Can I use a different model?**
A: Yes! Install with `ollama pull <model>` and update `.env`

**Q: How do I make it faster?**
A: Lower timeout, reduce temperature, close other apps

**Q: Can I store chat history?**
A: Yes, extend the code to store messages in database

**Q: Is it production-ready?**
A: Yes! Use with Gunicorn and proper configuration

**Q: How does it handle errors?**
A: All errors return HTTP 200 with status in JSON

---

## 🎉 Summary

You now have a **professional-grade Chat API** that is:

✅ **Simple** - Single-purpose REST API  
✅ **Fast** - No heavy ML models  
✅ **Smart** - Crafted system prompt for health topics  
✅ **Reliable** - Comprehensive error handling  
✅ **Documented** - 9000+ words of documentation  
✅ **Tested** - Full test suite included  
✅ **Ready** - Can be deployed to production today  

**Start now:**
```bash
# Windows
start.bat

# Linux/macOS
bash start.sh
```

**Test it:**
```bash
python test_chat_api.py
```

**Use it:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever"}'
```

Happy coding! 🏥💬
