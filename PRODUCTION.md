# 🏥 AI Health Assistant + Fake Medicine Detector
## Production-Ready Hackathon Application

### 🌟 Features

#### 1. **🩺 Smart Symptom Checker**
- Input multiple symptoms
- AI-powered disease prediction (Random Forest ML)
- Top 3 disease predictions with confidence scores (0-100%)
- Risk level assessment (High/Medium/Low)
- Emergency alert detection
- Personalized medical advice per disease
- Symptoms history with timeline view

#### 2. **💊 Advanced Medicine Detector**
- **3-Layer Detection System:**
  - **OCR Analysis** (40% weight): Extracts medicine name & batch number
  - **Image Quality Analysis** (40% weight): Hologram, barcode, color consistency, text clarity
  - **Rule-Based Checks** (20% weight): Resolution, blur, brightness validation
- Real-time authenticity verification
- ≥70% confidence = Authentic ✓
- Detailed analytics breakdown
- Medicine verification history

#### 3. **📋 Complete Health History**
- Timeline view of all analyses
- Switch between symptom & medicine history
- Detailed report viewing with full metrics
- Export-ready formatted data
- Persistent storage in SQLite database

#### 4. **💬 AI Chat Assistant**
- Ask health-related questions
- AI-powered responses
- Integrated with OpenAI API (optional)

---

## 🏗️ Architecture

### Backend Stack
```
Flask + Flask-SQLAlchemy + Flask-CORS
├── Python 3.11+
├── Machine Learning
│   ├── Random Forest Classifier (symptoms)
│   ├── OpenCV (image analysis)
│   └── Scikit-learn (ML models)
├── Database: SQLite (local) / PostgreSQL (production)
└── OCR: Tesseract (pytesseract)
```

### Frontend Stack
```
React 18 + Vite + Tailwind CSS
├── GSAP animations
├── Real-time API integration
├── Responsive design
└── Modern glass-morphism UI
```

---

## 🚀 Quick Start

### Local Development

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd ai-health-assistant
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   # Backend running at http://localhost:5000
   ```

3. **Setup Frontend**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   # Frontend running at http://localhost:5174
   ```

4. **Access the application**
   - Open browser to `http://localhost:5174`
   - Start with Symptom Checker or Medicine Detector
   - Check History to view past analyses

---

## 📊 API Endpoints

### Health Check
```
GET /api/health
```

### Symptoms
```
POST /api/symptoms
Body: { "symptoms": ["fever", "cough"] }

GET /api/symptoms/suggestions
GET /api/symptoms/history?limit=10
GET /api/symptoms/report/<id>
```

### Medicine Verification
```
POST /api/verify-medicine
Body: multipart/form-data with image

GET /api/medicine/history?limit=10
GET /api/medicine/report/<id>
```

### Statistics
```
GET /api/stats
```

---

## 💾 Database Schema

### SymptomAnalysis
- ID (primary key)
- user_symptoms (JSON)
- primary_disease
- confidence (float)
- risk_level
- emergency_alert (boolean)
- all_results (JSON)
- recommendations (JSON)
- created_at (timestamp)

### MedicineVerification
- ID (primary key)
- image_filename
- is_authentic (boolean)
- confidence (float)
- ocr_data (JSON)
- image_analysis (JSON)
- decision_logic (JSON)
- recommendation
- created_at (timestamp)

---

## 🧪 Testing the Application

### Test Symptom Checker
1. Go to "Symptom" tab
2. Click quick-select buttons: "Fever" → "Cough"
3. Click "Analyze Symptoms"
4. View predictions with risk levels and advice

**Example Symptoms to Try:**
- Fever + Cough = Common Cold/COVID-19
- Chest Pain + Shortness of Breath = Cardiovascular issues
- Headache + Nausea + Vomiting = Migraine/Meningitis

