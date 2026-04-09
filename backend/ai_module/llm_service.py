"""
Advanced AI Service using LLM (OpenAI GPT)
Comprehensive AI-powered health assistance with:
- Dynamic explanation generation
- Symptom extraction from natural language
- Chat-based health guidance
- Medicine detection explanations
"""

import os
import json
import sys
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY', '')
except ImportError:
    openai = None

class AIExplanationService:
    """Main service for LLM-based AI health assistant"""
    
    def __init__(self):
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.temperature = float(os.getenv('RESPONSE_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('MAX_TOKENS', '300'))
        self.timeout = int(os.getenv('REQUEST_TIMEOUT', '10'))
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        
        if self.api_key and openai:
            openai.api_key = self.api_key
        
        self.medical_disclaimer = (
            "⚠️ Medical Disclaimer: This information is for educational purposes only. "
            "Always consult a qualified healthcare provider for diagnosis and treatment."
        )
    
    def is_api_available(self) -> bool:
        """Check if OpenAI API is properly configured"""
        return bool(self.api_key and openai)
    
    def _call_openai(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Safely call OpenAI API with comprehensive error handling
        
        Returns:
            Response text or informative message
        """
        if not self.api_key:
            return (
                "ℹ️ Demo Mode: AI explanation not available. "
                "Set OPENAI_API_KEY in .env to enable full features."
            )
        
        if not openai:
            return "⚠️ OpenAI library not installed"
        
        try:
            tokens = max_tokens or self.max_tokens
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{
                    "role": "system",
                    "content": (
                        "You are a helpful medical information assistant. Provide accurate, "
                        "concise health information. Always emphasize consulting healthcare professionals. "
                        "Avoid making definitive diagnoses. Keep responses under 150 words."
                    )
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=self.temperature,
                max_tokens=tokens,
                timeout=self.timeout
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            error_type = type(e).__name__
            if "Authentication" in error_type:
                return "❌ Invalid API key"
            elif "RateLimit" in error_type:
                return "⏳ Rate limited - try again"
            elif "Timeout" in error_type:
                return "⏱️ Request timed out"
            else:
                return f"⚠️ Error: {str(e)[:80]}"
    
    # ============= EXPLANATION GENERATION =============
    def generate_explanation(self, disease: str, symptoms: List[str], confidence: int) -> Dict:
        """Generate dynamic explanation for predicted disease"""
        symptoms_str = ", ".join(symptoms)
        
        prompt = f"""Based on symptoms ({symptoms_str}), the system predicts {disease} with {confidence}% confidence.

Explain this prediction in 2-3 sentences:
1. Why these symptoms match {disease}
2. What general self-care helps
3. When to see a doctor

Be friendly and clear."""
        
        explanation = self._call_openai(prompt, max_tokens=150)
        
        return {
            "disease": disease,
            "confidence": f"{confidence}%",
            "explanation": explanation,
            "disclaimer": self.medical_disclaimer
        }
    
    # ============= SYMPTOM EXTRACTION =============
    def extract_symptoms_from_text(self, user_input: str, symptom_database: List[str]) -> Dict:
        """Extract symptoms from natural language description"""
        examples = ", ".join(symptom_database[:15])
        
        prompt = f"""From this description: "{user_input}"

Extract medical symptoms that match these known symptoms: {examples}

Respond in JSON format only:
{{
    "extracted_symptoms": ["symptom1", "symptom2"],
    "confidence": 0.95,
    "explanation": "Found X, Y, Z symptoms"
}}"""
        
        try:
            response = self._call_openai(prompt, max_tokens=150)
            data = json.loads(response)
            return {
                "extracted_symptoms": data.get("extracted_symptoms", []),
                "confidence": data.get("confidence", 0.7),
                "explanation": data.get("explanation", "Symptoms identified")
            }
        except:
            # Fallback if JSON parsing fails
            return {
                "extracted_symptoms": [],
                "confidence": 0.5,
                "explanation": "Could not parse response"
            }
    
    # ============= CHAT/CONVERSATIONAL AI =============
    def chat_answer(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Generate conversational response with context"""
        context_str = ""
        if context:
            disease = context.get("disease", "unknown")
            symptoms = context.get("symptoms", [])
            context_str = f"\nContext: Patient has {disease} with symptoms: {', '.join(symptoms)}\n"
        
        prompt = f"""Patient question: "{message}"{context_str}

Provide a helpful, safe health response in 2-3 sentences. 
Never claim to diagnose. Suggest seeing a doctor when appropriate.
Include 2 follow-up questions they might ask."""
        
        answer = self._call_openai(prompt, max_tokens=150)
        
        followups = [
            "Should I see a doctor?",
            "What can I do to feel better?",
            "Is this condition serious?"
        ]
        
        return {
            "answer": answer,
            "follow_up_suggestions": followups,
            "disclaimer": self.medical_disclaimer
        }
    
    # ============= HEALTH ADVICE =============
    def generate_health_advice(self, disease: str, symptoms: List[str], risk_level: str) -> Dict:
        """Generate personalized health advice"""
        symptoms_str = ", ".join(symptoms)
        
        prompt = f"""For someone with {disease} ({risk_level} risk level) and symptoms {symptoms_str}:

Provide 3-4 specific, actionable health advice points:
1. Immediate actions
2. When to seek help
3. General wellness tips
4. Prevention

Be concise but helpful."""
        
        advice = self._call_openai(prompt, max_tokens=200)
        
        return {
            "disease": disease,
            "risk_level": risk_level,
            "advice": advice,
            "disclaimer": self.medical_disclaimer
        }
    
    # ============= MEDICINE DETECTION EXPLANATION =============
    def explain_medicine_detection(self, medicine_name: str, detection_result: Dict) -> Dict:
        """Generate explanation for medicine detection/verification"""
        confidence = detection_result.get("confidence", 0)
        is_authentic = detection_result.get("is_recognized", False)
        packaging = detection_result.get("packaging_quality", "unknown")
        
        prompt = f"""Medicine: {medicine_name}
Detection: Confidence {confidence:.0%}, {'Recognized' if is_authentic else 'Not recognized'}, Packaging: {packaging}

Explain in 2-3 sentences:
1. What the detection means
2. Reliability of the result
3. What to do next

Be clear and practical."""
        
        explanation = self._call_openai(prompt, max_tokens=150)
        
        return {
            "medicine": medicine_name,
            "is_authentic": is_authentic,
            "confidence": f"{confidence:.0%}",
            "explanation": explanation,
            "disclaimer": self.medical_disclaimer
        }
    
    # ============= SYSTEM STATUS =============
    def get_system_status(self) -> Dict:
        """Get AI service status and configuration"""
        api_available = self.is_api_available()
        
        return {
            "status": "operational" if api_available else "demo_mode",
            "api_key_configured": bool(self.api_key),
            "model": self.model,
            "mode": "Full AI" if api_available else "Demo (limited)",
            "message": (
                "✅ AI features enabled" if api_available
                else "ℹ️ Running in demo mode - set OPENAI_API_KEY to enable"
            )
        }


# Singleton instance
_service = None

def get_ai_service() -> AIExplanationService:
    """Get or create the AI service instance"""
    global _service
    if _service is None:
        _service = AIExplanationService()
    return _service
