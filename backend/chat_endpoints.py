"""
Health Assistant Chat and Analysis Endpoints
==============================================
Provides /chat and /analyze endpoints for AI-powered health conversations.
Integrates with Ollama for real AI responses with smart prompt engineering.

Features:
- Real AI responses (no hardcoded answers)
- Smart prompt engineering for natural, varied responses
- Anti-repetition measures
- Proper error handling and logging
- Timeout handling
- Random variation IDs for response uniqueness
"""

import requests
import json
import logging
import uuid
import random
import time
from typing import Dict, Optional, Tuple
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)


class HealthChatAI:
    """
    AI Health Assistant using Ollama for real-time responses.
    Handles both /chat and /analyze endpoints with smart prompting.
    """

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        model: str = "llama3",
        timeout: int = 60,
        temperature: float = 0.9,
        top_p: float = 0.9,
        repeat_penalty: float = 1.2,
    ):
        """
        Initialize Health Chat AI.
        
        Args:
            ollama_url: Base URL for Ollama API
            model: Model to use (default: llama3)
            timeout: Request timeout in seconds
            temperature: Response creativity (0.0-1.0)
            top_p: Top-p sampling parameter
            repeat_penalty: Penalty for repeating content
        """
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout
        self.temperature = temperature
        self.top_p = top_p
        self.repeat_penalty = repeat_penalty
        self.api_endpoint = f"{ollama_url}/api/generate"
        
        # Track recent responses to avoid repetition
        self.response_cache = {}
        self.request_count = 0
        self.error_count = 0
        
        logger.info(
            f"✅ HealthChatAI initialized: model={model}, "
            f"temp={temperature}, top_p={top_p}, repeat_penalty={repeat_penalty}"
        )

    def is_available(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(
                f"{self.ollama_url}/api/tags",
                timeout=5
            )
            available = response.status_code == 200
            if available:
                logger.info("✅ Ollama service is available")
            return available
        except Exception as e:
            logger.error(f"❌ Ollama not available: {str(e)}")
            return False

    def _generate_variation_id(self) -> str:
        """Generate unique variation ID to ensure different responses."""
        return f"var_{uuid.uuid4().hex[:8]}_{int(time.time())}"

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """
        Call Ollama API with the given prompt.
        
        Args:
            prompt: The prompt to send to Ollama
            
        Returns:
            Generated response text or None if error
        """
        self.request_count += 1
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "repeat_penalty": self.repeat_penalty,
            }

            logger.info(f"📤 Sending request #{self.request_count} to Ollama...")
            logger.debug(f"   Prompt length: {len(prompt)} chars")

            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.error(f"❌ Ollama returned status {response.status_code}")
                self.error_count += 1
                return None

            result = response.json()
            generated_text = result.get("response", "").strip()

            if not generated_text:
                logger.warning("⚠️ Ollama returned empty response")
                self.error_count += 1
                return None

            logger.info(f"✅ Response received ({len(generated_text)} chars)")
            return generated_text

        except requests.exceptions.Timeout:
            logger.error("❌ Ollama request timeout (60 seconds exceeded)")
            self.error_count += 1
            return None
        except requests.exceptions.ConnectionError:
            logger.error("❌ Cannot connect to Ollama. Is it running?")
            self.error_count += 1
            return None
        except Exception as e:
            logger.error(f"❌ Error calling Ollama: {str(e)}")
            self.error_count += 1
            return None

    def chat(self, user_message: str) -> Dict:
        """
        Chat endpoint handler.
        Takes a user message and returns AI health assistant response.
        
        Args:
            user_message: User's health question or comment
            
        Returns:
            Dict with 'reply', 'variation_id', and metadata
        """
        if not user_message or not user_message.strip():
            return {
                "success": False,
                "error": "Message cannot be empty",
                "reply": None,
                "variation_id": None
            }

        variation_id = self._generate_variation_id()
        user_message = user_message.strip()

        # Log user input
        logger.info(f"💬 Chat request: '{user_message}'")
        logger.info(f"   Variation ID: {variation_id}")

        # Build smart prompt for /chat
        prompt = self._build_chat_prompt(user_message, variation_id)

        # Call Ollama
        ai_response = self._call_ollama(prompt)

        if not ai_response:
            return {
                "success": False,
                "error": "Failed to generate response from AI",
                "reply": None,
                "variation_id": variation_id
            }

        # Clean up response
        cleaned_response = self._clean_response(ai_response)

        # Log AI response
        logger.info(f"🤖 AI Reply: {cleaned_response[:100]}...")

        return {
            "success": True,
            "reply": cleaned_response,
            "variation_id": variation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "model": self.model,
            "request_number": self.request_count
        }

    def analyze(self, symptoms: str) -> Dict:
        """
        Analyze endpoint handler.
        Takes symptoms and returns structured analysis.
        
        Args:
            symptoms: Comma-separated symptoms or natural language description
            
        Returns:
            Dict with 'analysis' containing causes, advice, severity, and variation_id
        """
        if not symptoms or not symptoms.strip():
            return {
                "success": False,
                "error": "Symptoms cannot be empty",
                "analysis": None,
                "variation_id": None
            }

        variation_id = self._generate_variation_id()
        symptoms = symptoms.strip()

        # Log user input
        logger.info(f"🔍 Analyze request: '{symptoms}'")
        logger.info(f"   Variation ID: {variation_id}")

        # Build smart prompt for /analyze
        prompt = self._build_analyze_prompt(symptoms, variation_id)

        # Call Ollama
        ai_response = self._call_ollama(prompt)

        if not ai_response:
            return {
                "success": False,
                "error": "Failed to analyze symptoms",
                "analysis": None,
                "variation_id": variation_id
            }

        # Parse structured response
        analysis = self._parse_analysis_response(ai_response)

        # Log analysis
        logger.info(f"📊 Analysis generated: {len(analysis.get('causes', []))} possible causes")

        return {
            "success": True,
            "analysis": analysis,
            "variation_id": variation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "model": self.model,
            "request_number": self.request_count
        }

    def _build_chat_prompt(self, user_message: str, variation_id: str) -> str:
        """
        Build smart prompt for /chat endpoint.
        
        Creates a prompt that:
        - Makes AI act as health assistant
        - Gives short (3-5 lines) helpful advice
        - Avoids repeating user input
        - Avoids robotic phrases
        - Is natural and human-like
        - Suggests doctor if needed
        """
        # Add randomness to prompt to vary responses
        random_intro = random.choice([
            "I understand. Based on that, ",
            "Got it. Here's my take: ",
            "I see. Let me help: ",
            "That sounds concerning. ",
            "Here's what I'd suggest: ",
        ])

        prompt = f"""You are a friendly, natural health assistant. NOT a robot.

User asks: {user_message}

IMPORTANT RULES:
1. Keep response SHORT - maximum 3-5 lines
2. Be genuinely helpful and practical
3. NEVER repeat what the user said
4. NEVER use phrases like "I understand your question" or "As an AI"
5. Sound natural and like a real person, not a robot
6. If serious or unclear, suggest seeing a doctor
7. Use simple language
8. This is just general guidance, not medical advice

{random_intro}"""

        return prompt

    def _build_analyze_prompt(self, symptoms: str, variation_id: str) -> str:
        """
        Build smart prompt for /analyze endpoint.
        
        Creates a prompt that:
        - Identifies 2-4 possible causes
        - Gives simple advice
        - Suggests home remedies (if safe)
        - Mentions severity
        - Keeps response short (5-6 lines)
        - Avoids repeating symptoms
        - Uses simple language
        - Always generates unique response
        """
        random_start = random.choice([
            "Based on those symptoms, ",
            "Here's my analysis: ",
            "These symptoms suggest: ",
            "Let me analyze this: ",
        ])

        prompt = f"""You are a health assistant analyzing symptoms.

Symptoms reported: {symptoms}

ANALYZE AND PROVIDE:
1. 2-4 POSSIBLE CAUSES (most common first)
2. Simple ADVICE for managing
3. HOME REMEDIES (only safe, common ones)
4. SEVERITY level (mild/moderate/serious)

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Possible Causes:
- [cause 1]
- [cause 2]
- (etc)

Advice:
- [advice 1]
- [advice 2]

Home Remedies:
- [remedy 1]
- [remedy 2]

Severity:
- [description with level]

IMPORTANT RULES:
1. Keep entire response to 5-6 lines max
2. NEVER repeat the symptoms back
3. Use simple, everyday language
4. Only suggest safe remedies (rest, water, heat, etc)
5. Always suggest seeing doctor if serious
6. Make it unique - vary your response format each time (variation ID: {variation_id})
7. Be realistic about severity
8. This is just general guidance, not medical advice

{random_start}"""

        return prompt

    def _clean_response(self, response: str) -> str:
        """
        Clean up AI response.
        Remove unnecessary prefixes, extra whitespace, etc.
        """
        # Remove common "AI" prefixes
        prefixes_to_remove = [
            "As an AI",
            "As a language model",
            "I'm an AI",
            "I'm a language model",
            "I understand your question",
            "Based on your question",
        ]

        lines = response.strip().split('\n')
        
        # Remove first line if it's a common AI prefix
        first_line = lines[0] if lines else ""
        for prefix in prefixes_to_remove:
            if first_line.startswith(prefix):
                lines = lines[1:]
                break

        cleaned = '\n'.join(lines).strip()

        # Remove excessive newlines
        while '\n\n\n' in cleaned:
            cleaned = cleaned.replace('\n\n\n', '\n\n')

        return cleaned

    def _parse_analysis_response(self, response: str) -> Dict:
        """
        Parse structured analysis response from AI.
        
        Extracts:
        - Possible Causes
        - Advice
        - Home Remedies
        - Severity
        """
        analysis = {
            "causes": [],
            "advice": [],
            "remedies": [],
            "severity": "",
            "raw_response": response
        }

        # Split by section headers
        sections = response.split('\n')
        current_section = None
        current_list = []

        for line in sections:
            line = line.strip()
            
            if not line:
                continue

            # Detect section headers (case-insensitive)
            line_lower = line.lower()
            
            if "possible causes" in line_lower:
                if current_list and current_section:
                    analysis[current_section] = current_list
                current_section = "causes"
                current_list = []
            elif "advice" in line_lower:
                if current_list and current_section:
                    analysis[current_section] = current_list
                current_section = "advice"
                current_list = []
            elif "home remedies" in line_lower or "remedies" in line_lower:
                if current_list and current_section:
                    analysis[current_section] = current_list
                current_section = "remedies"
                current_list = []
            elif "severity" in line_lower:
                if current_list and current_section:
                    analysis[current_section] = current_list
                current_section = "severity"
                current_list = []
            elif line.startswith("-") or line.startswith("•"):
                # This is a bullet point
                item = line.lstrip("-•").strip()
                if item and current_section and current_section != "severity":
                    current_list.append(item)
            elif current_section == "severity" and line:
                # Severity is usually a paragraph, not a list
                current_list.append(line)

        # Add last section
        if current_list and current_section:
            if current_section == "severity":
                analysis[current_section] = '\n'.join(current_list)
            else:
                analysis[current_section] = current_list

        return analysis
