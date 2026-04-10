# AI Health Assistant Chat API - Setup & Usage Guide

## Overview

The Chat API provides a REST interface for health-related conversations powered by Ollama (Llama3 model). It's designed to be fast, reliable, and production-ready.

### Key Features
✅ **Smart Health Assistant** - Provides practical health advice  
✅ **Fast Responses** - Optimized timeouts and settings  
✅ **CORS Enabled** - Works with React frontend at localhost:5173  
✅ **Logging** - Detailed request/response logging  
✅ **Error Handling** - Graceful error handling with helpful messages  
✅ **Statistics** - Track API usage and performance  

---

## Prerequisites

### Required
- **Python 3.8+** - Python runtime
- **Ollama** - Local LLM service (https://ollama.ai)
- **Llama3 Model** - Download with `ollama pull llama3`
- **Flask** - Web framework (in requirements.txt)

### Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Ollama
# Download from https://ollama.ai
# Or on macOS: brew install ollama

# 3. Pull Llama3 model
ollama pull llama3

# 4. Verify installation
python -c "import requests; print(requests.get('http://localhost:11434/api/tags').status_code)"
```

---

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Flask settings
FLASK_PORT=5000
FLASK_DEBUG=False

# Ollama settings
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3
OLLAMA_TIMEOUT=30

# LLM parameters (tuned for health assistant)
OLLAMA_TEMPERATURE=0.9        # Higher = more creative responses
OLLAMA_TOP_P=0.9              # Nucleus sampling parameter
OLLAMA_REPEAT_PENALTY=1.2     # Penalize repetitive content
```

### Ollama Settings Explanation

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **stream** | false | Get complete response at once, not streamed |
| **temperature** | 0.9 | Balance between consistency (0.0) and creativity (1.0) |
| **top_p** | 0.9 | Only use top 90% probable tokens (nucleus sampling) |
| **repeat_penalty** | 1.2 | Discourage repeating the same words/phrases |

These settings ensure:
- ✅ Unique responses every time (no repetition)
- ✅ Natural, conversational language
- ✅ Fast response generation
- ✅ Practical health advice

---

## Running the API

### Start Ollama Service

```bash
# Terminal 1: Start Ollama (keeps running in background)
ollama serve

# You should see:
# > Ollama is running in http://0.0.0.0:11434
```

### Start Flask Backend

```bash
# Terminal 2: Navigate to backend directory
cd ai-health-assistant/backend

# Run the chat API
python chat_app.py

# You should see:
# > 🏥 AI Health Assistant Backend API
# > 🚀 Starting Flask server on port 5000
# > 💬 Chat endpoint: POST http://localhost:5000/api/chat
```

---

## API Endpoints

### 1. **POST /api/chat** - Main Chat Endpoint

Send a health question and get an AI response.

**Request:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever and sore throat"}'
```

**Request Body:**
```json
{
  "message": "What should I do about my fever?"
}
```

**Response (Success):**
```json
{
  "reply": "Here are some steps you can take:\n1. Rest and hydrate - drink plenty of water\n2. Take over-the-counter fever reducers if needed\n3. Monitor your temperature\n4. Seek medical attention if fever exceeds 103°F or lasts over 3 days",
  "status": "success",
  "response_time": 2.5
}
```

**Response (Error - Connection Issue):**
```json
{
  "reply": "I can't connect to the AI service right now. Please make sure Ollama is running: ollama serve",
  "status": "error",
  "error": "connection_failed"
}
```

**Response (Error - Empty Message):**
```json
{
  "reply": "Please ask me a health-related question.",
  "status": "error",
  "error": "empty_message"
}
```

---

### 2. **GET /api/health** - Health Check

Check if the API is running.

```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Health Assistant",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### 3. **GET /api/status** - Service Status

Check API and Ollama service status.

```bash
curl http://localhost:5000/api/status
```

**Response:**
```json
{
  "api": "online",
  "ollama": "online",
  "model": "llama3",
  "api_url": "http://localhost:11434",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### 4. **GET /api/stats** - Service Statistics

Get API usage statistics.

```bash
curl http://localhost:5000/api/stats
```

**Response:**
```json
{
  "service": "AI Health Assistant",
  "stats": {
    "total_requests": 42,
    "successful_requests": 40,
    "error_count": 2,
    "success_rate": "95.2%",
    "model": "llama3",
    "last_response": {
      "timestamp": "2024-01-15T10:30:45.123456",
      "user_message": "What about asthma?",
      "ai_reply": "Asthma...",
      "response_time": 2.1,
      "model": "llama3",
      "tokens_generated": 85
    }
  }
}
```

---

### 5. **GET /api/config** - Configuration (Debug)

View API configuration.

```bash
curl http://localhost:5000/api/config
```

**Response:**
```json
{
  "ollama": {
    "api_url": "http://localhost:11434",
    "model": "llama3",
    "timeout": 30,
    "temperature": 0.9,
    "top_p": 0.9,
    "repeat_penalty": 1.2,
    "endpoint": "http://localhost:11434/api/generate"
  },
  "cors_allowed_origins": [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173"
  ]
}
```

---

### 6. **POST /api/reset-stats** - Reset Statistics

Reset service statistics counter.

```bash
curl -X POST http://localhost:5000/api/reset-stats
```

**Response:**
```json
{
  "status": "success",
  "message": "Statistics reset"
}
```

---

## Error Handling

The API handles various error scenarios gracefully:

### Connection Error (Ollama not running)
```json
{
  "reply": "I can't connect to the AI service right now. Please make sure Ollama is running: ollama serve",
  "status": "error",
  "error": "connection_failed"
}
```

### Timeout Error (Response takes too long)
```json
{
  "reply": "The AI is taking too long to respond. Please try again.",
  "status": "error",
  "error": "timeout"
}
```

### Invalid Request
```json
{
  "reply": "Please send a valid JSON request with a \"message\" field.",
  "status": "error",
  "error": "invalid_request"
}
```

**Note:** Even when errors occur, the API returns HTTP 200 with error status in the JSON, ensuring the frontend always receives a proper response.

---

## Python Client Example

### Using requests library

```python
import requests
import json

def chat_with_health_assistant(message):
    """
    Send a health question to the AI assistant.
    
    Args:
        message (str): Health question
        
    Returns:
        dict: Response with "reply" key
    """
    url = "http://localhost:5000/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {"message": message}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=35)
        response.raise_for_status()
        
        data = response.json()
        return {
            "status": data.get("status"),
            "reply": data.get("reply"),
            "response_time": data.get("response_time")
        }
    except requests.exceptions.ConnectionError:
        return {"status": "error", "reply": "Cannot connect to AI service"}
    except requests.exceptions.Timeout:
        return {"status": "error", "reply": "Request timeout"}
    except Exception as e:
        return {"status": "error", "reply": str(e)}

# Usage
if __name__ == "__main__":
    questions = [
        "I have a fever and cough",
        "How long does the flu last?",
        "Should I see a doctor?",
        "What can I take for headache?"
    ]
    
    for question in questions:
        print(f"\n❓ Q: {question}")
        result = chat_with_health_assistant(question)
        print(f"✅ Status: {result['status']}")
        print(f"💬 A: {result['reply']}")
        if result.get('response_time'):
            print(f"⏱️  Response time: {result['response_time']:.2f}s")
```

---

## React Frontend Integration

### Example: React Component

```javascript
import { useState } from 'react';

function HealthChat() {
  const [message, setMessage] = useState('');
  const [reply, setReply] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      setReply(data.reply || 'No response');
    } catch (error) {
      setReply('Error: Could not reach AI service');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask a health question..."
      />
      <button onClick={sendMessage} disabled={loading}>
        {loading ? 'Thinking...' : 'Send'}
      </button>
      <div className="response">{reply}</div>
    </div>
  );
}

