from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import base64
import os
import random
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# =========================
# AI Symptom Analyzer API (Enhanced)
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Enhanced symptom analyzer with:
    - High temperature (0.95) for unique analysis
    - Top-p sampling for quality variety
    - Repeat penalty to avoid repetition
    - Structured output format
    """
    try:
        data = request.get_json()
        symptoms = data.get("symptoms", "").strip()

        if not symptoms:
            return jsonify({"result": "Please enter your symptoms."})

        # Track previous analyses for this symptom set
        symptom_hash = hashlib.md5(symptoms.encode()).hexdigest()
        previous_analyses = chat_memory['questions'].get(symptom_hash, [])
        
        # Build variation instruction
        variation_text = ""
        if previous_analyses:
            variation_text = f"\n⚠️ This symptom set was analyzed {len(previous_analyses)} time(s) before.\nProvide a DIFFERENT analysis this time with new perspectives."

        prompt = f"""You are a professional AI Health Assistant.

Patient symptoms: {symptoms}
{variation_text}

Provide response in this EXACT format:

Possible Conditions:
- condition 1
- condition 2
- condition 3

What To Do:
- step 1
- step 2
- step 3

Home Remedies:
- remedy 1
- remedy 2

When To See Doctor:
- warning sign 1
- warning sign 2

IMPORTANT RULES:
- Keep it concise (6-8 lines max)
- Use simple, clear English
- Be safe and helpful
- Do NOT give dangerous advice
- Be unique in your recommendations
- Vary your analysis approach each time

Make this analysis UNIQUE and DIFFERENT."""

        # Call Ollama with ENHANCED PARAMETERS
        print(f"\n🔄 Analyzing symptoms with enhanced parameters...")
        print(f"   Temperature: 0.95 | Top-P: 0.95 | Repeat Penalty: 1.3")
        
        response = ollama.chat(
            model="gemma:2b",
            messages=[
                {"role": "system", "content": "You are an expert health analyst. Provide unique, practical medical insights."},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0.95,      # High for variety
                "top_p": 0.95,            # Nucleus sampling
                "repeat_penalty": 1.3     # Avoid repetition
            }
        )

        output = response["message"]["content"]
        
        # Store analysis
        if symptom_hash not in chat_memory['questions']:
            chat_memory['questions'][symptom_hash] = []
        
        chat_memory['questions'][symptom_hash].append({
            "response": output[:150],
            "timestamp": datetime.now().isoformat()
        })

        return jsonify({
            "result": output,
            "status": "success",
            "variations": len(previous_analyses)
        })

    except Exception as e:
        print(f"❌ ANALYZE ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "result": str(e),
            "status": "error"
        }), 500


# =========================
# Medicine Image Analysis API
# =========================
@app.route("/analyze-medicine-image", methods=["POST"])
def analyze_medicine_image():
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({"valid": False, "message": "Please provide a valid medicine image"}), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({"valid": False, "message": "Please provide a valid medicine image"}), 400
        
        # Read image file and convert to base64
        image_data = image_file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        print(f"Processing image: {image_file.filename}")

        try:
            # Step 1: Classify - Is this a medicine/pharmaceutical product?
            classification_prompt = """You are a pharmaceutical identification assistant. Look at this image carefully.

Is this image showing a MEDICINE, DRUG, PHARMACEUTICAL PRODUCT, TABLET, PILL, CAPSULE, INJECTION, MEDICAL SUPPLEMENT, HEALTHCARE PRODUCT, or MEDICINE PACKAGING?

Answer ONLY: YES or NO

