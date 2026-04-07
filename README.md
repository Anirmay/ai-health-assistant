# AI Health Assistant 🏥

An intelligent healthcare solution that combines machine learning and generative AI to:
- 🩺 **Predict diseases** based on symptoms
- 💊 **Detect fake medicines** using image recognition
- 💬 **Provide conversational health advice** with Gen AI

## Features

### Core Features
- **Symptom Analyzer** - Enter symptoms, get disease predictions with confidence scores
- **Medicine Authenticator** - Verify medicine authenticity through image analysis
- **Risk Assessment** - Color-coded severity levels (Low/Medium/High/Critical)
- **Health Reports** - Download PDF reports of consultations
- **Chat Interface** - AI-powered conversational health Q&A

### UI/UX Features
- 3D Animated backgrounds with particle effects
- Smooth transitions and modern design
- Dark/Light mode support
- Mobile responsive
- Real-time predictions

## Tech Stack

### Frontend
- React 18
- Three.js (3D animations)
- Tailwind CSS
- Framer Motion (animations)
- OpenAI API integration

### Backend
- Python (3.8+)
- Flask/FastAPI
- TensorFlow/Scikit-learn
- OpenCV (medicine detection)

### Database
- Firebase or PostgreSQL

## Installation

### Frontend
```bash
cd frontend
npm install
npm start
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## Project Structure

```
ai-health-assistant/
├── frontend/          # React application with 3D animations
├── backend/           # Python ML backend
├── models/            # Pre-trained ML models
├── docs/              # Documentation
└── README.md
```

## Getting Started

1. Clone this repository
2. Follow the Installation section above
3. Configure API keys (OpenAI, Firebase)
4. Run frontend and backend servers
5. Visit http://localhost:3000

## Contributors

- Anirmay & Team

## License

MIT
