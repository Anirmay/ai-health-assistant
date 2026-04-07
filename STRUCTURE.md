# Project Structure

```
ai-health-assistant/
│
├── frontend/                          # React application with 3D animations
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnimatedBackground3D.jsx    # 3D particle system & shapes
│   │   │   └── UI.jsx                      # Reusable UI components
│   │   ├── App.jsx                         # Main app with 5 pages
│   │   ├── main.jsx                        # React entry point
│   │   └── index.css                       # Global styles & animations
│   ├── index.html                     # HTML template
│   ├── package.json                   # Frontend dependencies
│   ├── vite.config.js                 # Vite configuration
│   ├── tailwind.config.js             # Tailwind CSS config
│   └── postcss.config.js              # PostCSS config
│
├── backend/                           # Python Flask API
│   ├── ml_models/
│   │   ├── symptom_predictor.py       # Disease prediction ML model
│   │   ├── medicine_detector.py       # Image analysis for fake medicines
│   │   ├── trained_models/            # Pre-trained ML models
│   │   └── __init__.py
│   ├── ai_module/
│   │   ├── health_ai.py               # OpenAI integration
│   │   └── __init__.py
│   ├── app.py                         # Flask main application
│   ├── requirements.txt               # Python dependencies
│   ├── .env                           # Environment variables
│   └── config.py                      # Configuration (to create)
│
├── models/                            # ML Model storage
│   └── trained_models/                # Pre-trained model files
│
├── docs/                              # Documentation
│   ├── SETUP.md                       # Setup instructions
│   ├── API.md                         # API documentation
│   └── FEATURES.md                    # Feature descriptions
│
├── README.md                          # Project overview
└── .git/                              # Git repository
```

## Directory Breakdown

### Frontend Structure
```
frontend/
├── Components Layer
│   ├── AnimatedBackground3D.jsx  → 3D animated background with particles
│   └── UI.jsx                    → Loading, alerts, badges, progress bars
│
├── Pages
│   ├── HomePage          → Dashboard with feature cards
│   ├── SymptomChecker    → Text input for symptom analysis
│   ├── MedicineVerifier  → Image upload for medicine verification
│   ├── HealthHistory     → Past consultations
│   └── AIChatBot         → Chat interface
│
└── Styling
    ├── Tailwind CSS     → Utility-first styling
    ├── Framer Motion    → Smooth animations
    └── Three.js         → 3D graphics
```

### Backend Structure
```
backend/
├── API Layer (app.py)
│   ├── /api/health              → Health check
│   ├── /api/symptoms            → Disease prediction
│   ├── /api/verify-medicine     → Medicine verification
│   ├── /api/chat                → AI chat
│   └── /api/history             → User history
│
├── ML Models
│   ├── SymptomPredictor         → Random Forest classifier
│   └── MedicineDetector         → OpenCV image analysis
│
└── AI Module
    └── HealthAI                 → OpenAI integration
```

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/App.jsx` | Main React component with all 5 pages |
| `frontend/src/components/AnimatedBackground3D.jsx` | 3D animated background |
| `backend/app.py` | Flask API with all endpoints |
| `backend/ml_models/symptom_predictor.py` | ML model for disease prediction |
| `backend/ml_models/medicine_detector.py` | OpenCV image processing |
| `backend/ai_module/health_ai.py` | OpenAI ChatGPT integration |

## Technologies Used

### Frontend
- **React 18** - UI framework
- **Three.js** - 3D graphics and animations
- **Framer Motion** - Smooth animations
- **Tailwind CSS** - Styling
- **Vite** - Build tool

### Backend
- **Flask** - Web framework
- **TensorFlow** - Deep learning
- **Scikit-learn** - ML models
- **OpenCV** - Image processing
- **OpenAI API** - Generative AI

### Database (future)
- **Firebase** or **PostgreSQL**

## Scale & Scalability

### Current Capacity
- Single backend server
- In-memory model storage
- No database (future)

### For Production
- Add load balancing (Nginx)
- Use database (PostgreSQL)
- Cache predictions (Redis)
- Add user authentication (JWT)
- Implement rate limiting
- Add monitoring (Prometheus)

## Development Workflow

1. **Frontend Development**
   ```bash
   cd frontend && npm run dev
   ```

2. **Backend Development**
   ```bash
   cd backend && python app.py
   ```

3. **Testing**
   - Frontend: Manual testing in browser
   - Backend: Use curl or Postman

4. **Deployment**
   - Frontend: Vercel/Netlify
   - Backend: Heroku/Railway

## Future Enhancements

- [ ] User authentication & profiles
- [ ] Database integration
- [ ] More ML models
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Doctor consultation booking
- [ ] Medical records storage
- [ ] Wearable device integration
