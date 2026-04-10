# Anti-Repetition & Response Variation Implementation

## Overview

The AI Health Assistant now implements **strict anti-repetition rules** to ensure every response is unique, natural, and context-specific. No generic fallback patterns like "I understand you're asking about..." will ever appear.

## 🎯 Key Features Implemented

### 1. **Forbidden Patterns (NEVER Shown)**

The system explicitly forbids these patterns:
- ❌ "I understand you're asking about..."
- ❌ "Regarding your question..."
- ❌ "Your question..."
- ❌ "Please try again"
- ❌ "Service unavailable"
- ❌ "AI is not responding"

### 2. **Response Variation by Question Type**

The system now detects question type and generates **varied** context-aware responses:

#### Greeting (user says "Hi", "Hello", etc.)
```
"Hello! I'm here to help with health questions. What brings you in today?"
"Welcome! Feel free to ask me anything about your health concerns."
"Hi there! I'm ready to help. Tell me what's on your mind health-wise."
```
(Previous response is avoided)

#### Serious Symptoms (chest pain, breathing difficulty, etc.)
```
"This sounds urgent and requires immediate medical attention. Please seek emergency care or call your local emergency number."
"Based on what you've described, this needs urgent evaluation. Go to the nearest emergency room immediately."
"These symptoms warrant immediate professional evaluation. Please contact emergency services without delay."
```

#### Symptoms (fever, cough, etc. - non-serious)
```
"Your symptom(s) require monitoring and rest. Stay hydrated, get adequate sleep, and watch for worsening. How long have you had this?"
"For what you're experiencing, focus on rest, hydration, and monitoring symptom changes. Has this been going on long?"
"The best approach is rest, fluids, and tracking symptoms. When did this start?"
```

#### Medical/Diagnostic Questions
```
"That's an important health topic. Professional medical evaluation will give you specific guidance tailored to your situation."
"Your question is best answered by a healthcare provider who can assess your individual circumstances."
"For accurate medical information regarding your situation, consulting with a professional is the best approach."
```

### 3. **Response History Tracking**

- **Response History Dictionary**: Tracks the last 20 responses by normalized message
- **Normalized Messages**: Messages are normalized (lowercase, first 30 chars) to detect similar questions
- **Variation Logic**: When the same question is asked again, a different response is selected from the variation pool
- **No Repeats**: If multiple variations exist, the previously used one is avoided

### 4. **Enhanced System Prompt**

The LLM now receives explicit anti-repetition instructions:

```
ANTI-REPETITION (CRITICAL):
- NEVER start with "I understand you're asking about..."
- NEVER use the same opening twice - vary your approach
- Each response must have different wording and structure
- Be creative and natural - sound like a real health assistant
- If similar questions arise, give genuinely different perspectives
```

### 5. **Context-Aware Fallbacks**

When Ollama is unavailable, the system generates context-specific fallbacks instead of generic templates:

- **For symptoms**: Focuses on rest, hydration, and monitoring
- **For serious cases**: Emphasizes urgent medical attention
- **For greetings**: Warmly asks what assistance is needed
- **For medical terms**: Recommends professional evaluation
- **For general questions**: Offers natural conversational response

## 📁 Files Modified

### 1. **backend/ai_module/ollama_service.py**

#### New Methods Added:

**`_normalize_message(message: str) -> str`**
- Normalizes messages for tracking (lowercase, first 30 chars)
- Used to detect similar questions

**`_track_response(message: str, response: str)`**
- Records response in history
- Maintains sliding window of 20 recent responses
- Prevents tracking unlimited responses

**`_generate_context_aware_fallback(message: str) -> str`**
- REPLACES the generic "I understand you're asking..." fallback
- Detects question type (greeting, symptom, serious, medical, generic)
- Selects appropriate conversation pattern
- Ensures disclaimer is included

**`_pick_varied_response(message: str, responses: list) -> str`**
- Selects from a list of response variations
- Avoids responses used in previous similar questions
- Falls back to rotation if no varied option available
- Ensures all responses include required disclaimer

#### Enhanced Methods:

**`chat_answer()` method**
- Now calls `_track_response()` after every response
- Uses `_generate_context_aware_fallback()` instead of template
- Passes response history context to LLM
- Forbidden patterns explicitly listed in system prompt

**`__init__()` constructor**
- Added `self.response_history = {}` for tracking
- Updated timeouts to 60s for better response quality
- Increased max_tokens to 150 for more detailed answers

### 2. **backend/app.py**

#### `/api/chat` endpoint changes:

- Replaced generic fallback messages with varied alternatives
- Added hash-based selection for variation in error cases
- All responses include context-specific guidance

## 🔄 How It Works

### Scenario 1: First Question About Fever
```
User: "I have a fever"
→ System detects: is_symptom = True
→ LLM generates response with full rules + anti-repetition emphasis
→ Response tracked in history
→ Example output: "A fever indicates your body is fighting an infection. 
   Get rest, drink fluids, and monitor your temperature. How long have you had it?
   Consult a healthcare professional for personalized advice."
```

### Scenario 2: Similar Follow-up Question
```
User: "What about my fever?"
→ System detects: is_symptom = True (similar to first)
→ Response history shows a fever response was recently given
→ Different variation is selected or LLM generates new perspective
→ Example output: "Fevers are your immune system's response to infection.
   Focus on rest and hydration while monitoring how you feel. Has it gotten worse?
   Consult a healthcare professional for personalized advice."
```

### Scenario 3: Ollama Fails
```
User: "I have chest pain"
→ LLM fails/unavailable
→ System detects: is_serious = True
→ Context-aware fallback selected:
   "This sounds urgent and requires immediate medical attention. 
    Please seek emergency care right away. 
    Consult a healthcare professional for personalized advice."
```

## ✅ Verification Checklist

Run the test to verify anti-repetition:

```bash
cd backend
python test_rules_simple.py
```

Look for:
- ✅ No "I understand you're asking about..." patterns
- ✅ Different responses for similar symptom questions
- ✅ Context-specific fallbacks (not generic)
- ✅ All responses end with disclaimer
- ✅ 2-3 sentence responses (no long paragraphs)
- ✅ Each answer is tailored to the specific question

## 🎨 Response Variation Examples

### Cold Question
**First ask**: "A common cold typically improves within 7-10 days. Rest, hydrate, and monitor symptoms. If it worsens, see a doctor."

**Second ask (variation)**: "Colds are self-limiting viral infections. Your main focus should be rest and staying hydrated while symptoms resolve naturally. Are you experiencing any concerning symptoms?"

### Fever Question
**First ask**: "Fevers indicate your body is fighting infection. Rest, drink lots of fluids, and track your temperature. How high has it been?"

**Second ask (variation)**: "A fever is your immune system's response. The best treatment is rest, hydration, and monitoring. Have you been taking your temperature?"

## 🚀 Benefits

1. **No Repetition**: Each response uses different wording and structure
2. **Natural Conversation**: Feels like talking to a real health assistant
3. **Context-Aware**: Responses tailored to specific question types
4. **Graceful Degradation**: Falls back gracefully when Ollama unavailable
5. **No Generic Messages**: Every response is specific and helpful
6. **Better UX**: Users never see "Please try again" or "Service unavailable"

## 📊 Response History Storage

Maximum 20 responses stored with keys like:
```python
{
    "i have a fever": "A fever indicates...",
    "what about my cough": "Coughs can be caused by...",
    "hi": "Hello! I'm here to help...",
    "chest pain": "This sounds urgent..."
}
```

Old responses are removed automatically when limit exceeded.

## 🔧 Configuration

Update `.env` to control response behavior:

```env
# Timeouts for better quality
OLLAMA_TIMEOUT=60
LLM_RESPONSE_TIMEOUT=60
LLM_MAX_TOKENS=150
LLM_NUM_PREDICT=120
```

---

**Status**: ✅ Fully Implemented  
**Last Updated**: April 9, 2026  
**Features**: Anti-repetition, Context-aware responses, Varied fallbacks, Response history tracking