Be very strict. Only answer YES if it's clearly a medicine or healthcare product."""
            
            print("Classifying image...")
            classification_response = ollama.chat(
                model="llava:7b",
                messages=[{
                    "role": "user",
                    "content": classification_prompt,
                    "images": [image_base64]
                }],
                options={"temperature": 0.1},
                stream=False
            )
            
            classification_result = classification_response["message"]["content"].strip().upper()
            print(f"Classification result: {classification_result}")
            
            # If not medicine, return error
            if "NO" in classification_result or classification_result.startswith("NO"):
                return jsonify({
                    "valid": False,
                    "message": "Please provide a valid medicine"
                })
            
            # Step 2: Detailed Analysis - Extract medicine information
            analysis_prompt = """You are an expert pharmacist AI. Analyze this medicine image CAREFULLY and provide DETAILED information.

Provide the following information in this exact format:

**Medicine Name/Type:** [What medicine or type of medicine is this?]

**Active Ingredient(s):** [What are the main active ingredients? Look at the packaging/label]

**Uses:** [What is this medicine used for?]

**Dosage:** [What is the recommended dose? Check the packaging]

**Side Effects:** [What are common side effects?]

**Precautions:** [Important warnings or precautions]

**Contraindications:** [Who should NOT take this?]

Be precise and extract information from the image. If you can read the label, provide exact details."""
            
            print("Analyzing medicine details...")
            analysis_response = ollama.chat(
                model="llava",
                messages=[{
                    "role": "user",
                    "content": analysis_prompt,
                    "images": [image_base64]
                }],
                options={"temperature": 0.3},
                stream=False
            )
            
            result_text = analysis_response["message"]["content"]
            print(f"Analysis complete")
            
            return jsonify({
                "valid": True,
                "result": result_text
            })
            
        except Exception as vision_error:
            print(f"Vision model error: {vision_error}")
            import traceback
            traceback.print_exc()
            
            # Return error message with setup instructions
            return jsonify({
                "valid": False,
                "message": "Medicine analyzer requires Ollama vision model. Run: ollama pull llava"
            }), 500
        
    except Exception as e:
        print(f"Error in medicine image endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "valid": False,
            "message": "Please provide a valid medicine"
        }), 400


# =========================
# Health Check API
# =========================

# =========================
# AI Chat API with Memory
# =========================
# Store conversation history to avoid repetition
chat_memory = {
    'questions': {},  # Store to prevent repetition with timestamps
    'conversation_history': [],  # For context
    'response_styles': {},  # Track which response style was used
    'timestamps': {}  # Track when questions were asked
}

# Response style variations for Anti-repetition
RESPONSE_STYLES = [
    "detailed_analysis",
    "quick_summary",
    "step_by_step",
    "comparison_approach",
    "risk_benefit",
    "practical_guide"
]

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    try:
        # Try to connect to Ollama to verify it's working
        ollama.list()
        return jsonify({
            "status": "operational",
            "message": "AI Health Assistant API is working"
        })
    except Exception as e:
        print(f"Health check failed: {e}")
        return jsonify({
            "status": "unavailable",
            "message": "AI service is not responding"
        }), 503

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Enhanced chat endpoint with:
    - High temperature settings for unique responses (0.95)
    - Advanced sampling parameters (top_p, repeat_penalty)
    - Anti-repetition with response style variation
    - Optimal solution generation
    - UUID-based response uniqueness
    """
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        analysis_context = data.get("context", {})

        if not user_message:
            return jsonify({"message": "Please enter a message."})

        # Store in conversation history for context
        chat_memory['conversation_history'].append({
            "role": "user",
            "content": user_message
        })

        # Keep only last 10 messages for context
        if len(chat_memory['conversation_history']) > 10:
            chat_memory['conversation_history'] = chat_memory['conversation_history'][-10:]

        # ============= ANTI-REPETITION LOGIC =============
        message_hash = hashlib.md5(user_message.encode()).hexdigest()
        previous_responses = chat_memory['questions'].get(message_hash, [])
        used_styles = chat_memory['response_styles'].get(message_hash, [])
        
        # Select a different response style than before
        available_styles = [s for s in RESPONSE_STYLES if s not in used_styles]
        if not available_styles:
            # Reset if all styles used
            available_styles = RESPONSE_STYLES
            used_styles = []
        
        current_style = random.choice(available_styles)
        used_styles.append(current_style)
        chat_memory['response_styles'][message_hash] = used_styles[-3:]  # Keep last 3
        
        # Build dynamic prompt based on response style
        style_prompts = {
            "detailed_analysis": """Provide an in-depth, comprehensive analysis with multiple perspectives.
Include detailed reasoning for each recommendation.""",
            
            "quick_summary": """Provide a concise, bullet-point answer.
Focus on the most critical information only.""",
            
            "step_by_step": """Provide a clear step-by-step action plan.
Number each step and explain what to do and why.""",
            
            "comparison_approach": """Compare different approaches or options.
Explain pros and cons of each.""",
            
            "risk_benefit": """Analyze risks and benefits.
Highlight potential outcomes of different actions.""",
            
            "practical_guide": """Provide a practical, real-world applicable guide.
Focus on what someone can actually do immediately."""
        }

        variation_instruction = ""
        if previous_responses:
            variation_instruction = f"""⚠️ CRITICAL - This question has been asked {len(previous_responses)} time(s) before.
