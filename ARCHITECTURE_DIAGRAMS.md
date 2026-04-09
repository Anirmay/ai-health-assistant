# System Architecture: Unsupported Symptom Handling

## Complete Request/Response Flow

```
┌──────────────────────── FRONTEND ─────────────────────┐
│                                                        │
│  User Input: "hair loss"                              │
│  textarea ──┬─────────────────────────────┐           │
│             ↓                             │           │
│       [Analyze] button                    │           │
│             │                             │           │
│             ├────────────────────────────►│           │
│             │  POST /api/symptoms         │           │
│             │  {"symptoms": "hair loss"}  │           │
│             │                             │           │
└─────────────┼─────────────────────────────┼───────────┘
              │                             │
              │          HTTP POST          │
              ↓                             ↓
┌──────────────────────── BACKEND ─────────────────────┐
│                                                       │
│  app.py: analyze_symptoms()                          │
│  │                                                   │
│  ├─► STEP 1: NLP SYMPTOM MAPPING                     │
│  │   └─ map_user_symptoms("hair loss")               │
│  │      └─ from symptom_mapper.py                    │
│  │         ├─ Exact Match? NO                        │
│  │         ├─ NLP Similarity? YES (92%)              │
│  │         └─ Result: "hair loss" mapped             │
│  │                                                   │
│  ├─► STEP 1.5: VALIDATE SYMPTOM SUPPORT (NEW!)       │
│  │   └─ validate_symptoms_support(["hair loss"])     │
│  │      └─ from symptom_disease_model.py             │
│  │         ├─ is_symptom_supported("hair loss")?     │
│  │         ├─ Check: "hair_loss" in DB? NO!          │
│  │         ├─ Result: unsupported!                   │
│  │         └─ Get suggestions: ["fever", ...]        │
│  │                                                   │
│  ├─► VALIDATION CHECK                                │
│  │   if not all_supported:                           │
│  │      return {                                     │
│  │        status: "unsupported_symptom",            │
│  │        message: "We understood...",              │
│  │        unsupported: ["hair loss"],               │
│  │        suggestions: ["fever", ...],              │
│  │      }                                            │
│  │   ELSE continue...                                │
│  │                                                   │
│  ├─► STEP 2: DISEASE PREDICTION (skipped for this case)
│  │   └─ [Not reached due to validation failure]      │
│  │                                                   │
│  └─► RETURN RESPONSE                                 │
│      {                                               │
│        "status": "unsupported_symptom",             │
│        "user_input": "hair loss",                    │
│        "symptom_mappings": [                         │
│          {                                           │
│            "user_input": "hair loss",                │
│            "mapped_symptom": "hair loss",            │
│            "confidence": 0.92,                       │
│            "method": "nlp"                           │
│          }                                           │
│        ],                                            │
│        "mapping_confidence": 0.92,                   │
│        "mapped_symptoms": ["hair loss"],             │
│        "supported_symptoms": [],                     │
│        "unsupported_symptoms": ["hair loss"],        │
│        "message": "✓ We understood your symptom..." │
│        "suggestion": "💡 Try adding more common...", │
│        "common_suggestions": [                       │
│          "fever",                                    │
│          "cough",                                    │
│          "headache",                                 │
│          "fatigue",                                  │
│          "shortness_of_breath"                       │
│        ]                                             │
│      }                                               │
│                                                       │
└───────────────────────────────────────────────────────┘
              │          HTTP 200 + JSON         │
              ↓                                  ↓
┌──────────────────────── FRONTEND ─────────────────────┐
│                                                        │
│  response.json()                                      │
│  │                                                    │
│  ├─► Check result.status                             │
│  │   └─ Is "unsupported_symptom"? YES               │
│  │                                                   │
│  ├─► RENDER: Unsupported Component                   │
│  │   ├─ ⚠️ Orange Alert Card                         │
│  │   ├─ Show unsupported: "hair loss"                │
│  │   ├─ Show suggestion buttons:                     │
│  │   │  [+ fever] [+ cough] [+ headache] ...         │
│  │   ├─ Show "What You Can Do" guidance              │
│  │   └─ Show action buttons:                         │
│  │      [🔄 Try Different] [Clear All]               │
│  │                                                   │
│  └─► User sees beautiful fallback message             │
│      (not a confusing error)                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## Comparison: Before vs After

### BEFORE (Broken Experience)
```
User: "I have hair loss"
  ↓
NLP: "OK, mapped to 'hair loss'" ✓
  ↓
ML Model: "I don't know what to do with this"
  ↓