export default HealthChat;
```

---

## Performance Tips

### Response Time Optimization

| Setting | Recommendation | Impact |
|---------|----------------|--------|
| **Temperature** | 0.9 | Balanced creativity & speed |
| **Timeout** | 30s | Enough for quality 3-5 line response |
| **repeat_penalty** | 1.2 | Prevents long, repetitive answers |

### Expected Performance

```
Average response time: 2-5 seconds
- Model loading: included in first request
- Token generation: ~0.05s per 5 tokens
- Network latency: ~0.1s
```

### Batch Processing

For multiple requests, maintain connection pools:

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

# Now use session.post() for better connection reuse
```

---

## Troubleshooting

### Issue: "I can't connect to the AI service"

**Solution:**
```bash
# 1. Check if Ollama is running
curl http://localhost:11434/api/tags

# 2. Start Ollama if not running
ollama serve

# 3. Verify llama3 model is installed
ollama ls  # Should show llama3

# 4. If not, install it
ollama pull llama3
```

### Issue: Slow responses (>10s)

**Solution:**
```bash
# 1. Check Ollama memory usage
ollama list

# 2. Close other applications
# 3. Reduce timeout if acceptable
# 4. Check network connectivity
```

### Issue: Repetitive responses

**Solution:**
```bash
# Edit .env file:
OLLAMA_REPEAT_PENALTY=1.5  # Increase from 1.2
OLLAMA_TEMPERATURE=0.95    # Increase from 0.9
```

