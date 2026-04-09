# AI Health Assistant - Advanced API Documentation

## Overview
This document describes the new LLM-powered endpoints added to the AI Health Assistant backend. These endpoints integrate OpenAI's GPT-3.5-turbo model with the existing ML and NLP layers to provide conversational AI, dynamic explanations, and advanced health analysis.

## Configuration

### Environment Variables
```bash
# .env file
OPENAI_API_KEY=sk-your-api-key-here
```

### Dependencies
- `openai>=0.27.0` - OpenAI Python client
- `flask` - Web framework
- `sentence-transformers` - NLP embeddings

## New Endpoints

### 1. `/api/ai/status` (GET)
**Check if AI service is available and properly configured**

**Response:**
```json
{
  "status": "operational",
  "api_key_configured": true,
  "model": "gpt-3.5-turbo",
  "message": "AI service is operational"
}
```

**Status Codes:**
- `200` - Service operational
- `503` - Service unavailable (missing API key)

**Example Usage:**
```bash
curl http://localhost:5000/api/ai/status
```

---

### 2. `/api/ai/explain` (POST)
**Generate AI-powered explanation for disease predictions**

**Request Body:**
```json
{
  "disease": "Flu",
  "symptoms": ["fever", "cough", "fatigue"],
  "confidence": 72
}
```

**Response:**
```json
{
  "status": "success",
  "disease": "Flu",
  "confidence": 72,
  "ai_explanation": {
    "explanation": "Based on your symptoms of fever, cough, and fatigue (72% confidence), you likely have the flu (influenza). The flu is caused by the influenza virus and typically presents with these exact symptoms...",
    "disclaimer": "⚠️ Medical Disclaimer: This AI is provided for informational purposes only and should not be used for self-diagnosis or self-treatment. Please consult with a qualified healthcare professional for accurate diagnosis and treatment recommendations."
  }
}
```

**Example Usage:**
```bash
curl -X POST http://localhost:5000/api/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "Flu",
    "symptoms": ["fever", "cough"],
    "confidence": 72
  }'
```

---

### 3. `/api/ai/extract-symptoms` (POST)
**Extract symptoms from natural language text using LLM-powered NLP**

**Request Body:**
```json
{
  "text": "I have been experiencing hair fall and feeling very tired lately. Also my head hurts."
}
```

**Response:**
```json
{
  "status": "success",
  "user_input": "I have been experiencing hair fall and feeling very tired lately. Also my head hurts.",
  "extracted_data": {
    "extracted_symptoms": ["hair loss", "fatigue", "headache"],
    "confidence": 0.94,
    "explanation": "The system identified hair loss (alopecia), general fatigue, and headache from your description. These are recognized medical symptoms."
  }
}
```

**Features:**
- Handles various symptom descriptions (medical terms, laymen terms, typos)
- Returns confidence score for extraction accuracy
- Provides validation against known symptom database

**Example Usage:**
```bash
curl -X POST http://localhost:5000/api/ai/extract-symptoms \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I have a runny nose and sore throat"
  }'
```

---

### 4. `/api/chat` (POST)
**Chat interface for health-related questions with conversational AI**

**Request Body:**
```json
{
  "message": "Is this serious? Should I go to the hospital?",
  "context": {
    "disease": "Influenza",
    "symptoms": ["fever", "cough"],
    "confidence": 72,
    "risk_level": "Medium"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "user_message": "Is this serious? Should I go to the hospital?",
  "ai_response": {
    "answer": "The flu (influenza) is typically considered a moderate-risk illness. Most cases of flu resolve within 1-2 weeks at home...",
    "follow_up_suggestions": [
      "What are common treatment options for the flu?",
      "How can I prevent spreading the flu to others?",
      "When should I seek emergency medical care?"
    ],
    "disclaimer": "⚠️ Medical Disclaimer: This AI is provided for informational purposes only..."
  }
}
```

**Features:**
- Context-aware responses (considers previous diagnosis)
- Suggests follow-up questions
- 24/7 availability
- Temperature set to 0.7 for balanced responses

**Example Usage:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I do if symptoms get worse?",
    "context": {
      "disease": "Flu",
      "symptoms": ["fever"],
      "confidence": 70
    }
  }'
```

---

### 5. `/api/ai/advice` (POST)
**Generate personalized health advice based on diagnosis**

**Request Body:**
```json
{
  "disease": "Type 2 Diabetes",
  "symptoms": ["excessive thirst", "fatigue"],
  "risk_level": "High"
}
```

**Response:**
```json
{
  "status": "success",
  "disease": "Type 2 Diabetes",
  "ai_advice": {
    "advice": "For Type 2 Diabetes management: 1) Monitor blood sugar regularly, 2) Follow a balanced diet low in sugar and refined carbs, 3) Exercise 30 minutes daily, 4) Maintain healthy weight, 5) Take prescribed medications as directed...",
    "disclaimer": "⚠️ Medical Disclaimer: This AI..."
  }
}
```

**Example Usage:**
```bash
curl -X POST http://localhost:5000/api/ai/advice \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "Hypertension",
    "symptoms": ["high blood pressure"],
    "risk_level": "High"
  }'