API Response: "{error: No matching diseases found}"
  ↓
User sees: "No diseases match the provided symptoms"
  ↓
User thinks: "The system is broken!" or "Hair loss isn't medical?"
  ↓
🤯 Confused/Frustrated
```

### AFTER (Great Experience)
```
User: "I have hair loss"
  ↓
NLP: "OK, mapped to 'hair loss'" ✓
  ↓
Validation: "This symptom isn't in our trained model" ⚠️
  ↓
API Response: {
  status: "unsupported_symptom",
  message: "We understood you, just can't predict yet",
  suggestions: ["fever", "cough", ...]
}
  ↓
User sees: 
  ⚠️ "Limitations Detected"
  ✓ "We understood: hair loss"
  ⚠️ "Not supported in our model"
  💡 "Try: fever, cough, headache, fatigue..."
  [+ fever] [+ cough] [+ headache] [+ fatigue]
  ↓
😊 User clicks [+ fever] or tries other symptoms
```

---

## Deep Dive: Validation Logic

```python
# Backend Validation Process

def validate_symptoms(symptoms_list):
    """Validates symptoms against trained database"""
    
    # Step 1: Normalize
    symptoms = [s.strip().lower().replace(' ', '_') for s in symptoms_list]
    
    # Step 2: Separate supported/unsupported
    supported = []
    unsupported = []
    for symptom in symptoms:
        if symptom in self.symptom_disease_db:
            supported.append(symptom)      # ✓ Found in database
        else:
            unsupported.append(symptom)    # ❌ Not found
    
    # Step 3: Get suggestions
    common_suggestions = sorted(
        self.symptom_disease_db.keys(),
        key=lambda s: len(self.symptom_disease_db.get(s, [])),
        reverse=True
    )[:5]  # Top 5 most common
    
    # Step 4: Return results
    return {
        'supported': supported,              # [] for "hair loss"
        'unsupported': unsupported,          # ['hair_loss'] ← normalized
        'all_supported': len(unsupported)==0,# False
        'common_suggestions': suggestions    # ['fever', 'cough', ...]
    }
```

---

## Frontend Conditional Logic

```jsx
// Simplified decision tree

if (result === null) {
  // Show initial form
  return <InputForm />
}

if (result.status === "unsupported_symptom") {
  // 🎨 Show fallback UI
  return <UnsupportedSymptomCard 
    message={result.message}
    unsupported={result.unsupported_symptoms}
    suggestions={result.common_suggestions}
  />
}

if (result.status === "success" || !result.status) {
  // 📊 Show normal disease prediction
  return <DiseaseResultCard primary={result.primary_disease} />
}

// Fallback
return <ErrorCard />
```

---

## Database Schema Reference

```python
# Symptoms Database (in SymptomDiseasePredictor.__init__)

self.symptom_disease_db = {
    # Key: symptom (underscore format)
    # Value: list of diseases
    
    'fever': [
        'flu',      # 🏥 Can predict
        'covid',
        'malaria',
        'typhoid',
        'dengue'
    ],
    
    'cough': [
        'cold',
        'flu',
        'covid',
        'tuberculosis',
        'bronchitis'
    ],
    
    # ... 8 more symptoms ...
    
    # ❌ NOT in database:
    # 'hair_loss', 'skin_rash', 'joint_pain', etc.
}

# Validation checks:
# is_symptom_supported('fever')           → True ✓
# is_symptom_supported('hair_loss')       → False ❌
# is_symptom_supported('Hair Loss')       → False ❌ (case matters)
# is_symptom_supported('hair loss')       → False ❌ (becomes 'hair_loss')
```

---

## Error Handling Paths

```
Request received
│
├─► If symptoms empty
│   └─► Return 400: "No symptoms provided"
│
├─► If NLP fails
│   └─► [Existing behavior, still works]
│
├─► If validation detects unsupported
│   └─► Return 200 + {status: "unsupported_symptom"}
│       └─► Frontend shows graceful message
│
└─► If all supported
    └─► Do prediction
        ├─► If diseases found
        │   └─► Return 200 + {status: "success", ...results}
        │
        └─► If NO diseases found (edge case)
            └─► Return 200 + {status: "success", but empty results}
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Request Layer                     │
│  POST /api/symptoms {"symptoms": "..."}            │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│              Feature Engineering                    │
│  ┌─────────────────────────────────────┐            │
│  │ NLP Semantic Similarity Mapping      │            │
│  │ user input → known symptoms          │            │
│  │ "hair fall" → "hair loss" (92%)     │            │
│  └────────────────┬────────────────────┘            │
└───────────────────┼─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│           Validation Layer (NEW!)                   │
│  ┌─────────────────────────────────────┐            │
│  │ Check against Trained Symptoms DB   │            │
│  │ "hair loss" in DB? NO               │            │
│  │ → Return: UNSUPPORTED               │            │
│  └────────────────┬────────────────────┘            │
└───────────────────┼─────────────────────────────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
   Supported            Unsupported
        │                      │
        ▼                      ▼
