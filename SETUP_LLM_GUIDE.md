# AI Health Assistant - LLM Integration Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 14+ with npm
- OpenAI API account with API key
- Flask backend running
- Modern web browser

## Quick Start (5 minutes)

### 1. Set OpenAI API Key
```bash
# On Windows PowerShell
$env:OPENAI_API_KEY = "sk-your-api-key-here"

# On Windows Command Prompt
set OPENAI_API_KEY=sk-your-api-key-here

# On Linux/Mac
export OPENAI_API_KEY="sk-your-api-key-here"
```

### 2. Start Backend
```bash
cd backend
python app.py
```

Backend will start at `http://localhost:5000`

### 3. Check AI Service Status
```bash
curl http://localhost:5000/api/ai/status
```

Should return:
```json
{
  "status": "operational",
  "api_key_configured": true,
  "model": "gpt-3.5-turbo",
  "message": "AI service is operational"
}
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend will start at `http://localhost:5173`

## Detailed Integration Guide

### Backend Setup

#### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Required packages already in requirements.txt:**
- `openai>=0.27.0`
- `flask`
- `sentence-transformers`
- `scikit-learn`
- `opencv-python`
- `pytesseract`

#### Step 2: Configure OpenAI API Key

**Option 1: Environment Variable (Recommended)**
```bash
# Create or edit .env file in backend directory
OPENAI_API_KEY=sk-your-api-key-here
```

**Option 2: System Environment Variable**
```bash
# Permanent setup (Windows)
setx OPENAI_API_KEY "sk-your-api-key-here"

# Permanent setup (Mac/Linux)
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Step 3: Verify Backend LLM Module
```bash
# In backend directory
python -c "from ai_module.llm_service import get_ai_service; print('✓ LLM Service loaded successfully')"
```

#### Step 4: Test Backend Endpoints
```bash
# Test 1: Check AI status
curl -X GET http://localhost:5000/api/ai/status

# Test 2: Generate explanation
curl -X POST http://localhost:5000/api/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "Flu",
    "symptoms": ["fever", "cough"],
    "confidence": 72
  }'

# Test 3: Chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Should I see a doctor?",
    "context": {"disease": "Flu", "symptoms": ["fever"]}
  }'
```

### Frontend Setup

#### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

#### Step 2: Build System
```bash
# Development mode with hot reload
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

#### Step 3: Verify Frontend Components
Ensure these components exist:
- `src/components/ChatWidget.jsx` - New chat component
- `src/components/AnimatedGradientBackground.jsx` - Animated background
- `src/App.jsx` - Main application (updated with ChatPage)

#### Step 4: Test Frontend Chat Page
1. Navigate to `http://localhost:5173`
2. Go to "Chat" tab in navigation
3. Verify ChatWidget appears
4. Try sending a message

## Architecture Overview

```
User Input (Frontend)
        ↓
    Chat Page (React)
        ↓
    ChatWidget Component
        ↓
/api/chat Endpoint (Flask)
        ↓
AIExplanationService.chat_answer()
        ↓
OpenAI GPT-3.5-turbo
        ↓
Response (with medical disclaimer)
        ↓
Display in Chat UI
```

## Key Components

### Backend: `ai_module/llm_service.py`
- **AIExplanationService class**: Main interface for all LLM operations
- **Methods**:
  - `generate_explanation()` - Explain disease predictions
  - `extract_symptoms_from_text()` - Extract symptoms from natural language
  - `generate_health_advice()` - Generate personalized health advice
  - `chat_answer()` - Conversational responses
  - `explain_medicine_detection()` - Explain medicine verification results
  - `get_system_status()` - Check service availability

### Frontend: `components/ChatWidget.jsx`
- **Features**:
  - Real-time messaging
  - Typing indicator
  - Follow-up suggestions
  - Responsive design
  - Error handling

### Flask Endpoints
All endpoints documented in [API_LLM_DOCUMENTATION.md](../backend/API_LLM_DOCUMENTATION.md)

## Performance Optimization

### Current Settings
```python
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 300
TIMEOUT_SECONDS = 10
```

### Optimization Tips
1. **Cache Responses**: Store similar responses to reduce API calls
2. **Batch Requests**: Group multiple queries when possible
3. **Monitor Usage**: Track OpenAI API consumption and costs
4. **Rate Limiting**: Implement rate limiting on Flask backend
5. **Response Compression**: Enable gzip compression for API responses

## Monitoring and Debugging

### Check AI Service Status
```bash
curl http://localhost:5000/api/ai/status
```

### Enable Debug Logging
```python
# In backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Test LLM Service Directly
```python
from ai_module.llm_service import get_ai_service