### Issue: Generic/robotic responses

**Solution:**
```bash
# Edit .env file:
OLLAMA_TEMPERATURE=1.0      # Increase for more creativity
OLLAMA_TOP_P=0.95           # Increase nucleus sampling
```

---

## Logging

### View Logs

The API logs to console. Look for:

```
✅ Ollama service is available
🔄 [Request #1] User: I have a fever...
📤 Sending request to http://localhost:11434/api/generate
✅ [Request #1] Response received in 2.45s (256 chars)
💬 AI Reply: Here are some steps...
```

### Log Levels

```
DEBUG  - Detailed information for debugging
INFO   - General information (requests, responses)
WARNING - Warning messages (Ollama unavailable)
ERROR  - Error messages (connection failed)
```

---

## Production Deployment

### Using Gunicorn

```bash
# Install gunicorn (if not already in requirements)
pip install gunicorn

# Run with multiple workers for concurrent requests
gunicorn --workers 4 --bind 0.0.0.0:5000 chat_app:app

# For better performance with async
gunicorn --workers 4 --worker-class gevent --bind 0.0.0.0:5000 chat_app:app
```

### Environment Variables for Production

```env
FLASK_DEBUG=False
OLLAMA_TIMEOUT=30
OLLAMA_TEMPERATURE=0.9
```

### CORS Configuration

Update for your production domain:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## Quick Test Script

Copy this to test the API:

```bash
#!/bin/bash

echo "🧪 Testing AI Health Assistant API..."
echo ""

# Test 1: Health Check
echo "1️⃣ Health Check..."
curl -s http://localhost:5000/api/health | jq .
echo ""

# Test 2: Status
echo "2️⃣ Service Status..."
curl -s http://localhost:5000/api/status | jq .
echo ""

# Test 3: Chat Request
echo "3️⃣ Chat Request..."
curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a sore throat"}' | jq .
echo ""

# Test 4: Stats
echo "4️⃣ Statistics..."
curl -s http://localhost:5000/api/stats | jq .
echo ""

echo "✅ All tests completed!"
```

---

## FAQ

**Q: Can I change the model from llama3?**
- A: Yes. Install another model with `ollama pull <model>` and update the env variable `OLLAMA_MODEL`.

**Q: How do I make responses longer/shorter?**
- A: The prompt is designed for 3-5 lines. Edit `_build_health_prompt()` in `ollama_chat.py` to change the system message.

**Q: Can I use this without Ollama?**
- A: You can modify the code to use OpenAI's API instead, but Ollama is free and runs locally.

**Q: What's the difference between chat_app.py and app.py?**
- A: `chat_app.py` is the focused chat API. `app.py` is the full application with symptom analysis and medicine verification.

---

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review logs with proper timestamps
3. Test with curl before trying from frontend
4. Verify Ollama is running: `ollama serve`

---

## Summary

You now have a production-ready Flask API with:

✅ **Smart prompting** for health assistant behavior  
✅ **Ollama integration** with llama3 model  
✅ **CORS support** for React frontend  
✅ **Error handling** for all failure scenarios  
✅ **Logging** for debugging and monitoring  
✅ **Statistics** for API usage tracking  
✅ **Documentation** for easy setup and usage  

**Start using it:**
```bash
# Terminal 1
ollama serve

# Terminal 2
cd ai-health-assistant/backend
python chat_app.py

# Terminal 3 (Test)
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I manage chest pain?"}'
```

Happy chatting! 💬🏥
