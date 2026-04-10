"""
Ollama Chat Service for Health Assistant
Handles direct communication with Ollama API for health-related conversations.
"""

import requests
import json
import logging
import time
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OllamaChatService:
    """
    Service for health-related chat using Ollama (Llama3 model).
    Handles prompt engineering, API calls, error handling, and logging.
    """

    def __init__(
        self,
        api_url: str = "http://localhost:11434",
        model: str = "llama3",
        timeout: int = 30,
        temperature: float = 0.9,
        top_p: float = 0.9,
        repeat_penalty: float = 1.2,
    ):
        """
        Initialize Ollama Chat Service.
        
        Args:
            api_url: Base URL for Ollama API (default: http://localhost:11434)
            model: Model to use (default: llama3)
            timeout: Timeout for API requests in seconds (default: 30)
            temperature: Temperature for response generation (0.0-1.0) (default: 0.9)
            top_p: Top-p sampling parameter (0.0-1.0) (default: 0.9)
            repeat_penalty: Penalty for repetitive content (default: 1.2)
        """
        self.api_url = api_url
        self.model = model
        self.timeout = timeout
        self.temperature = temperature
        self.top_p = top_p
        self.repeat_penalty = repeat_penalty
        self.endpoint = f"{api_url}/api/generate"
        self.last_response = None
        self.request_count = 0
        self.error_count = 0
        
        logger.info(
            f"🏥 Health Chat Service initialized: {model} model, "
            f"temp={temperature}, top_p={top_p}, repeat_penalty={repeat_penalty}"
        )

    def is_available(self) -> bool:
        """
        Check if Ollama service is running and accessible.
        
        Returns:
            bool: True if Ollama API is reachable, False otherwise
        """
        try:
            response = requests.get(
                f"{self.api_url}/api/tags",
                timeout=5
            )
            is_ok = response.status_code == 200
            if is_ok:
                logger.info("✅ Ollama service is available")
            else:
                logger.warning(f"⚠️ Ollama returned status {response.status_code}")
            return is_ok
        except requests.exceptions.ConnectionError:
            logger.warning(
                f"❌ Cannot connect to Ollama at {self.api_url}. "
                f"Make sure Ollama is running: ollama serve"
            )
            return False
        except requests.exceptions.Timeout:
            logger.warning("❌ Ollama connection timeout")
            return False
        except Exception as e:
            logger.warning(f"❌ Error checking Ollama availability: {str(e)}")
            return False

    def _build_health_prompt(self, user_message: str) -> str:
        """
        Build a strong system prompt for health assistant behavior.
        
        Args:
            user_message: User's health-related question
            
        Returns:
            str: Formatted prompt for Ollama
        """
        system_prompt = """You are a smart, helpful health assistant. Your role is to:
1. Provide SHORT, PRACTICAL health advice (3-5 lines only)
2. Never repeat the user's question back to them
3. Suggest possible causes and simple home remedies when appropriate
4. Recommend seeing a doctor if the condition seems serious
5. Use natural, conversational language - avoid robotic phrases like "I understand your question"
6. Generate unique responses every time - never give generic answers
7. Be empathetic and supportive

IMPORTANT RULES:
- Keep responses concise and actionable
- Include warning signs that require immediate medical attention
- Always encourage professional medical advice for serious conditions
- Do not pretend to diagnose - only suggest possibilities
- Be practical: give real remedies, not just saying "see a doctor"
- Never use phrases like "I understand your question", "as mentioned", "let me explain"
- Each response must be unique and personalized to their specific concern

User's health question:"""
        
        return f"{system_prompt}\n{user_message}"

    def chat(self, message: str) -> Dict[str, str]:
        """
        Send a health-related message to Ollama and get a response.
        
        Args:
            message: User's health question or message
            
        Returns:
            dict: Response data with 'reply' key containing the AI response
            
        Raises:
            requests.exceptions.Timeout: If API request times out
            requests.exceptions.ConnectionError: If cannot connect to Ollama
            Exception: For other API errors
        """
        if not message or not message.strip():
            logger.warning("⚠️ Empty message received")
            return {
                "reply": "Please ask me a health-related question. I'm here to help!",
                "status": "error",
                "error": "empty_message"
            }

        self.request_count += 1
        user_msg = message.strip()
        
        # Log request
        logger.info(f"🔄 [Request #{self.request_count}] User: {user_msg[:60]}...")
        
        try:
            # Build prompt
            full_prompt = self._build_health_prompt(user_msg)
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,  # Important: don't stream, get complete response
                "temperature": self.temperature,
                "top_p": self.top_p,
                "repeat_penalty": self.repeat_penalty,
            }
            
            # Make API request
            start_time = time.time()
            logger.debug(f"📤 Sending request to {self.endpoint}")
            
            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            elapsed_time = time.time() - start_time
            
            # Check response status
            if response.status_code != 200:
                logger.error(
                    f"❌ Ollama API error: {response.status_code} - {response.text[:200]}"
                )
                self.error_count += 1
                return {
                    "reply": "I'm experiencing technical issues. Please try again in a moment.",
                    "status": "error",
                    "error": f"ollama_error_{response.status_code}"
                }
            
            # Parse response
            response_data = response.json()
            ai_reply = response_data.get("response", "").strip()
            
            if not ai_reply:
                logger.warning("⚠️ Empty response from Ollama")
                self.error_count += 1
                return {
                    "reply": "I couldn't generate a response. Please try again.",
                    "status": "error",
                    "error": "empty_response"
                }
            
            # Log success
            logger.info(
                f"✅ [Request #{self.request_count}] Response received in {elapsed_time:.2f}s "
                f"({len(ai_reply)} chars)"
            )
            logger.debug(f"💬 AI Reply: {ai_reply[:100]}...")
            
            # Store last response
            self.last_response = {
                "timestamp": datetime.now().isoformat(),
                "user_message": user_msg,
                "ai_reply": ai_reply,
                "response_time": elapsed_time,
                "model": self.model,
                "tokens_generated": response_data.get("eval_count", 0)
            }
            
            return {
                "reply": ai_reply,
                "status": "success",
                "response_time": elapsed_time
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Request timeout after {self.timeout}s")
            self.error_count += 1
            return {
                "reply": "The AI is taking too long to respond. Please try again.",
                "status": "error",
                "error": "timeout"
            }
            
        except requests.exceptions.ConnectionError:
            logger.error(
                f"🔌 Connection failed. Is Ollama running? "
                f"Start it with: ollama serve"
            )
            self.error_count += 1
            return {
                "reply": (
                    "I can't connect to the AI service right now. "
                    "Please make sure Ollama is running: ollama serve"
                ),
                "status": "error",
                "error": "connection_failed"
            }
            
        except json.JSONDecodeError:
            logger.error("❌ Invalid JSON response from Ollama")
            self.error_count += 1
            return {
                "reply": "I received an invalid response from the AI. Please try again.",
                "status": "error",
                "error": "invalid_response"
            }
            
        except Exception as e:
            logger.error(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
            self.error_count += 1
            return {
                "reply": "An unexpected error occurred. Please try again.",
                "status": "error",
                "error": str(e)
            }

    def get_stats(self) -> Dict:
        """
        Get service statistics.
        
        Returns:
            dict: Statistics including request count, error count, etc.
        """
        success_count = self.request_count - self.error_count
        success_rate = (
            (success_count / self.request_count * 100)
            if self.request_count > 0
            else 0
        )
        
        return {
            "total_requests": self.request_count,
            "successful_requests": success_count,
            "error_count": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "model": self.model,
            "last_response": self.last_response
        }

    def reset_stats(self):
        """Reset service statistics."""
        self.request_count = 0
        self.error_count = 0
        self.last_response = None
        logger.info("📊 Service statistics reset")