### Test Medicine Detector
1. Go to "Medicine" tab
2. Upload a medicine box photo
3. Drag-drop or click to select
4. View:
   - OCR extracted data (medicine name, batch#)
   - Image quality metrics
   - Decision logic breakdown
   - Final authenticity verdict

**Test with:**
- Actual medicine box photos
- High-quality images work best
- Image must show packaging clearly

### Check History
1. Go to "History" tab
2. Switch between Symptoms & Medicine tabs
3. Click any item to view full detailed report
4. See confidence scores, risk levels, recommendations

---

## 🌍 Deployment

### Deploy to Heroku
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Deploy to Railway
```bash
railway init
railway up
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📈 Real Medicine Database

Over 60+ real medicines included:
- **Fever/Pain:** Paracetamol, Ibuprofen, Aspirin, Diclofenac
- **Antibiotics:** Amoxicillin, Azithromycin, Ciprofloxacin
- **Digestive:** Omeprazole, Metoclopramide, Loperamide
- **Heart:** Amlodipine, Enalapril, Metoprolol
- **Diabetes:** Metformin, Glipizide, Insulin
- **Vitamins:** B12, D3, Multivitamins, Iron, Calcium
- + More categories

---

## 🔒 Production Checklist

- [x] Database persistence with SQLAlchemy
- [x] API endpoints for history & reports
- [x] Error handling & logging
- [x] CORS properly configured
- [x] Deployment files (Procfile, requirements.txt)
- [x] Environment configuration (.env.example)
- [x] Real medicine database
- [ ] Rate limiting
- [ ] Authentication (optional)
- [ ] HTTPS/SSL certificates (on deployment)
- [ ] Database backups (on deployment)

---

## 📝 Project Structure

```
ai-health-assistant/
├── backend/
│   ├── app.py                          # Flask app with all routes
│   ├── database.py                     # SQLAlchemy models
│   ├── medicine_database.py            # Real medicine data
│   ├── requirements.txt                # Python dependencies
│   ├── ml_models/
│   │   ├── symptom_disease_model.py   # Disease prediction (Random Forest)
│   │   └── medicine_detector_enhanced.py # 3-layer medicine verification
│   └── ai_module/
│       └── health_ai.py               # Chat functionality
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Main React component
│   │   ├── components/
│   │   │   ├── AnimatedBackground3D.jsx
│   │   │   └── UI.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── .env.example                        # Configuration template
├── .gitignore
├── Procfile                           # Heroku deployment
├── runtime.txt                        # Python version
├── DEPLOYMENT.md                      # Deployment guide
└── README.md                          # This file
```

---

## 🎯 Hackathon Features

✅ **Fully Functional AI System**
- Real ML models (not mock)
- Real API endpoints
- Real database storage
- Professional UI/UX

✅ **Production Ready**
- Error handling
- Input validation
- Response caching
- Deployment ready

✅ **Scalable Architecture**
- Database persistence
- API designed for scale
- Cloud deployment ready
- Can handle N+ concurrent users

✅ **Real-World Impact**
- Helps identify fake medicines
- Aids symptom diagnosis
- Provides medical advice
- Saves patient history

---

## 📦 Performance

- **Response time:** <2 seconds for analysis
- **Database:** Optimized queries with indexing
- **Frontend:** Vite dev server (instant HMR)
- **Animations:** GPU-accelerated GSAP
- **Images:** Optimized with Tailwind purging

---

## 🔐 Security Considerations

- Input validation on all endpoints
- CORS configured for production
- SQL injection protected (SQLAlchemy ORM)
- XSS prevention (React auto-escaping)
- Environment variables for secrets

---

## 🤝 Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - Feel free to use for personal or commercial projects

---

## 🎓 Technologies Used

- **Frontend:** React, Vite, Tailwind CSS, GSAP
- **Backend:** Flask, SQLAlchemy, Scikit-learn, OpenCV
- **ML:** Random Forest, Image Processing
- **DevOps:** Docker (optional), Heroku/Railway
- **Database:** SQLite, PostgreSQL (production)

---

## 📞 Support

For issues or questions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for setup help
2. Review API endpoints above
3. Check browser console for frontend errors
4. Run `heroku logs --tail` for backend errors

---

## 🌟 Quick Tips

- **Symptom Checker:** Be specific with symptoms for better predictions
- **Medicine Detector:** Use clear, well-lit photos of medicine packaging
- **History:** Click any item to see detailed breakdown
- **Testing:** Use the provided test scenarios above
- **Deployment:** Follow [DEPLOYMENT.md](DEPLOYMENT.md) exactly

---

**Made with ❤️ for Healthcare Innovation**

Start using AI Health Assistant today! 🚀
