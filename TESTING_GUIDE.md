# 🧪 Testing Guide - AI Health Assistant

## ✅ How to Verify Both Pages Work Perfectly

---

## 📋 SYMPTOM PAGE TESTING CHECKLIST

### **Test 1: Basic Navigation**
- [ ] Click "Symptom" button in navigation
- [ ] URL changes to `http://localhost:5174/symptom`
- [ ] Page title shows "🩺 Symptom Analyzer"

### **Test 2: Select Symptoms**
- [ ] Click symptom buttons: "+ fever", "+ cough", "+ fatigue"
- [ ] Symptoms appear in text input box
- [ ] Buttons show active state (highlight)

### **Test 3: Analyze Symptoms**
- [ ] Click "🔍 Analyze Symptoms" button
- [ ] Results appear within 2 seconds
- [ ] Primary prediction shows (e.g., "Covid")

### **Test 4: Verify Results Display**
- [ ] ✅ **PRIMARY PREDICTION section shows:**
  - Disease name (e.g., "Covid")
  - Confidence percentage (e.g., "95%")
  - Risk Level: "High" (in yellow)
  - Symptoms Matched: "3" (count of matched symptoms)

- [ ] ✅ **WHEN TO SEE DOCTOR section shows:**
  - Medical urgency text
  - Example: "Get tested immediately - Consult doctor if symptoms worsen"
  - Should have blue/cyan border

### **Test 5: Verify Reasoning (Explainability)**
*This is the KEY feature for judges!*
- [ ] After results, look for "Why This Prediction?" section
- [ ] Should show:
  - ✓ Matched Symptoms tags: ["Fever", "Cough", "Fatigue"]
  - ✓ AI Explanation text
  - ✓ Confidence Level text (e.g., "Very High")
  - ✓ Symptoms Matched ratio (e.g., "3 of 5")

### **Test 6: Alternative Possibilities**
- [ ] Flu appears with 66% confidence
- [ ] Malaria appears with 33% confidence
- [ ] Each has medical advice

### **Test 7: Important Features**
- [ ] Disclaimer shown at bottom
- [ ] "Analyze Again" button works
- [ ] "Save Results" button available

---

## 💊 MEDICINE PAGE TESTING CHECKLIST

### **Test 1: Basic Navigation**
- [ ] Click "Medicine" button in navigation
- [ ] URL changes to `http://localhost:5174/medicine`
- [ ] Page title shows "🧬 Medicine Authenticator"

### **Test 2: Upload Medicine Image**
- [ ] Click upload area or drag-drop an image
- [ ] Image preview appears
- [ ] File name displayed (e.g., "medicine.jpg")
- [ ] "✕ Clear" button available

### **Test 3: Verify Authenticity**
- [ ] Click "🔐 Verify Authenticity" button
- [ ] Results appear within 3 seconds
- [ ] Shows "✓ AUTHENTIC" or "✗ COUNTERFEIT"

### **Test 4: Verify Main Results**
- [ ] ✅ **VERIFICATION RESULT section shows:**
  - Status badge (AUTHENTIC or COUNTERFEIT)
  - Color indicator (green or red)
  - Warning emoji if suspicious

- [ ] ✅ **AI CONFIDENCE LEVEL section shows:**
  - Percentage (e.g., "68%")
  - Recommendation text
  - Example: "⚠️ CAUTION: May be counterfeit"

### **Test 5: Verify Reasoning (3-Layer Breakdown)**
*This is the STAR feature!*
- [ ] Look for "🔍 Detailed Analysis Breakdown" section
- [ ] Should show THREE layers with status badges:

  **Layer 1: OCR Verification**
  - [ ] Status: ✅ PASS or ⚠️ WARNING or ❌ FAIL
  - [ ] Detail: Shows medicine name or "Not detected"
  - [ ] Score bar and percentage

  **Layer 2: Image Quality Analysis**
  - [ ] Status: ✅ PASS or ⚠️ WARNING or ❌ FAIL
  - [ ] Detail: Checks for:
    - ✓ Hologram detection
    - ✓ Barcode validity
    - ✓ Color consistency
    - ✓ Text clarity
  - [ ] Overall quality rating (Excellent/Good/Fair/Poor)

  **Layer 3: Technical Checks**
  - [ ] Status: ✅ PASS or ⚠️ WARNING
  - [ ] Detail: Shows:
    - ✓ Resolution quality
    - ✓ Blur detection
    - ✓ Brightness level

### **Test 6: Verify OCR Data Extraction**
- [ ] "🔍 OCR Data Extraction" section shows:
  - [ ] Medicine Name
  - [ ] Batch Number
  - [ ] Database Match status
  - [ ] OCR Confidence percentage

### **Test 7: Verify Image Quality Analysis**
- [ ] "🎨 Image Quality Analysis" section shows:
  - [ ] Hologram Detection (%)
  - [ ] Barcode Quality (%)
  - [ ] Color Consistency (%)
  - [ ] Text Clarity (%)
  - [ ] Overall Packaging Quality (rating)

### **Test 8: Verify Decision Logic**
- [ ] "⚙️ Decision Logic Breakdown" section shows:
  - [ ] Component scores with percentages
  - [ ] Component weights (40%, 40%, 20%)
  - [ ] Threshold for authenticity (≥70%)
  - [ ] Final confidence calculation

