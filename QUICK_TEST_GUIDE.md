# Quick Testing Guide - Context-Aware Features

## Test These Inputs to Verify Smart Responses

### ✅ Test 1: Polite Response
```
Input:  "Thanks for the help!"
Expect: Friendly welcome message without error
Result: _____ (test yourself)
```

### ✅ Test 2: High Fever Alert
```
Input:  "I have 104F fever"
Expect: Mentions 104°F specifically, says "quite high", "seek medical attention soon"
Result: _____ (test yourself)
```

### ✅ Test 3: Mild Fever Conservative
```
Input:  "I have 99.5 temperature"
Expect: Mentions 99.5°F specifically, says "mild", recommends rest/hydration
Result: _____ (test yourself)
```

### ✅ Test 4: Week-Long Fever
```
Input:  "I have fever for a week"
Expect: Mentions "week", says "definitely needs medical evaluation"
Result: _____ (test yourself)
```

### ✅ Test 5: Worsening Symptoms
```
Input:  "My symptoms are getting worse, should I see a doctor?"
Expect: Says "definitely see doctor", mentions "worsening"
Result: _____ (test yourself)
```

### ✅ Test 6: Month-Long Issue
```
Input:  "I have pain for a month, see a doctor?"
Expect: Mentions "over a month", says "definitely consult doctor"
Result: _____ (test yourself)
```

### ✅ Test 7: Consistency Check
```
Input:  "I have fever" (twice)
Expect: Same response both times (safe, just consistent)
Result: _____ (test yourself)
```

### ✅ Test 8: Temperature Formats
```
Input A: "101F"        → Expect: Uses 101°F
Input B: "39.2C"       → Expect: Uses converted temperature (~102.56°F)
Input C: "38°C fever"  → Expect: Uses converted temperature (~100.4°F)
Result: _____ (test yourself)
```

### ✅ Test 9: Emergency Detection
```
Input:  "Can't breathe and have chest pain"
Expect: IMMEDIATE emergency response, "seek medical attention immediately"
Result: _____ (test yourself)
```

### ✅ Test 10: Response Format
```
Input:  Any question
Expect: Always 2-3 sentences + disclaimer
        "Consult a healthcare professional for personalized advice."
Result: _____ (test yourself)
```

---

## What Should NOT Happen

❌ Generic responses ("A fever can be caused by many things...")
❌ Ignored temperature values (should mention the number)
❌ Missed duration mentions (should reference "week" if given)
❌ Same response every time (context should vary it)
❌ Crashes on "thanks" or polite language
❌ Missing disclaimer at end
❌ More than 3-4 sentences

---

## Feature Checklist

- [ ] Temperature extraction works (101F, 39.2C)
- [ ] Duration extraction works (week, month, days)
- [ ] Fever responses differ by severity (99F vs 104F)
- [ ] Doctor responses differ by duration (hours vs weeks)
- [ ] Emergency detected immediately
- [ ] Polite responses handled gracefully
- [ ] All responses include disclaimer
- [ ] All responses are 2-3 sentences
- [ ] No diagnosis/medicine/wrong doctor advice
- [ ] System doesn't crash on edge cases

---

## Automated Test Suite

Run all 10 tests automatically:

```bash
cd backend
python test_context_aware.py
```

Expected output: **ALL 10 TESTS PASSED** ✅

---

## Debug Tips

If a test fails:

1. **Check backend is running**
   ```
   cd backend
   python app.py
   ```

2. **Verify Ollama is running**
   - Model should be: `phi3`
   - Check: http://localhost:11434

3. **Check temperature extraction**
   - Look for pattern: `(\d{2,3}(?:\.\d)?)`
   - Should match: "101", "101.5", "99.5"

4. **Check duration extraction**
   - Should detect: "week", "month", "days", "just", "today"
   - Should map to normalized text

5. **Check response includes requested info**
   - If given temp → should mention it
   - If given duration → should reference it
   - No data → fallback to generic safe response

---

## Success Criteria

✅ All inputs above get specific, context-aware responses
✅ No generic fallback responses (except truly ambiguous cases)
✅ Emergency detected immediately
✅ Temperatures/durations mentioned explicitly
✅ All responses 2-3 sentences + disclaimer
✅ Zero crashes on any input

---

## Next Steps

1. Run automated tests: `python test_context_aware.py`
2. Manual chat tests using scenarios above
3. Verify emergency handling
4. Check temperature parsing with various formats
5. Verify duration-based routing

Ready for production! 🎉

