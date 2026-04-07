import openai
import os
from dotenv import load_dotenv

load_dotenv()

class HealthAI:
    """
    Generative AI module for health conversations using OpenAI
    """
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        
        self.system_prompt = """You are a helpful health assistant AI. 
        You provide general health information and advice. 
        IMPORTANT: Always remind users that this is not a substitute for professional medical advice.
        If the issue seems serious, recommend seeing a doctor immediately.
        Keep responses concise and helpful."""
    
    def get_response(self, user_message):
        """Get AI response to health-related question"""
        try:
            if not self.api_key:
                return self.get_fallback_response(user_message)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error with OpenAI API: {str(e)}")
            return self.get_fallback_response(user_message)
    
    def get_fallback_response(self, user_message):
        """Provide fallback response when OpenAI is not available"""
        responses = {
            'fever': 'Fever is a sign your body is fighting an infection. Rest, stay hydrated, and take over-the-counter fever reducers if needed. See a doctor if it persists beyond 3 days.',
            'cough': 'A persistent cough could indicate various conditions. Try drinking warm liquids, using lozenges, and staying hydrated. If it lasts more than 3 weeks, consult a doctor.',
            'headache': 'Try resting in a quiet, dark room, staying hydrated, and doing relaxation exercises. Over-the-counter pain relievers can help. See a doctor if severe or frequent.',
            'fatigue': 'Fatigue can result from stress, poor sleep, or illness. Ensure adequate sleep (7-9 hours), eat balanced meals, and exercise. If persistent, consult a healthcare provider.',
            'default': 'Thank you for your health question. I recommend consulting with a healthcare professional for personalized medical advice. In emergencies, call 911.',
        }
        
        message_lower = user_message.lower()
        for key, response in responses.items():
            if key in message_lower:
                return response
        
        return responses['default']

# Create global AI instance
health_ai = HealthAI()

def get_ai_response(message):
    """Public function to get AI response"""
    return health_ai.get_response(message)