### **Test 9: Additional Features**
- [ ] Scanned image preview displayed
- [ ] "📸 Verify Another" button works
- [ ] "💾 Save Report" button available
- [ ] Medical recommendation text shown

---

## 🧪 QUICK VERIFICATION TEST

### **Run This Quick Test (5 minutes)**

#### **SYMPTOM PAGE - Quick Test:**
```
1. Click "Symptom" button
2. Click: + fever, + cough, + fatigue
3. Click "Analyze Symptoms"
4. VERIFY YOU SEE:
   ✓ Primary prediction (Covid)
   ✓ 95% confidence
   ✓ Risk: High
   ✓ Matched: 3 symptoms
   ✓ When to see doctor: "Get tested immediately..."
   ✓ Alternative options: Flu (66%), Malaria (33%)
```

#### **MEDICINE PAGE - Quick Test:**
```
1. Click "Medicine" button
2. Upload any image file
3. Click "Verify Authenticity"
4. VERIFY YOU SEE:
   ✓ Result: AUTHENTIC/COUNTERFEIT
   ✓ Confidence level (e.g., 68%)
   ✓ 3 Reasoning Layers with status badges
   ✓ OCR data extraction section
   ✓ Image quality analysis
   ✓ Technical checks breakdown
```

---

## 🎯 HACKHATHON JUDGE CHECKLIST

**Judges will look for these KEY things:**

### **Explainability (Most Important)**
- [ ] **Symptom Page**: Shows WHY it predicted COVID (matched symptoms, confidence level)
- [ ] **Medicine Page**: Shows THREE layers of reasoning (OCR, Image Quality, Technical)
- [ ] **Both**: Clear visual indicators (badges, colors, percentages)

### **Transparency**
- [ ] Results are explained in human-readable format
- [ ] Confidence levels clearly displayed
- [ ] Layer-by-layer breakdown visible
- [ ] When to see doctor recommendations provided

### **User Experience**
- [ ] Both pages load quickly
- [ ] Results appear within 2-3 seconds
- [ ] UI is clean and professional
- [ ] Color-coded status indicators (green/yellow/red)

### **Medical Features**
- [ ] Alternative predictions shown
- [ ] Medical advice provided
- [ ] Urgent care recommendations included
- [ ] Disclaimer present

---

## 📊 EXPECTED API RESPONSES

### **Symptom API Response Should Include:**
```json
{
  "primary_disease": "Covid",
  "results": [
    {
      "disease": "Covid",
      "confidence": 95,
      "reasoning": {
        "matched_symptoms": ["Fever", "Cough", "Fatigue"],
        "explanation": "Your symptoms are commonly associated with Covid",
        "confidence_level": "Very High",
        "match_count": 3
      }
    }
  ],
  "when_to_see_doctor": "Get tested immediately...",
  "risk_level": "High"
}
```

### **Medicine API Response Should Include:**
```json
{
  "is_authentic": false,
  "final_confidence": 0.68,
  "reasoning": [
    {
      "layer": "OCR Verification",
      "status": "PASS",
      "detail": "✓ Medicine found...",
      "score": 0.85
    },
    {
      "layer": "Image Quality Analysis",
      "status": "WARNING",
      "detail": "✓ Hologram: 70%, ✗ Barcode: 30%",
      "score": 0.58
    },
    {
      "layer": "Technical Checks",
      "status": "PASS",
      "detail": "✓ Resolution: Good, ✓ Not blurry",
      "score": 1.0
    }
  ],
  "recommendation": "⚠️ May be counterfeit"
}
```

---

## 🔍 DEBUGGING TIPS

### **If Symptom Page Not Working:**
- [ ] Check browser console for errors (F12)
- [ ] Verify backend running: `curl http://localhost:5000/api/health`
- [ ] Try different symptoms
- [ ] Check API response: `curl -X POST http://localhost:5000/api/symptoms -H "Content-Type: application/json" -d '{"symptoms": ["fever"]}'`

### **If Medicine Page Not Working:**
- [ ] Ensure image file exists and is readable
- [ ] Try different image formats (JPG, PNG)
- [ ] Check file size (max 5MB)
- [ ] Verify backend running
- [ ] Check browser console for upload errors

### **If Reasoning Not Showing:**
- [ ] Refresh page (Ctrl+R or Cmd+R)
- [ ] Clear browser cache
- [ ] Check that frontend was rebuilt: `npm run build`
- [ ] Check that backend has latest code

---

## ✨ SUCCESS CRITERIA

**Your project is working PERFECTLY if:**

✅ **Symptom Page:**
- Predictions appear with confidence scores
- "When to see doctor" shows medical urgency
- Matched symptoms are visible
- Alternative options with reasoning displayed

✅ **Medicine Page:**
- Verification result clearly shown (AUTHENTIC/COUNTERFEIT)
- Three reasoning layers displayed with status badges
- OCR data extraction shows
- Image quality metrics visible
- Detailed breakdown with percentages shown

✅ **Both Pages:**
- All UI elements load without errors
- Results appear within 3 seconds
- Navigation works smoothly
- URLs update correctly
- Reasoning is transparent and understandable

---

## 🚀 READY FOR HACKATHON!

If all checkboxes pass, your project is **HACKATHON-READY** with:
- ✅ Full explainability features
- ✅ Three-layer reasoning system
- ✅ Medical guidance integration
- ✅ Professional UI/UX
- ✅ Production-ready code

**Good luck with your hackathon submission! 🎯**
