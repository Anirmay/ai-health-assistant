# Setup Guide

## Prerequisites
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- Git

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Run development server
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Build for production
```bash
npm run build
```

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
- Copy `.env` file and add your API keys:
  - `OPENAI_API_KEY`: Get from https://platform.openai.com/api-keys

### 5. Run the backend server
```bash
python app.py
```

The backend API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health`
- Response: `{ "status": "healthy", "service": "AI Health Assistant" }`

### Symptom Analysis
- **POST** `/api/symptoms`
- Payload: `{ "symptoms": "fever and cough" }`
- Response: Disease prediction with confidence

### Medicine Verification
- **POST** `/api/verify-medicine`
- Payload: FormData with image file
- Response: Authenticity result with confidence

### Chat with AI
- **POST** `/api/chat`
- Payload: `{ "message": "What should I do for a fever?" }`
- Response: AI-generated health advice

### User History
- **GET** `/api/history`
- Response: User's past health consultations

## Troubleshooting

### Frontend issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `npm cache clean --force`

### Backend issues
- Ensure virtual environment is activated
- Check Python version: `python --version`
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`

### CORS issues
- Backend already has CORS configured
- Ensure both servers are running

## Deployment

### Frontend (Vercel/Netlify)
1. Build: `npm run build`
2. Deploy `dist` folder

### Backend (Heroku/Railway)
1. Add `Procfile`: `web: python app.py`
2. Set environment variables
3. Deploy

## Features Overview

| Feature | Status | Tech |
|---------|--------|------|
| Symptom Checker | ✅ | ML/Scikit-learn |
| Medicine Verifier | ✅ | OpenCV |
| AI Chat | ✅ | OpenAI API |
| 3D Animations | ✅ | Three.js |
| Health History | 🔄 | Database |
| User Auth | 🔄 | JWT |

✅ = Implemented | 🔄 = In Progress
