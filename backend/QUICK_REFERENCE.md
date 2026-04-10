# Quick Reference - AI Health Assistant Chat API

## 🚀 Start the API (Choose One)

### Windows (Command Prompt)
```cmd
cd backend
start.bat
```

### Windows (PowerShell)
```powershell
cd backend
.\start.ps1
```

### Linux/macOS
```bash
cd backend
bash start.sh
```

### Manual (Any OS)
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Flask API
cd backend
python chat_app.py
```

---

## 💬 Send a Chat Message

### Using curl
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever and sore throat"}'
```

### Using Python
```python
import requests

response = requests.post(
    'http://localhost:5000/api/chat',
    json={'message': 'I have a sore throat'},
    timeout=35
)
print(response.json()['reply'])
```

### Using JavaScript (React)
```javascript
const response = await fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'I have a fever' })
});
const data = await response.json();
console.log(data.reply);
```

---

## ✅ Check API Status

```bash
# Health check
curl http://localhost:5000/api/health

# Full status
curl http://localhost:5000/api/status

# View config
curl http://localhost:5000/api/config

# View stats
curl http://localhost:5000/api/stats
```

---

## 🧪 Test Everything

```bash
python test_chat_api.py
```

Runs 8 comprehensive tests:
1. Health check
2. Service status
3. Configuration
4. Chat with AI
5. Edge cases
6. Statistics
7. Error handling
8. CORS support

---

## ⚙️ Configuration (.env)

Most important settings:

```env
FLASK_PORT=5000              # Flask API port
OLLAMA_MODEL=llama3          # Which model to use
OLLAMA_TIMEOUT=30            # How long to wait for response
OLLAMA_TEMPERATURE=0.9       # Higher = more creative (0-1)
OLLAMA_TOP_P=0.9            # Diversity of responses
OLLAMA_REPEAT_PENALTY=1.2   # Prevent repetition
```

**Adjust for:**
- **Faster responses:** Lower TIMEOUT to 20s, TEMPERATURE to 0.7
- **More creative:** TEMPERATURE=1.0, TOP_P=0.95
- **Less repetition:** REPEAT_PENALTY=1.5

---

## 📊 API Response Examples

### Success Response
```json
{
  "reply": "Here are some steps you can take:\n1. Rest and hydrate\n2. Take pain relievers\n3. See a doctor if symptoms worsen",
  "status": "success",
  "response_time": 2.45
}
```

### Error Response
```json
{
  "reply": "I can't connect to the AI service right now. Please make sure Ollama is running: ollama serve",
  "status": "error",
  "error": "connection_failed"
}
```

---

## 🔗 All API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check if API is alive |
| `/api/status` | GET | Check Ollama & API status |
| `/api/chat` | POST | Chat with AI (main endpoint) |
| `/api/config` | GET | View configuration (debug) |
| `/api/stats` | GET | View usage statistics |
| `/api/reset-stats` | POST | Reset statistics counter |

---

## 🐛 Troubleshooting

### "Cannot connect to AI service"
```bash
# Make sure Ollama is running in another terminal
ollama serve

# Check Ollama is responding
curl http://localhost:11434/api/tags
```

### "Response takes too long" (>10s)
```bash
# Check if model is loaded
ollama ps

# Close other applications
# Try a smaller model if available
```

### "Ollama not installed"
```bash
# Download from https://ollama.ai
# Or (macOS): brew install ollama
# After install, restart your terminal
```

### "Python dependencies missing"
```bash
pip install -r requirements.txt
```

---

## 📚 Full Documentation

For detailed information, see:
- **CHAT_API_SETUP.md** - Complete 8000+ word setup guide
- **IMPLEMENTATION_SUMMARY.md** - Overview of what was created

---

## 🎯 Common Tasks

### Change the model
1. Install model: `ollama pull mistral`
2. Set in `.env`: `OLLAMA_MODEL=mistral`
3. Restart API

### Make responses longer
Edit prompt in `ollama_chat.py`:
```python
# Change from "3-5 lines" to "7-10 lines"
def _build_health_prompt(self, user_message: str) -> str:
    # ... modify system prompt ...
```

### Track API usage
```bash
curl http://localhost:5000/api/stats
```

### Reset usage stats
```bash
curl -X POST http://localhost:5000/api/reset-stats
```

### Integrate with React
```javascript
import { useState } from 'react';

function ChatWidget() {
  const [reply, setReply] = useState('');
  
  const handleChat = async (message) => {
    const res = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    setReply(data.reply);
  };
  
  return (
    <div>
      <button onClick={() => handleChat('I have a fever')}>
        Get Advice
      </button>
      <p>{reply}</p>
    </div>
  );
}
```

---

## 📈 Performance Tips

```
Response time breakdown:
- Model loading (first request): ~1-2s
- Standard request: ~2-4s
- Network latency: ~0.1s
- Token generation: ~0.05s per 5 tokens

Optimize by:
- Keeping Ollama running (model stays loaded)
- Using SSD for faster disk I/O
- Giving Ollama adequate RAM (8GB+ recommended)
- Choosing appropriate model size (llama3 is good middle ground)
```

---

## 🎓 Learning Resources

1. **Ollama Docs:** https://ollama.ai
2. **Flask Docs:** https://flask.palletsprojects.com
3. **LLM Prompt Engineering:** See `_build_health_prompt()` in `ollama_chat.py`
4. **API Testing:** Use `test_chat_api.py` as reference

---

## 💡 Tips & Tricks

1. **Keep Ollama running** - Use `nohup ollama serve &` on Linux/macOS
2. **Monitor performance** - Check `/api/stats` regularly
3. **Adjust parameters** - Try different temperature/top_p settings
4. **Use conversation context** - Pass context to API for better responses
5. **Cache responses** - Consider caching for performance
6. **Set up logging** - Enable logging for debugging

---

## ✨ What You Have

✅ Smart health assistant prompt  
✅ Ollama integration with llama3  
✅ Flask REST API with 6 endpoints  
✅ CORS support for React  
✅ Error handling for all cases  
✅ Comprehensive logging  
✅ Test suite with 8 tests  
✅ Configuration management  
✅ Performance monitoring  
✅ Production-ready code  

---

## 🔗 Quick Links

- **Chat:** `POST /api/chat` with `{"message": "your question"}`
- **Status:** `GET /api/status` to check if everything is working
- **Docs:** See `CHAT_API_SETUP.md` for full documentation
- **Tests:** Run `python test_chat_api.py` to verify setup
- **Config:** Edit `.env` file to adjust settings

---

## 🎯 Next Steps

1. Start the API: `start.bat` (Windows) or `bash start.sh` (Linux/macOS)
2. Test it: `python test_chat_api.py`
3. Check stats: `curl http://localhost:5000/api/stats`
4. Integrate with React frontend
5. Customize prompt for your needs
6. Deploy to production

---

**Everything is ready!** 🚀

Start with:
```bash
# Windows
start.bat

# Linux/macOS  
bash start.sh
```

Then test with:
```bash
python test_chat_api.py
```

That's it! 🎉
