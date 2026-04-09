"""
Ollama Local LLM Service
Provides AI explanations using locally running phi3 model via Ollama.
No API keys needed - works completely offline!
"""

import os
import json
import requests
import logging
from typing import Dict, List, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


class OllamaService:
    """
    Service for interacting with local Ollama LLM (phi3).
    Provides methods for all AI explanation tasks.
    """

    def __init__(self):
        """Initialize Ollama service with configuration from environment."""
        self.api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "gemma:2b")
        # Timeout set to 40 seconds for lightweight model (gemma:2b can be slow)
        self.timeout = max(40, int(os.getenv("OLLAMA_TIMEOUT", "40")))
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "80"))
        self.num_predict = int(os.getenv("LLM_NUM_PREDICT", "70"))
        # Response timeout also needs to be 40 seconds
        self.response_timeout = max(40, int(os.getenv("LLM_RESPONSE_TIMEOUT", "40")))
        
        self.api_endpoint = f"{self.api_url}/api/generate"
        self._is_available = None
        self.chat_history = []  # Store last 2-3 messages for context
        
        print(f"✅ Ollama Service initialized: {self.model} model, {self.timeout}s timeout, {self.num_predict} tokens max")
        logger.info(f"✅ Ollama Service initialized: {self.model} model, {self.timeout}s timeout, {self.num_predict} tokens max")

    @property
    def is_available(self) -> bool:
        """Check if Ollama service is running and accessible."""
        if self._is_available is not None:
            return self._is_available
        
        try:
            response = requests.get(
                f"{self.api_url}/api/tags",
                timeout=5
            )
            self._is_available = response.status_code == 200
            if self._is_available:
                logger.info("✅ Ollama service is available and running")
            return self._is_available
        except Exception as e:
            logger.warning(f"⚠️ Ollama not available: {str(e)}")
            self._is_available = False
            return False

    def _get_predefined_response(self, message_lower: str) -> Optional[Dict]:
        """
        Get predefined safe response for common questions without LLM.
        Optimization: Returns instantly, no LLM call needed.
        """
        # Recovery time questions
        if any(word in message_lower for word in ['how long', 'how much time', 'recovery', 'when will i', 'how soon', 'takes to recover']):
            if 'fever' in message_lower or 'cold' in message_lower or 'flu' in message_lower:
                return {
                    "answer": "Most fevers resolve within 3-7 days with rest and hydration. However, duration varies by cause. If symptoms persist beyond a week, see a doctor.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["My fever lasted over a week", "What can I take?"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
            elif 'cold' in message_lower:
                return {
                    "answer": "A common cold typically improves within 3-10 days. Rest, stay hydrated, and monitor symptoms. If symptoms worsen, see a doctor.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["My symptoms aren't improving", "Should I see someone?"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
            else:
                return {
                    "answer": "Recovery time depends on the condition. Rest, hydration, and monitoring are important. If symptoms persist beyond a few days or worsen, consult a doctor.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["Tell me your symptoms", "How long has it been?"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
        
        # "Should I see a doctor" questions
        if any(word in message_lower for word in ['should i see', 'need to see', 'do i need', 'visit doctor', 'when to see']) and 'doctor' in message_lower:
            if 'fever' in message_lower:
                return {
                    "answer": "See a doctor if: fever is over 103°F, lasts more than 3 days, or you have other concerning symptoms. High fevers with confusion or difficulty breathing need immediate attention.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["My fever is 104F", "It's been a week"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
            elif 'cold' in message_lower or 'cough' in message_lower:
                return {
                    "answer": "See a doctor if: symptoms worsen after 10 days, you have difficulty breathing, high fever, or persistent cough. Most colds improve without medical care.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["My symptoms are getting worse", "I'm having trouble breathing"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
        
        # What to do questions (self-care)
        if any(word in message_lower for word in ['what can i do', 'what should i do', 'how can i', 'remedy', 'what helps', 'treatment']):
            if 'fever' in message_lower:
                return {
                    "answer": "For fever: Rest, drink plenty of fluids, avoid overheating, monitor temperature. Cool compresses may help. Avoid self-medicating without medical advice. See a doctor if fever is very high or lasts long.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["What's a normal temperature?", "Should I see someone?"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
            elif 'cold' in message_lower or 'runny nose' in message_lower:
                return {
                    "answer": "For cold: Rest, stay hydrated, use saline nasal drops, avoid irritants. Most colds improve naturally. Don't self-medicate. See a doctor if symptoms worsen or don't improve in a week.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["When should I see a doctor?", "What about medicine?"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
        
        # Symptoms not improving
        if any(word in message_lower for word in ['not improving', 'getting worse', 'worsening', 'persistent', 'lasting', 'long time']):
            return {
                "answer": "If symptoms aren't improving: see a doctor for proper evaluation. Worsening symptoms especially need medical attention. Don't delay seeking care if you're worried. Always err on the side of caution with health.\n\nConsult a healthcare professional for personalized advice.",
                "follow_up_suggestions": ["What are your symptoms?", "How long?"],
                "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
            }
        
        # Returns None if no predefined response matches
        return None

    def _call_ollama(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None
    ) -> Optional[str]:
        """
        Call Ollama API directly with AGGRESSIVE debug logging.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens in response (optional)
            
        Returns:
            The generated response text or None if error
        """
        # STEP 1: Check availability
        print("\n" + "="*70)
        print("🔍 OLLAMA DEBUG - STEP 1: Checking Ollama availability...")
        print(f"   is_available property: {self.is_available}")
        
        if not self.is_available:
            print("❌ Ollama service NOT available - returning None")
            logger.warning("❌ Ollama service not available")
            return None
        
        try:
            # STEP 2: Build request
            print("🔍 OLLAMA DEBUG - STEP 2: Building request...")
            url = "http://localhost:11434/api/generate"
            print(f"   URL: {url}")
            print(f"   Model: {self.model}")
            
            num_predict = max_tokens or self.num_predict
            if num_predict > 100:
                num_predict = 100
            print(f"   Max tokens: {num_predict}")
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "num_predict": num_predict
            }
            
            print(f"   Prompt length: {len(prompt)} chars")
            print(f"   Prompt preview: {prompt[:80]}...")
            print(f"   Full payload: {json.dumps(payload, indent=2)}")
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # STEP 3: Send request
            print("🔍 OLLAMA DEBUG - STEP 3: Sending POST request...")
            print(f"   URL: {url}")
            print(f"   Timeout: 40 seconds")
            print(f"   Payload size: {len(json.dumps(payload))} bytes")
            
            logger.info(f"🔄 Calling Ollama API at {url}")
            logger.info(f"   Model: {self.model}, Timeout: 40s, Max tokens: {num_predict}")
            
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=40
            )
            
            # STEP 4: Check response status
            print("🔍 OLLAMA DEBUG - STEP 4: Got response!")
            print(f"   Status code: {response.status_code}")
            print(f"   Response length: {len(response.text)} bytes")
            print(f"   Raw response text: {response.text[:300]}")
            
            logger.info(f"📊 Response status: {response.status_code}")
            logger.debug(f"📄 Raw response text ({len(response.text)} chars): {response.text[:200]}...")
            
            # STEP 5: Parse response
            print("🔍 OLLAMA DEBUG - STEP 5: Parsing JSON response...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   JSON parsed successfully!")
                    print(f"   JSON keys: {list(data.keys())}")
                    print(f"   Full JSON: {json.dumps(data, indent=2)}")
                    
                    result = data.get("response", "").strip()
                    print(f"   Response field length: {len(result)} chars")
                    print(f"   Response field: {result[:100]}...")
                    
                    if result:
                        print(f"✅ SUCCESS! Got AI response ({len(result)} chars)")
                        logger.info(f"✅ Got AI response ({len(result)} chars)")
                        logger.debug(f"   Response: {result[:100]}...")
                        print("="*70 + "\n")
                        return result
                    else:
                        print("❌ Response field was EMPTY - returning None")
                        logger.warning("⚠️ Response body was empty")
                        print("="*70 + "\n")
                        return None
                        
                except Exception as json_err:
                    print(f"❌ JSON parse error: {type(json_err).__name__}: {str(json_err)}")
                    print(f"   Raw response was: {response.text}")
                    logger.error(f"❌ Failed to parse JSON: {str(json_err)}")
                    logger.error(f"   Raw response was: {response.text}")
                    print("="*70 + "\n")
                    return None
            else:
                print(f"❌ Response status NOT 200: {response.status_code}")
                print(f"   Response: {response.text}")
                logger.error(f"❌ Ollama returned status {response.status_code}")
                logger.error(f"   Response: {response.text}")
                print("="*70 + "\n")
                return None
                
        except requests.Timeout as e:
            print(f"❌ TIMEOUT ERROR (40s): {str(e)}")
            logger.error(f"❌ TIMEOUT (40s) - Ollama took too long: {str(e)}")
            print("="*70 + "\n")
            return None
            
        except requests.ConnectionError as e:
            print(f"❌ CONNECTION ERROR: {str(e)}")
            print("   Is Ollama running at http://localhost:11434?")
            logger.error(f"❌ CONNECTION ERROR - Cannot reach Ollama at localhost:11434")
            logger.error(f"   Make sure Ollama is running: {str(e)}")
            print("="*70 + "\n")
            return None
            
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            logger.error(f"❌ UNEXPECTED ERROR: {type(e).__name__}: {str(e)}")
            logger.error(f"   Traceback: {traceback.format_exc()}")
            print("="*70 + "\n")
            return None
    
    def safe_call_ollama(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Safe wrapper around _call_ollama that ALWAYS returns a valid string.
        Never raises exceptions - always returns fallback on error.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens in response (optional)
            
        Returns:
            Response text or fallback message (never None)
        """
        try:
            response = self._call_ollama(prompt, max_tokens)
            if response:
                return response
            else:
                logger.warning("⚠️ _call_ollama returned None, using fallback")
                return "I'm having trouble generating a response right now. Please try again."
        except Exception as e:
            logger.error(f"❌ safe_call_ollama error: {type(e).__name__}: {str(e)}")
            return "I encountered an unexpected error. Please try again."


    def generate_explanation(
        self,
        disease: str,
        symptoms: List[str],
        confidence: float
    ) -> Dict:
        """
        Generate AI explanation for disease based on symptoms.
        
        Args:
            disease: Predicted disease name
            symptoms: List of detected symptoms
            confidence: Confidence score (0-100)
            
        Returns:
            Dictionary with explanation and metadata
        """
        symptoms_str = ", ".join(symptoms)
        
        prompt = f"""Based on the following medical symptoms, provide a brief, simple explanation (2-3 sentences):

Symptoms: {symptoms_str}
Preliminary indication: {disease}
Confidence: {confidence:.1f}%

Provide a clear but cautious explanation. Important: Always end with "Consult a healthcare professional for proper diagnosis."

Explanation:"""

        explanation = self._call_ollama(prompt, max_tokens=150)
        
        if explanation is None:
            explanation = f"Based on detected symptoms of {', '.join(symptoms)}, this may indicate {disease}. Please consult a healthcare professional for proper diagnosis and treatment."
        
        return {
            "disease": disease,
            "symptoms": symptoms,
            "confidence": f"{confidence:.1f}%",
            "explanation": explanation,
            "disclaimer": "⚠️ This is informational only. Always consult a qualified healthcare provider."
        }

    def explain_medicine_detection(
        self,
        medicine_name: str,
        detection_result: Dict
    ) -> Dict:
        """
        Generate AI explanation for medicine authenticity detection.
        
        Args:
            medicine_name: Name of the detected medicine
            detection_result: Dictionary with detection results
            
        Returns:
            Dictionary with explanation and safety info
        """
        is_authentic = detection_result.get("is_recognized", False)
        confidence = detection_result.get("confidence", 0)
        packaging_quality = detection_result.get("packaging_quality", "unknown")
        
        status = "authentic" if is_authentic else "potentially counterfeit"
        
        prompt = f"""Analyze this medicine detection result and provide a brief safety explanation:

Medicine: {medicine_name}
Status: {status}
Confidence: {confidence:.1f}%
Packaging Quality: {packaging_quality}

Provide a concise explanation (2-3 sentences) about what this means. Important: Always include "Consult a pharmacist if you have concerns about medicine authenticity."

Explanation:"""

        explanation = self._call_ollama(prompt, max_tokens=150)
        
        if explanation is None:
            status_text = "appears to be authentic" if is_authentic else "could not be verified"
            explanation = f"This medicine {status_text} based on available data. For safety, always consult with a pharmacist or doctor about medicine authenticity."
        
        return {
            "medicine": medicine_name,
            "is_authentic": is_authentic,
            "confidence": f"{confidence:.1f}%",
            "explanation": explanation,
            "safety_note": "🔒 Never use medicines from untrusted sources. Consult a pharmacist if you have concerns."
        }

    def chat_answer(
        self,
        message: str,
        context: Optional[Dict] = None,
        history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Generate responses using AI (Ollama) for ANY question.
        No hardcoded responses - always uses the LLM.
        
        Args:
            message: User's question (any topic)
            context: Optional context about disease/symptoms
            history: Previous messages for context
            
        Returns:
            Dictionary with AI response
        """
        print(f"\n{'*'*70}")
        print(f"💬 CHAT ANSWER - Received message: {message[:60]}...")
        
        message = message.strip()
        if not message:
            print("⚠️ Message is empty")
            return {
                "answer": "Please ask me a question or tell me about your symptoms.",
                "follow_up_suggestions": [],
                "disclaimer": "💬 Ask me anything"
            }
        
        # Check if Ollama is available
        print(f"🔍 Checking if Ollama available...")
        ollama_available = self.is_available
        print(f"   Ollama available: {ollama_available}")
        
        if not ollama_available:
            print("❌ Ollama NOT available")
            logger.warning("❌ Ollama not available in chat_answer")
            return {
                "answer": "AI is offline. Make sure Ollama is running. Consult a healthcare professional for urgent advice.",
                "follow_up_suggestions": [],
                "disclaimer": "⚠️ AI service unavailable"
            }
        
        # Build a generic prompt that handles any question
        print(f"🔍 Building prompt...")
        
        context_str = ""
        if context:
            context_str = f"\nContext: Disease: {context.get('disease', '')}, Symptoms: {', '.join(context.get('symptoms', []))}\n"
            print(f"   Added context: {len(context_str)} chars")
        
        history_str = ""
        if history and len(history) > 0:
            history_str = "Previous messages:\n"
            for msg in history[-3:]:  # Last 3 messages
                q = msg.get('question', msg.get('user_message', ''))
                a = msg.get('answer', '')
                if q and a:
                    history_str += f"User: {q}\nAssistant: {a}\n"
            print(f"   Added history: {len(history_str)} chars")
        
        # Create a simple, flexible prompt that works for ANY question
        prompt = f"""You are a helpful, knowledgeable assistant.

{history_str}{context_str}

User: {message}

Respond naturally and helpfully. If the question is health-related, provide medical information. If it's not health-related (like a joke), respond naturally anyway. Keep response to 2-3 sentences maximum."""
        
        print(f"📝 Final prompt: {len(prompt)} chars")
        print(f"   Prompt preview: {prompt[:100]}...")
        
        try:
            print(f"🔄 Calling _call_ollama()...")
            logger.info(f"💬 Processing user message: {message[:60]}...")
            
            # Always call the AI - no hardcoded checks
            answer = self._call_ollama(prompt, max_tokens=100)
            
            print(f"✅ _call_ollama returned: {type(answer)} (value: {repr(answer)[:50]}...)")
            
            # If AI failed to respond, only then use fallback
            if answer is None:
                print("❌ answer is None - using fallback")
                logger.warning("⚠️ AI returned None, using fallback")
                return {
                    "answer": "AI is not responding right now. Please try again.",
                    "follow_up_suggestions": [],
                    "disclaimer": "⚠️ AI temporarily unavailable"
                }
            
            print(f"✅ Got answer from AI: {len(answer)} chars")
            
            # Clean up the response (remove junk)
            answer = self._cleanup_response(answer)
            print(f"✅ After cleanup: {len(answer)} chars")
            
            # Get follow-up suggestions if response is substantial
            follow_ups = self._get_followup_suggestions(message, context) if len(answer) > 30 else []
            
            result = {
                "answer": answer,
                "follow_up_suggestions": follow_ups,
                "disclaimer": "💬 AI-generated response"
            }
            
            print(f"✅ CHAT SUCCESS - Returning: {result}")
            print(f"{'*'*70}\n")
            
            return result
            
        except Exception as e:
            print(f"❌ CHAT ERROR: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            logger.error(f"❌ Chat error: {type(e).__name__}: {str(e)}")
            print(f"{'*'*70}\n")
            return {
                "answer": "Something went wrong. Please try again.",
                "follow_up_suggestions": [],
                "disclaimer": "⚠️ Error occurred"
            }
    
    
    def _check_non_health_question(self, message_lower: str) -> Optional[Dict]:
        """
        Check if question is off-topic (not health-related).
        Returns response if off-topic; None if health-related.
        
        This prevents timeouts by rejecting non-health questions 
        WITHOUT trying to call the LLM.
        """
        # List of non-health topics to reject quickly
        non_health_keywords = [
            'joke', 'funny', 'tell me', 'make me laugh',
            'weather', 'sports', 'news', 'politics',
            'math', 'calculate', '2+2', 'equation',
            'movie', 'tv show', 'music', 'song', 'artist',
            'cook', 'recipe', 'restaurant',
            'weather', 'forecast', 'temperature outside',
            'time', 'what time', 'date', 'day',
            'game', 'play', 'score',
            'capital', 'country', 'city',
            'hello world', 'coding', 'programming',
            'who are you', 'what is your name'
        ]
        
        # If message contains non-health keywords, reject it
        if any(keyword in message_lower for keyword in non_health_keywords):
            logger.info(f"❌ Non-health question detected: {message_lower[:50]}")
            return {
                "answer": "I'm specifically designed to help with health-related questions and symptoms. For other topics, please ask a general-purpose AI. How can I help with your health today?\n\nConsult a healthcare professional for personalized advice.",
                "follow_up_suggestions": ["I have a fever", "Tell me about my symptoms", "Should I see a doctor?"],
                "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
            }
        
        # If no non-health keywords found, it's probably health-related
        # Return None so it continues to LLM processing
        return None
    
    def _handle_fever_question(self, message: str) -> Dict:
        """Handle fever/temperature with context-aware responses."""
        message_lower = message.lower()
        
        # Extract temperature if provided
        temp_value = self._extract_temperature(message)
        duration = self._extract_duration(message)
        
        logger.info(f"🌡️ Fever handler: temp={temp_value}, duration={duration}")
        
        # Build context-specific response
        if temp_value:
            logger.info(f"✅ Using temperature-based response: {temp_value}°F")
            if temp_value > 103:  # Very high fever
                answer = f"A temperature of {temp_value}°F is quite high and concerning. Seek medical attention soon - this could indicate a serious infection.\n\nConsult a healthcare professional for personalized advice."
            elif temp_value > 101:  # High fever
                answer = f"A {temp_value}°F fever suggests infection. Rest, drink fluids, and monitor closely. If it doesn't improve in 2-3 days or worsens, see a doctor.\n\nConsult a healthcare professional for personalized advice."
            else:  # Mild-moderate fever
                answer = f"A {temp_value}°F temperature is mild to moderate. Rest, hydrate, and rest in a cool place. Monitor it - most fevers resolve on their own.\n\nConsult a healthcare professional for personalized advice."
        elif duration:
            logger.info(f"✅ Using duration-based response: {duration}")
            if 'just' in duration or 'today' in duration or 'morning' in duration or 'night' in duration:
                answer = f"Since your fever just started, observe how it progresses. Rest, drink fluids, and keep track of any other symptoms. See a doctor if it persists beyond 3 days.\n\nConsult a healthcare professional for personalized advice."
            elif 'few days' in duration or 'several days' in duration or 'two' in duration or 'three' in duration or 'day' in duration:
                answer = f"A fever lasting several days needs attention. Monitor your temperature and other symptoms closely. Contact your doctor if symptoms worsen or don't improve soon.\n\nConsult a healthcare professional for personalized advice."
            elif 'week' in duration or 'weeks' in duration or 'month' in duration or 'months' in duration:
                answer = f"A fever lasting this long ({duration}) definitely needs medical evaluation. See your doctor soon for proper assessment and treatment.\n\nConsult a healthcare professional for personalized advice."
            else:
                answer = "A fever can be from infection or inflammation. Track how long it lasts, any other symptoms, and your temperature trend. See a doctor if concerned.\n\nConsult a healthcare professional for personalized advice."
        else:
            logger.info("✅ Using generic fever response")
            # Generic fallback
            answer = "A fever can be due to infection or inflammation. Rest, drink plenty of fluids, and monitor your temperature. If it persists over 3 days or reaches 104°F (40°C), see a doctor.\n\nConsult a healthcare professional for personalized advice."
        
        return {
            "answer": answer,
            "follow_up_suggestions": ["How long have you had it?", "Any other symptoms?", "What's your temperature?"],
            "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
        }
    
    def _handle_doctor_question(self, message: str) -> Dict:
        """Handle doctor/medical visit questions - adapt to context."""
        message_lower = message.lower()
        
        # Extract duration to provide context-specific response
        duration = self._extract_duration(message)
        
        # Detect severity indicators
        if any(kw in message_lower for kw in ['severe', 'emergency', 'can\'t breathe', 'chest pain', 'bleeding', 'unconscious']):
            return {
                "answer": "These sound like emergency symptoms. Seek medical attention immediately or call emergency services.\n\nConsult a healthcare professional for personalized advice.",
                "follow_up_suggestions": ["Call emergency", "Get help now"],
                "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
            }
        
        # Detect duration-based recommendations
        if any(word in message_lower for word in ['week', 'month', 'long time', 'persistent', 'ongoing', 'lasting']):
            if duration:
                return {
                    "answer": f"If symptoms have lasted {duration}, definitely consult a doctor for proper assessment and treatment. This duration warrants professional evaluation.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["Describe your symptoms", "Any other changes?"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
            else:
                return {
                    "answer": "If symptoms have lasted this long, definitely consult a doctor for a proper assessment. They can identify the cause and recommend treatment.\n\nConsult a healthcare professional for personalized advice.",
                    "follow_up_suggestions": ["Describe your symptoms", "How long exactly?"],
                    "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
                }
        
        # Detect worsening
        if any(word in message_lower for word in ['worsening', 'getting worse', 'worse', 'declining']):
            return {
                "answer": "If your symptoms are worsening, it's wise to see a doctor soon rather than waiting. They can address what's getting worse before it progresses further.\n\nConsult a healthcare professional for personalized advice.",
                "follow_up_suggestions": ["Tell me your symptoms", "When did it start getting worse?"],
                "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
            }
        
        # Default cautious response
        return {
            "answer": "If your symptoms are persistent, affecting your daily life, or you're concerned, it's better to consult a doctor. They can properly assess your condition.\n\nConsult a healthcare professional for personalized advice.",
            "follow_up_suggestions": ["Tell me your symptoms", "How long has this been happening?"],
            "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
        }
    
    def _handle_medicine_question(self, message: str) -> Dict:
        """Handle medicine/medication questions - don't recommend specific drugs."""
        return {
            "answer": "Medicine recommendations depend on your specific symptoms and medical history. A doctor or pharmacist can suggest what's appropriate for you. Don't self-medicate.\n\nConsult a healthcare professional for personalized advice.",
            "follow_up_suggestions": ["What are your symptoms?", "Should I see a doctor?"],
            "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
        }
    
    def _extract_temperature(self, message: str) -> Optional[float]:
        """Extract temperature value from message."""
        import re
        
        # Look for patterns like: 101.5, 101, 39.2 degrees, 104F, etc.
        patterns = [
            r'(\d{2,3}(?:\.\d)?)\s*(?:°|degree)?(?:\s*)?(?:f|fahrenheit)?',  # 101.5F or 101F
            r'(\d{2}\.\d)\s*(?:°|degree)?(?:\s*)?(?:c|celsius)?',  # 39.2C
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message.lower(), re.IGNORECASE)
            if matches:
                try:
                    temp = float(matches[0])
                    # If temp is in Celsius range (< 42), likely Celsius - convert to Fahrenheit
                    if temp < 42:
                        temp = (temp * 9/5) + 32
                    return temp
                except ValueError:
                    continue
        
        return None
    
    def _extract_duration(self, message: str) -> Optional[str]:
        """Extract symptom duration from message."""
        message_lower = message.lower()
        
        # Check for duration keywords (in order of specificity)
        # More specific patterns first
        if 'several months' in message_lower or 'months' in message_lower:
            return 'several months'
        if 'month' in message_lower:
            return 'over a month'
        if 'couple weeks' in message_lower or 'two weeks' in message_lower:
            return 'a couple weeks'
        if 'week' in message_lower:
            return 'about a week'
        if 'several days' in message_lower:
            return 'several days'
        if 'few days' in message_lower:
            return 'a few days'
        if 'three days' in message_lower or '3 days' in message_lower:
            return 'three days'
        if 'two days' in message_lower or '2 days' in message_lower:
            return 'two days'
        if 'a day' in message_lower or 'one day' in message_lower:
            return 'one day'
        if 'last night' in message_lower or 'night' in message_lower:
            return 'since last night'
        if 'this morning' in message_lower or 'morning' in message_lower:
            return 'since this morning'
        if 'today' in message_lower:
            return 'today'
        if 'just' in message_lower or 'just started' in message_lower or 'started' in message_lower:
            return 'just started'
        
        return None

        """Handle medicine/medication questions - don't recommend specific drugs."""
        return {
            "answer": "Medicine recommendations depend on your specific symptoms and medical history. A doctor or pharmacist can suggest what's appropriate for you. Don't self-medicate.\n\nConsult a healthcare professional for personalized advice.",
            "follow_up_suggestions": ["What are your symptoms?", "Should I see a doctor?"],
            "disclaimer": "⚠️ Medical Disclaimer: This is for informational purposes only."
        }
    
    def _is_invalid_response(self, response: str) -> bool:
        """Check if response contains invalid medical advice or inaccuracies."""
        response_lower = response.lower()
        
        # Check for wrong medical advice (diagnosis patterns)
        diagnose_patterns = [
            'you have',          # No diagnosis
            'you are sick',
            'you suffer from',
            'you have been diagnosed',
            'indicates that you',
        ]
        
        # Check for medicine prescriptions and recommendations
        medicine_patterns = [
            'i prescribe',       # No prescriptions
            'take this medicine',
            'take ibuprofen',     # Specific drugs
            'take aspirin',
            'take paracetamol',
            'take acetaminophen',
            'take antibiotics',
            'buy this',
            'use this drug',
            ' take ',             # Space before/after to avoid "take care"
            'take pill',         # Any pill recommendation
            ' pill ',
            ' mg ',              # Dosage indication
            'inject',
            'prescription',
            'this medicine will',
        ]
        
        # Check for overconfidence and certainty
        overconfident = [
            ' definitely have',  # No certainty
            'definitely ',       # Statements of certainty
            'must have',
            'is certainly',
            '100%',
            'for sure',
            'proven cause',
            'guaranteed',
        ]
        
        # Random/irrelevant content
        random_patterns = [
            'the capital of',    # Unrelated
            'what is math',
            'calculate',
            ' = ',               # Math equations
        ]
        
        # Check all patterns
        for pattern in diagnose_patterns + medicine_patterns + overconfident + random_patterns:
            if pattern in response_lower:
                logger.warning(f"Invalid response pattern detected: {pattern}")
                return True
        
        # Check if response is too short
        if len(response.strip()) < 15:
            return True
        
        # Check if response is mostly unhelpful
        if response.strip().lower().startswith(('sorry', 'i don\'t know', 'unclear', 'not sure')):
            return True
        
        return False

    def _cleanup_response(self, response: str) -> str:
        """Extract first 2-3 sentences, remove junk and enforce accuracy."""
        if response is None:
            return "I couldn't generate a response. Please try again."
        
        response = response.strip()
        if not response:
            return "I couldn't generate a response. Please try again."
        
        import re
        
        # Split by sentence endings
        sentences = re.split(r'[.!?]+', response)
        
        # Filter sentences: valid length and no junk
        junk_phrases = [
            'Answer:', 'A:', 'Q:', 'Response:', 'ROLE', 'INSTRUCTION',
            'Safely and generally', 'Sure thing', 'Sure,', 'AI Assistant:',
            'assistant:', 'model:', 'system:', 'instruction:', 'prompt:',
            'simply put', 'in simple terms', 'here is', 'the answer is'
        ]
        
        result = []
        for sent in sentences:
            sent = sent.strip()
            
            # Apply filters
            if (len(sent) < 10):  # Too short
                continue
            if any(phrase.lower() in sent.lower() for phrase in junk_phrases):
                continue
            if sent.endswith(':'):  # Headers/labels
                continue
            
            result.append(sent)
            if len(result) >= 3:  # Max 3 sentences
                break
        
        # Join with periods
        if result:
            answer = '. '.join(result) + '.'
        else:
            answer = response[:120].strip() + '.'
        
        # Deduplicate words/phrases to prevent repetition (e.g., "rest, hydrate, and rest")
        # Split into words and remove consecutive duplicates
        words = answer.split()
        deduped = []
        for word in words:
            # Check if word is different from previous word OR if previous word is a conjunction
            if not deduped or word.lower() != deduped[-1].lower() or deduped[-1].lower() in ['and', 'or', 'but', 'the', 'a', 'an']:
                deduped.append(word)
        
        answer = ' '.join(deduped)
        return answer


    def generate_health_advice(
        self,
        disease: str,
        symptoms: List[str],
        risk_level: str
    ) -> Dict:
        """
        Generate personalized health advice for a condition.
        
        Args:
            disease: Disease name
            symptoms: Associated symptoms
            risk_level: Risk level (Low, Medium, High)
            
        Returns:
            Dictionary with advice and recommendations
        """
        symptoms_str = ", ".join(symptoms)
        
        prompt = f"""Provide helpful, general health advice for someone with the following:

Condition: {disease}
Symptoms: {symptoms_str}
Risk Level: {risk_level}

Provide 3-4 general recommendations (not medical advice). Format as a numbered list.
Important: End with "Seek immediate medical attention if symptoms worsen or don't improve in a few days."

Advice:"""

        advice = self._call_ollama(prompt, max_tokens=200)
        
        return {
            "disease": disease,
            "risk_level": risk_level,
            "advice": advice,
            "disclaimer": "⚠️ This is general information. Consult a healthcare provider for personalized advice."
        }

    def extract_symptoms_from_text(
        self,
        user_input: str,
        symptom_database: List[str]
    ) -> Dict:
        """
        Extract symptoms from user's free-form text using NLP.
        
        Args:
            user_input: User's description of symptoms
            symptom_database: List of recognized symptoms
            
        Returns:
            Dictionary with extracted symptoms and confidence
        """
        db_str = ", ".join(symptom_database[:20])  # Use first 20 common symptoms
        
        prompt = f"""Extract health symptoms from this text. Only mention symptoms from the provided list.

Text: "{user_input}"

Available symptoms: {db_str}

Return ONLY a JSON object like: {{"symptoms": ["symptom1", "symptom2"], "confidence": 0.85}}

JSON:"""

        response = self._call_ollama(prompt, max_tokens=100)
        
        try:
            # Try to parse JSON response
            result = json.loads(response)
            return {
                "extracted_symptoms": result.get("symptoms", []),
                "confidence": result.get("confidence", 0.5)
            }
        except json.JSONDecodeError:
            logger.warning("Could not parse LLM response as JSON")
            return {
                "extracted_symptoms": [],
                "confidence": 0.3,
                "note": "Could not parse response"
            }

    def get_system_status(self) -> Dict:
        """
        Get the status of the Ollama service.
        
        Returns:
            Dictionary with service status information
        """
        status = {
            "status": "online" if self.is_available else "offline",
            "api_url": self.api_url,
            "model": self.model,
            "mode": "Local (Llama 3)" if self.is_available else "Offline",
            "message": self._get_status_message()
        }
        return status

    @staticmethod
    def _get_followup_suggestions(message: str, context: Optional[Dict]) -> List[str]:
        """Generate relevant follow-up suggestions."""
        suggestions = [
            "Should I see a doctor?",
            "What can I do to feel better?",
            "When should I seek medical attention?",
            "Are there any home remedies?",
            "How long will recovery take?"
        ]
        return suggestions[:3]

    @staticmethod
    def _get_status_message() -> str:
        """Get status message for current state."""
        return "✅ Ollama is running locally with gemma:2b - secure, accurate, offline health guidance"

    @staticmethod
    def _get_offline_message() -> str:
        """Get message when Ollama is not running."""
        return (
            "I'm offline right now. Make sure Ollama is running: ollama serve\n"
            "In the meantime, please consult a healthcare professional for your health concerns."
        )

    @staticmethod
    def _get_error_message() -> str:
        """Get generic error message."""
        return "Please try again or consult a healthcare professional for personalized advice."


# Global singleton instance
_ollama_service = None


def get_ollama_service() -> OllamaService:
    """Get or create the Ollama service singleton."""
    global _ollama_service
    if _ollama_service is None:
        _ollama_service = OllamaService()
    return _ollama_service