```

---

### 6. `/api/ai/medicine-explanation` (POST)
**Generate explanation for medicine detection results**

**Request Body:**
```json
{
  "medicine_name": "Aspirin",
  "detection_result": {
    "confidence": 0.92,
    "packaging_quality": "high",
    "is_recognized": true
  }
}
```

**Response:**
```json
{
  "status": "success",
  "medicine_explanation": {
    "explanation": "Aspirin (acetylsalicylic acid) is a widely used over-the-counter medication. The system detected this medicine with 92% confidence and confirmed high packaging quality, indicating this is a genuine product...",
    "confidence": 0.92,
    "disclaimer": "⚠️ Medical Disclaimer: This AI is provided for informational purposes only..."
  }
}
```

---

### 7. `/api/advanced/symptom-analysis` (POST)
**Complete end-to-end analysis combining NLP, ML, and LLM**

**Request Body:**
```json
{
  "symptoms": "I have been having severe headaches for three days along with a fever and cough"
}
```

**Response:**
```json
{
  "status": "success",
  "user_input": "I have been having severe headaches for three days along with a fever and cough",
  "analysis": {
    "nlp_extraction": {
      "extracted_symptoms": ["headache", "fever", "cough"],
      "confidence": 0.96,
      "method": "LLM-based extraction"
    },
    "ml_prediction": {
      "primary_disease": {
        "disease": "Influenza",
        "confidence": 78
      },
      "alternatives": [
        {
          "disease": "Common Cold",
          "confidence": 65
        }
      ],
      "risk_level": "Medium",
      "emergency_alert": null
    },
    "ai_explanation": {
      "explanation": "Based on your symptoms of headache, fever, and cough...",
      "disclaimer": "⚠️ Medical Disclaimer..."
    },
    "health_advice": {
      "advice": "For flu management: rest, stay hydrated, take over-the-counter medications for fever relief...",
      "disclaimer": "⚠️ Medical Disclaimer..."
    }
  }
}
```

**Pipeline:**
1. **NLP Extraction** - Extract symptoms from natural language (using LLM)
2. **ML Prediction** - Predict disease using Random Forest model
3. **LLM Explanation** - Generate dynamic explanation
4. **Health Advice** - Provide personalized recommendations

---

## Error Handling

### Error Response Format
```json
{
  "status": "error",
  "error": "OpenAI API error: Authorization error - Invalid API key"
}
```

### Common Errors

| Error | Status Code | Cause |
|-------|------------|-------|
| `OpenAI API error: Authorization error` | 500 | Missing or invalid API key |
| `OpenAI API error: Rate limit exceeded` | 500 | Too many requests to OpenAI API |
| `OpenAI API error: Request timeout` | 500 | API call took too long (>10 seconds) |
| `No text provided` | 400 | Empty input text |
| `No message provided` | 400 | Empty chat message |

### Fallback Behavior
When API is unavailable, the system returns graceful fallback messages instead of crashing:
```json
{
  "status": "error",
  "error": "OpenAI API error: Authorization error",
  "Note": "AI explanation temporarily unavailable"
}
```

---

## Performance Characteristics

### Response Times
- Status check: <100ms
- Explanation generation: 1-3 seconds
- Symptom extraction: 2-4 seconds
- Chat response: 1-5 seconds
- Health advice: 2-4 seconds
- Advanced analysis: 5-10 seconds (includes ML prediction)

### Optimization Settings
- Model: GPT-3.5-turbo (cost-effective, fast)
- Temperature: 0.7 (balance between creativity and consistency)
- Max tokens: 300 per response (limits response length and cost)
- Timeout: 10 seconds per API call

---

## Integration Examples

### Frontend React Integration
```javascript
// Send chat message
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Is this serious?",
    context: {
      disease: "Flu",
      symptoms: ["fever", "cough"],
      confidence: 72
    }
  })
});

const data = await response.json();
console.log(data.ai_response.answer);
```

### Python Backend Integration
```python
from ai_module.llm_service import get_ai_service

ai_service = get_ai_service()

# Generate explanation
explanation = ai_service.generate_explanation(
    disease="Flu",
    symptoms=["fever", "cough"],
    confidence=72
)

# Chat answer
response = ai_service.chat_answer(
    user_question="Is this serious?",
    context={"disease": "Flu", "risk_level": "Medium"}
)
```

---

## Security Considerations

1. **API Key Management**: Store OpenAI API key in environment variables, never commit to version control
2. **Rate Limiting**: Implement rate limiting to prevent API abuse
3. **Input Validation**: All user inputs are validated before sending to OpenAI
4. **Medical Disclaimer**: All responses include medical disclaimer
5. **Data Privacy**: No user data is stored in OpenAI after response generation

---

## Testing

### Manual Testing with cURL
```bash
# Check API status
curl http://localhost:5000/api/ai/status

# Test explanation generation
curl -X POST http://localhost:5000/api/ai/explain \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "Flu",
    "symptoms": ["fever", "cough"],
    "confidence": 72
  }'

# Test chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I take?",
    "context": {"disease": "Flu", "symptoms": ["fever"]}
  }'
```

---

## Deployment Checklist

- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Test all endpoints locally
- [ ] Run symptom analysis pipeline end-to-end
- [ ] Test error handling (disconnect API, invalid key)
- [ ] Verify response times meet <2 second target
- [ ] Test with various symptom combinations
- [ ] Verify medical disclaimers appear in all responses
- [ ] Load test with concurrent requests
- [ ] Monitor OpenAI API usage and costs

---

## Support

For issues or questions:
- Check API status endpoint: `/api/ai/status`
- Review error messages returned by endpoints
- Verify OpenAI API key is correct
- Check rate limiting isn't exceeded
- Contact the development team for support
