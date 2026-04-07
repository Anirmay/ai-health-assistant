# API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Currently no authentication required (add JWT in production)

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check if the API is running

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Health Assistant"
}
```

---

### 2. Symptom Analysis

**Endpoint:** `POST /api/symptoms`

**Description:** Analyze symptoms and predict possible diseases

**Request Body:**
```json
{
  "symptoms": "fever, cough, difficulty breathing"
}
```

**Response:**
```json
{
  "disease": "Respiratory Infection",
  "confidence": 0.92,
  "risk_level": "Medium",
  "recommendations": [
    "See a doctor",
    "Take antibiotics if prescribed",
    "Rest",
    "Drink fluids"
  ]
}
```

**Status Codes:**
- `200`: Success
- `400`: No symptoms provided
- `500`: Server error

---

### 3. Medicine Verification

**Endpoint:** `POST /api/verify-medicine`

**Description:** Verify if a medicine is authentic using image analysis

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `image` (image file)

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/verify-medicine \
  -F "image=@medicine.jpg"
```

**Response:**
```json
{
  "is_authentic": true,
  "confidence": 0.87,
  "details": {
    "hologram_detected": true,
    "barcode_valid": true,
    "color_consistency": true,
    "text_clarity": true
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: No image provided
- `500`: Server error

---

### 4. AI Chat

**Endpoint:** `POST /api/chat`

**Description:** Ask health-related questions to AI assistant

**Request Body:**
```json
{
  "message": "What should I do for a high fever?"
}
```

**Response:**
```json
{
  "response": "Fever is a sign your body is fighting an infection...",
  "success": true
}
```

**Status Codes:**
- `200`: Success
- `400`: No message provided
- `500`: Server error

---

### 5. User History

**Endpoint:** `GET /api/history`

**Description:** Get user's past health consultations

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "date": "2024-04-07",
      "type": "symptom_check",
      "result": "Respiratory Infection",
      "confidence": 0.92
    },
    {
      "id": 2,
      "date": "2024-04-06",
      "type": "medicine_check",
      "result": "Authentic",
      "confidence": 0.87
    }
  ]
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Errors

| Code | Message | Solution |
|------|---------|----------|
| 400 | No symptoms provided | Include symptoms in request body |
| 400 | No image provided | Upload an image file |
| 500 | Error in symptom analysis | Check input and try again |
| 500 | Error in medicine verification | Ensure image is clear and valid |

---

## Rate Limiting
Currently no rate limiting. Add for production deployment.

---

## Best Practices

1. **Symptom Analysis**
   - Provide detailed symptom descriptions
   - Results are for reference only, not medical diagnosis

2. **Medicine Verification**
   - Use clear, well-lit images
   - Include medicine label and barcode
   - Multiple angles improve accuracy

3. **AI Chat**
   - Ask specific health questions
   - For emergencies, always seek professional help
   - Responses are general guidance only

---

## Example Requests

### JavaScript/Fetch
```javascript
// Symptom Analysis
const response = await fetch('/api/symptoms', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ symptoms: 'fever and cough' })
});
const data = await response.json();

// AI Chat
const chatResponse = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'What should I do?' })
});
```

---

## Notes
- All timestamps are in UTC
- Confidence scores range from 0 to 1
- Medical advice is for informational purposes only