┌───────────────┐     ┌──────────────────┐
│  Prediction   │     │  Fallback        │
│  Layer        │     │  Response        │
│               │     │                  │
│ ML Model      │     │ • Message        │
│ ├─ Flu (60%) │     │ • Suggestions    │
│ ├─ Covid(25%)│     │ • Guidance       │
│ └─ Other(15%)│     │ • Action buttons │
└───────┬───────┘     └────────┬─────────┘
        │                      │
        └───────────┬──────────┘
                    │
        ┌───────────▼──────────┐
        │  Response to Client  │
        │  (JSON)              │
        └───────────┬──────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Frontend Display     │
        │  ├─ Results Card OR   │
        │  └─ Fallback Card     │
        └───────────────────────┘
```

---

## System States

```
NORMAL SUCCESS STATE
→ Input: "fever, cough, headache"
→ Validation: ✓ All supported
→ Prediction: ✓ "Flu" (60%)
→ Response: status: "success"
→ Display: Disease cards, alternatives, explanations

GRACEFUL FAILURE STATE (NEW)
→ Input: "hair loss"
→ Validation: ❌ Unsupported
→ Prediction: [Skipped]
→ Response: status: "unsupported_symptom"
→ Display: Orange alert, suggestions, guidance

ERROR STATE
→ Input: [empty]
→ Validation: [Skipped]
→ Prediction: [Skipped]
→ Response: error: "No symptoms provided"
→ Display: Error message
```

---

## Component Hierarchy

```
SymptomPage
├─ InputForm
│  ├─ Textarea
│  ├─ QuickSymptomButtons (fever, cough, ...)
│  ├─ AnalyzeButton
│  └─ ClearButton
│
└─ ResultsDisplay
   ├─ NLPInterpretation (always shown if result exists)
   │  └─ MappingList (input → mapped → confidence)
   │
   ├─ ConditionalBlocks
   │  ├─ IF unsupported:
   │  │  └─ UnsupportedSymptomCard
   │  │     ├─ Alert (orange)
   │  │     ├─ UnsupportedList (red X items)
   │  │     ├─ SuggestionButtons (blue + items, clickable)
   │  │     ├─ GuidanceSectionCard
   │  │     └─ ActionButtons (Try Different, Clear)
   │  │
   │  ├─ ELSE IF supported:
   │  │  ├─ DiseaseCard (green primary)
   │  │  ├─ AlternativesCard
   │  │  ├─ DisclaimerCard
   │  │  └─ ActionButtons (Analyze Again, Save)
   │  │
   │  └─ OTHERWISE:
   │     └─ ErrorCard
   │
   └─ EmergencyAlert (if present, always on top)
```

---

## Performance Characteristics

```
Time Complexity:
├─ NLP Mapping: O(1) + semantic similarity O(n)
│  where n = number of known symptoms (10)
│
├─ Validation: O(n) simple lookup
│  where n = number of user symptoms (typically 1-3)
│
├─ Suggestion generation: O(m log m)
│  where m = total symptoms in database (10)
│  → Sorted once, take top 5
│
└─ Total: ~O(n + m) ≈ O(13) = constant time

Space Complexity:
├─ Database: O(10) constant
├─ Response: O(n) linear in number of symptoms
└─ Total: O(constant + linear) = O(n)

Latency Impact:
├─ Validation check: +5-10ms
├─ Suggestion creation: +1-3ms
├─ Total overhead: ~10-15ms per request
└─ Acceptable: <100ms total response time still
```

---

## Future Architecture Changes

```
Current:
User → NLP → Validation → [Success/Fallback] → Display

Planned v2:
User → NLP → Validation → Smart Routing
├─→ If unsupported but similar to known:
│  └─ Use fuzzy similarity to suggest mapping
│
└→ If completely unknown:
   └─ Return fallback + semantic search results
   
Planned v3:
Add ML-based fallback:
├─ Learn from user corrections
├─ Build synonym dictionary
└─ Eventually auto-map unsupported → supported
```