ai_service = get_ai_service()

# Test explanation
result = ai_service.generate_explanation("Flu", ["fever", "cough"], 72)
print(result)

# Test chat
response = ai_service.chat_answer("Is this serious?", {"disease": "Flu"})
print(response)
```

### Check Logs
```bash
# Python backend shows logs in console
# Browser DevTools → Console tab shows frontend errors
```

## Troubleshooting

### Issue: "Authorization error - Invalid API key"
**Solution**:
1. Verify API key is correct: https://platform.openai.com/account/api-keys
2. Check environment variable is set: `echo $OPENAI_API_KEY`
3. Restart Flask backend after setting API key

### Issue: "Rate limit exceeded"
**Solution**:
1. Wait a few seconds before retrying
2. Implement exponential backoff in client
3. Consider upgrading OpenAI API plan

### Issue: Chat widget not appearing
**Solution**:
1. Check browser console for errors
2. Verify `ChatWidget.jsx` exists in `src/components/`
3. Check imports in `App.jsx`
4. Clear browser cache: Ctrl+Shift+Del

### Issue: "Request timeout"
**Solution**:
1. Check OpenAI API status: https://status.openai.com/
2. Increase timeout in `llm_service.py`: `TIMEOUT_SECONDS = 15`
3. Check network connection

### Issue: Backend not responding
**Solution**:
1. Verify Flask is running: `http://localhost:5000/api/ai/status`
2. Check backend logs for errors
3. Ensure port 5000 is available
4. Restart backend: `python app.py`

## Cost Estimation

### GPT-3.5-turbo Pricing (as of 2024)
- Input: $0.0005 per 1K tokens
- Output: $0.0015 per 1K tokens

### Typical Usage
- Short explanation: ~100 tokens = ~$0.0002-0.0004
- Chat response: ~150 tokens = ~$0.0003-0.0006
- Health advice: ~200 tokens = ~$0.0004-0.0008

### Monthly Estimates (100 users, 5 queries/day)
- 100 users × 5 queries × 30 days = 15,000 queries
- Average tokens per query: 150 (in + out)
- Estimated cost: ~$15-25/month

## Production Deployment Checklist

- [ ] API key stored in secure environment variables
- [ ] CORS properly configured for production domain
- [ ] Rate limiting enabled
- [ ] Error logging configured
- [ ] Response caching implemented
- [ ] Monitoring and alerts set up
- [ ] OpenAI API usage tracking
- [ ] Database backups configured (if using)
- [ ] HTTPS enabled
- [ ] Medical disclaimers reviewed by legal
- [ ] User data privacy compliance verified
- [ ] Load testing completed
- [ ] Backup AI provider considered (fallback)

## Advanced Configuration

### Custom OpenAI Parameters
Edit `backend/ai_module/llm_service.py`:
```python
# Adjust these constants for your needs
TEMPERATURE = 0.7  # Lower = more deterministic, Higher = more creative
MAX_TOKENS = 300   # Reduce to cut costs, increase for longer responses
REQUEST_TIMEOUT = 10  # Timeout in seconds
```

### Response Caching
Add caching layer to reduce API calls:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_explanation(disease, symptoms_tuple):
    symptoms = list(symptoms_tuple)
    return generate_explanation(disease, symptoms, 75)
```

### Custom Prompt Engineering
Modify prompts in `llm_service.py` to suit your needs:
```python
def generate_explanation(self, disease: str, symptoms: List[str], confidence: int):
    # Customize this prompt for your use case
    prompt = f"""
    Medical Context: {disease}
    Patient Symptoms: {', '.join(symptoms)}
    Confidence: {confidence}%
    
    Provide a brief, clear explanation suitable for a patient...
    """
```

## Support and Resources

- OpenAI Documentation: https://platform.openai.com/docs
- OpenAI API Status: https://status.openai.com/
- Flask Documentation: https://flask.palletsprojects.com/
- React Documentation: https://react.dev/
- Project GitHub: [Your repo URL]

## Next Steps

1. **Monitor Performance**: Track API response times and costs
2. **Gather User Feedback**: Improve prompts based on user feedback
3. **Scale Up**: Implement caching and optimization as usage grows
4. **Add Features**: Consider adding image analysis, voice input, etc.
5. **Integrate Analytics**: Track which topics are most frequently asked

## Support Contact

For issues or questions:
- Email: support@aihealthassistant.com
- Issues: GitHub Issues on project repository
- Documentation: See [API_LLM_DOCUMENTATION.md](../backend/API_LLM_DOCUMENTATION.md)