You MUST give a COMPLETELY DIFFERENT answer this time.
Use a different structure and explanation approach.
"""
            # Add suggestion from previous responses
            if len(previous_responses) > 1:
                variation_instruction += f"Have already discussed: basics. Now go deeper/alternative.\n"

        # Build the main prompt with multi-line randomization
        random_openings = [
            "Here's what I think:",
            "Let me break this down:",
            "Based on the health principles:",
            "Here's my analysis:",
            "From a practical standpoint:",
        ]

        prompt = f"""You are an expert AI Health Assistant. Generate UNIQUE and OPTIMAL health solutions.

User Question: {user_message}

{variation_instruction}

RESPONSE STYLE: {current_style.upper()}
{style_prompts[current_style]}

MANDATORY RULES:
1. ALWAYS be unique - never repeat previous explanations
2. Provide optimal, evidence-based or best-practice advice
3. Be specific and actionable
4. Use clear, simple language
5. Include why the solution works
6. Mention when to seek professional help
7. Avoid generic AI phrases like "I understand" or "As an AI"

{random.choice(random_openings)}
"""

        # Add context if available
        if analysis_context:
            prompt += f"\nContext: {analysis_context}\n"

        # ============= ENHANCED LLM PARAMETERS =============
        # Build messages with system prompt
        messages_with_context = [
            {"role": "system", "content": """You are a world-class health expert AI assistant.
Your job:
1. Provide unique, creative, optimal solutions
2. Never repeat the same answer twice
3. Vary your response structure and examples
4. Be practical and specific
5. Always maintain medical safety

Key: Create DIFFERENT responses even for identical questions."""},
            *chat_memory['conversation_history'][-4:]
        ]

        # Call Ollama with ENHANCED PARAMETERS for more variation
        print(f"\n🔄 Calling Ollama with enhanced parameters...")
        print(f"   Temperature: 0.95 (HIGH - more variation)")
        print(f"   Top-P: 0.95 (nucleus sampling)")
        print(f"   Repeat Penalty: 1.3 (prevents repetition)")
        print(f"   Response Style: {current_style}")
        
        response = ollama.chat(
            model="llama3",
            messages=messages_with_context,
            stream=False,
            options={
                "temperature": 0.95,  # Higher = more varied/creative responses
                "top_p": 0.95,  # Nucleus sampling - better quality variety
                "repeat_penalty": 1.3  # Penalize repetitive text
            }
        )

        bot_response = response["message"]["content"]

        # ============= STORE RESPONSE METADATA =============
        # Store this answer with metadata
        if message_hash not in chat_memory['questions']:
            chat_memory['questions'][message_hash] = []
        
        chat_memory['questions'][message_hash].append({
            "response": bot_response[:150],  # Store more context
            "style": current_style,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 5 responses per question to save memory
        if len(chat_memory['questions'][message_hash]) > 5:
            chat_memory['questions'][message_hash] = chat_memory['questions'][message_hash][-5:]

        # Add bot response to history
        chat_memory['conversation_history'].append({
            "role": "assistant",
            "content": bot_response
        })

        return jsonify({
            "message": bot_response,
            "ai_response": {
                "answer": bot_response,
                "style": current_style,
                "variations_count": len(previous_responses)
            },
            "status": "success"
        })

    except Exception as e:
        print(f"❌ CHAT ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "message": "Sorry, I'm having trouble right now. Please try again.",
            "error": str(e),
            "status": "error"
        }), 500

@app.route("/api/chat/clear", methods=["POST"])
def clear_chat():
    """Clear chat history and memory"""
    global chat_memory
    chat_memory = {
        'questions': {},
        'conversation_history': [],
        'response_styles': {},
        'timestamps': {}
    }
    return jsonify({"message": "Chat history cleared", "status": "success"})

@app.route("/api/chat/stats", methods=["GET"])
def chat_stats():
    """Get chat statistics and variation info"""
    total_questions = len(chat_memory['questions'])
    total_responses = sum(len(v) if isinstance(v, list) else 1 for v in chat_memory['questions'].values())
    
    return jsonify({
        "total_unique_questions": total_questions,
        "total_responses_generated": total_responses,
        "avg_responses_per_question": total_responses / max(total_questions, 1),
        "response_styles_used": len(RESPONSE_STYLES),
        "status": "operational"
    })


# =========================
# Run Server
# =========================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)