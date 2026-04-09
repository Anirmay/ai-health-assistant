from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import numpy as np
from ml_models.symptom_disease_model import predict_disease_from_symptoms, get_symptom_suggestions, validate_symptoms_support
from ml_models.symptom_mapper import map_user_symptoms, get_symptom_mapping_summary
from ml_models.medicine_detector import verify_medicine
from ml_models.medicine_detector_enhanced import verify_medicine_enhanced
from ai_module.health_ai import get_ai_response
from ai_module.ollama_service import get_ollama_service
from database import db, init_db, SymptomAnalysis, MedicineVerification
from medicine_database import verify_medicine_in_database, get_medicine_info
import logging

load_dotenv()

# Helper function to convert numpy types to native Python types for JSON serialization
def convert_numpy_types(obj):
    """Recursively convert numpy types to Python native types"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.bool_, np.bool)):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, (np.ndarray, np.generic)):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    return obj

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///health_assistant.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
init_db(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'AI Health Assistant'}), 200

@app.route('/api/symptoms', methods=['POST'])
def analyze_symptoms():
    try:
        data = request.json
        symptoms_input = data.get('symptoms', '')
        
        if not symptoms_input:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # ===== STEP 1: NLP SYMPTOM MAPPING =====
        # Map natural language input to known symptoms
        symptom_mappings = map_user_symptoms(symptoms_input)
        mapping_summary, mapping_confidence, mapped_symptoms_list = get_symptom_mapping_summary(symptom_mappings)
        
        # Convert mapped symptoms to comma-separated string for prediction
        mapped_symptoms_str = ','.join(mapped_symptoms_list)
        
        logger.info(f"User input: {symptoms_input} → Mapped to: {mapped_symptoms_str}")
        
        # ===== STEP 1.5: VALIDATE SYMPTOM SUPPORT =====
        # Check if mapped symptoms are supported by the ML model
        validation_result = validate_symptoms_support(mapped_symptoms_list)
        
        if not validation_result['all_supported']:
            # Some or all symptoms are not supported
            unsupported_symptoms = validation_result['unsupported']
            common_suggestions = validation_result['common_suggestions']
            
            logger.warning(f"Unsupported symptoms: {unsupported_symptoms}")
            
            return jsonify({
                'status': 'unsupported_symptom',
                'user_input': symptoms_input,
                'symptom_mappings': symptom_mappings,
                'mapping_summary': mapping_summary,
                'mapping_confidence': mapping_confidence,
                'mapped_symptoms': mapped_symptoms_list,
                'supported_symptoms': validation_result['supported'],
                'unsupported_symptoms': unsupported_symptoms,
                'message': f"✓ We understood your symptom(s): {', '.join(unsupported_symptoms)}\n⚠️ However, these symptom(s) are not yet supported in our current prediction model.",
                'suggestion': f"💡 Try adding more common symptoms like: {', '.join(common_suggestions)}",
                'common_suggestions': common_suggestions,
                'error_type': 'unsupported_symptom_after_nlp'
            }), 200
        
        # ===== STEP 2: DISEASE PREDICTION =====
        # Use mapped symptoms for prediction
        result = predict_disease_from_symptoms(mapped_symptoms_str)
        results_list = result.get('results', [])
        
        # Prepare data for database with proper serialization
        try:
            # Extract basic recommendations from results
            recommendations_list = []
            for r in results_list:
                recommendations_list.append(r.get('advice', ''))
            
            # Create a simplified results version for storage
            simplified_results = []
            for r in results_list:
                simplified_results.append({
                    'disease': r.get('disease'),
                    'confidence': r.get('confidence'),
                    'advice': r.get('advice')
                })
            
            # Store in database with simplified data
            primary_disease_name = (results_list[0]['disease'] if results_list else 'Unknown')
            primary_confidence = (results_list[0]['confidence'] if results_list else 0)
            
            analysis = SymptomAnalysis(
                user_symptoms=json.dumps(symptoms_input),
                primary_disease=primary_disease_name,
                confidence=primary_confidence,
                risk_level=result.get('risk_level', 'Unknown'),
                emergency_alert=result.get('emergency_alert', False),
                all_results=json.dumps(simplified_results),
                recommendations=json.dumps(recommendations_list)
            )
            db.session.add(analysis)
            db.session.commit()
        except Exception as db_error:
            logger.warning(f"Database storage skipped: {str(db_error)}")
            db.session.rollback()
        
        # ===== STEP 3: AI EXPLANATION (USING LOCAL OLLAMA) =====
        # Generate AI explanation for the predicted disease using local Llama 3
        ai_explanation = None
        try:
            ollama_service = get_ollama_service()
            if primary_disease_obj:
                explanation_result = ollama_service.generate_explanation(
                    disease=primary_disease_obj.get('disease', 'Unknown'),
                    symptoms=mapped_symptoms_list,
                    confidence=primary_disease_obj.get('confidence', 0)
                )
                ai_explanation = explanation_result.get('explanation')
        except Exception as e:
            logger.warning(f"AI explanation generation failed: {str(e)}")
        
        # ===== STEP 4: RETURN RESULTS WITH NLP INFO AND AI EXPLANATION =====
        # Return full results with NLP mapping information and AI explanation
        primary_disease_obj = results_list[0] if results_list else None
        
        return jsonify({
            'status': 'success',
            # Original user input and mapped result
            'user_input': symptoms_input,
            'symptom_mappings': symptom_mappings,
            'mapping_summary': mapping_summary,
            'mapping_confidence': mapping_confidence,
            'mapped_symptoms': mapped_symptoms_list,
            
            # Disease prediction results
            'primary_disease': primary_disease_obj,
            'results': results_list,
            'risk_level': result.get('risk_level'),
            'emergency_alert': result.get('emergency_alert'),
            'when_to_see_doctor': result.get('when_to_see_doctor'),
            'symptom_count': result.get('symptom_count'),
            'data_quality_warning': result.get('data_quality_warning'),
            'recommendations': [r.get('advice', '') for r in results_list],
            
            # AI-generated explanation
            'ai_explanation': ai_explanation
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in symptom analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/symptoms/suggestions', methods=['GET'])
def get_symptom_list():
    """Get available symptoms for autocomplete"""
    try:
        suggestions = get_symptom_suggestions()
        return jsonify({'symptoms': suggestions}), 200
    except Exception as e:
        logger.error(f"Error fetching symptoms: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/symptoms/map', methods=['POST'])
def map_symptoms_endpoint():
    """
    NLP endpoint to test symptom mapping independently
    Returns what the system understands the user input as
    """
    try:
        data = request.json
        user_input = data.get('symptom', '')
        
        if not user_input:
            return jsonify({'error': 'No symptom provided'}), 400
        
        # Map the symptom
        mappings = map_user_symptoms(user_input)
        summary, confidence, mapped = get_symptom_mapping_summary(mappings)
        
        return jsonify({
            'user_input': user_input,
            'mappings': mappings,
            'summary': summary,
            'confidence': confidence,
            'mapped_symptoms': mapped,
            'is_recognized': confidence >= 0.6
        }), 200
    except Exception as e:
        logger.error(f"Error in symptom mapping: {str(e)}")
        return jsonify({'error': str(e)}), 500
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-medicine', methods=['POST'])
def verify_medicine_handler():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image']
        image_filename = image.filename
        
        logger.info(f"Processing medicine image: {image_filename}")
        
        # Use enhanced detection with OCR and ML
        result = verify_medicine_enhanced(image)
        
        # Convert numpy types to native Python types for JSON serialization
        result = convert_numpy_types(result)
        
        # Check if verification had an error
        if 'error' in result:
            logger.error(f"Medicine verification error: {result.get('error')}")
            return jsonify({
                'is_authentic': False,
                'final_confidence': 0,
                'error': result.get('error'),
                'recommendation': 'Unable to process image. Please try with a clearer medicine package photo.',
                'reasoning': []
            }), 200
        
        # Store in database (with error handling)
        try:
            verification = MedicineVerification(
                image_filename=image_filename,
                is_authentic=result.get('is_authentic', False),
                confidence=result.get('final_confidence', 0),
                ocr_data=json.dumps(result.get('ocr_result', {})),
                image_analysis=json.dumps(result.get('image_analysis', {})),
                decision_logic=json.dumps(result.get('decision_logic', {})),
                recommendation=result.get('recommendation', '')
            )
            db.session.add(verification)
            db.session.commit()
        except Exception as db_error:
            logger.warning(f"Database storage skipped: {str(db_error)}")
            db.session.rollback()
        
        # ===== AI EXPLANATION (USING LOCAL OLLAMA) =====
        # Generate AI explanation for the medicine detection result using Llama 3
        ai_explanation = None
        try:
            ollama_service = get_ollama_service()
            medicine_name = result.get('medicine_name', 'Unknown Medicine')
            explanation_result = ollama_service.explain_medicine_detection(
                medicine_name=medicine_name,
                detection_result={
                    'confidence': result.get('final_confidence', 0),
                    'is_recognized': result.get('is_authentic', False),
                    'packaging_quality': 'high' if result.get('is_authentic') else 'low'
                }
            )
            ai_explanation = explanation_result.get('explanation')
        except Exception as e:
            logger.warning(f"AI explanation generation failed: {str(e)}")
        
        return jsonify({
            'is_authentic': result.get('is_authentic'),
            'final_confidence': result.get('final_confidence'),
            'ocr_result': result.get('ocr_result'),
            'image_analysis': result.get('image_analysis'),
            'rule_checks': result.get('rule_checks'),
            'decision_logic': result.get('decision_logic'),
            'recommendation': result.get('recommendation'),
            'reasoning': result.get('reasoning', []),
            'ai_explanation': ai_explanation
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in medicine verification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_user_history():
    """Get all symptom analysis history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        analyses = SymptomAnalysis.query.order_by(SymptomAnalysis.created_at.desc()).limit(limit).all()
        return jsonify({'history': [a.to_dict() for a in analyses]}), 200
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/symptoms/history', methods=['GET'])
def get_symptom_history():
    """Get symptom analysis history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        analyses = SymptomAnalysis.query.order_by(SymptomAnalysis.created_at.desc()).limit(limit).all()
        return jsonify({'data': [a.to_dict() for a in analyses]}), 200
    except Exception as e:
        logger.error(f"Error fetching symptom history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicine/history', methods=['GET'])
def get_medicine_history():
    """Get medicine verification history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        verifications = MedicineVerification.query.order_by(MedicineVerification.created_at.desc()).limit(limit).all()
        return jsonify({'data': [v.to_dict() for v in verifications]}), 200
    except Exception as e:
        logger.error(f"Error fetching medicine history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/symptoms/report/<int:id>', methods=['GET'])
def get_symptom_report(id):
    """Get detailed symptom analysis report"""
    try:
        analysis = SymptomAnalysis.query.get(id)
        if not analysis:
            return jsonify({'error': 'Report not found'}), 404
        return jsonify(analysis.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching symptom report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicine/report/<int:id>', methods=['GET'])
def get_medicine_report(id):
    """Get detailed medicine verification report"""
    try:
        verification = MedicineVerification.query.get(id)
        if not verification:
            return jsonify({'error': 'Report not found'}), 404
        return jsonify(verification.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching medicine report: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get usage statistics"""
    try:
        symptom_count = SymptomAnalysis.query.count()
        medicine_count = MedicineVerification.query.count()
        return jsonify({
            'symptom_analyses': symptom_count,
            'medicine_verifications': medicine_count,
            'total_analyses': symptom_count + medicine_count
        }), 200
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ===== NEW: AI/LLM ENDPOINTS =====

@app.route('/api/ai/status', methods=['GET'])
def ai_status():
    """Check if Ollama AI service is available"""
    try:
        ollama_service = get_ollama_service()
        is_available = ollama_service.is_available
        
        return jsonify({
            'status': 'operational' if is_available else 'unavailable',
            'available': is_available,
            'model': os.getenv('OLLAMA_MODEL', 'tinyllama'),
            'api_url': os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
        }), 200
    except Exception as e:
        logger.error(f"Error checking AI status: {str(e)}")
        return jsonify({
            'status': 'error',
            'available': False,
            'error': str(e)
        }), 500

@app.route('/api/ai/explain', methods=['POST'])
def generate_explanation():
    """
    Generate AI-powered explanation for disease prediction
    
    Request:
    {
        "disease": "Flu",
        "symptoms": ["fever", "cough"],
        "confidence": 62
    }
    
    Response:
    {
        "explanation": "AI-generated explanation...",
        "disclaimer": "..."
    }
    """
    try:
        data = request.json
        disease = data.get('disease', 'Unknown')
        symptoms = data.get('symptoms', [])
        confidence = data.get('confidence', 0)
        
        ai_service = get_ai_service()
        result = ai_service.generate_explanation(disease, symptoms, confidence)
        
        return jsonify({
            'status': 'success',
            'disease': disease,
            'confidence': confidence,
            'ai_explanation': result
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'Note': 'AI explanation temporarily unavailable'
        }), 500

@app.route('/api/ai/extract-symptoms', methods=['POST'])
def extract_symptoms_ai():
    """
    Extract symptoms from natural language using LLM
    
    Request:
    {
        "text": "I have hair fall and feel very tired"
    }
    
    Response:
    {
        "extracted_symptoms": ["hair loss", "fatigue"],
        "confidence": 0.92,
        "explanation": "..."
    }
    """
    try:
        data = request.json
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({'error': 'No text provided'}), 400
        
        # Get list of known symptoms for reference
        known_symptoms = get_symptom_suggestions()
        
        ai_service = get_ai_service()
        result = ai_service.extract_symptoms_from_text(user_input, known_symptoms)
        
        return jsonify({
            'status': 'success',
            'user_input': user_input,
            'extracted_data': result
        }), 200
    
    except Exception as e:
        logger.error(f"Error extracting symptoms: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """
    Chat interface for health-related questions
    
    Request:
    {
        "message": "Is this serious?",
        "context": {
            "disease": "Flu",
            "symptoms": ["fever", "cough"],
            "confidence": 62,
            "risk_level": "Medium"
        }
    }
    
    Response:
    {
        "answer": "Based on your symptoms...",
        "follow_up_suggestions": ["...", "..."],
        "disclaimer": "..."
    }
    """
    try:
        data = request.json
        message = data.get('message', '')
        context = data.get('context', None)
        
        if not message:
            logger.warning("❌ Chat: No message provided")
            return jsonify({
                'status': 'success',
                'user_message': '',
                'ai_response': {
                    'answer': 'Please ask me a question or tell me about your symptoms.',
                    'follow_up_suggestions': [],
                    'disclaimer': '💬 Ask me anything'
                }
            }), 200
        
        logger.info(f"💬 Chat request: {message[:60]}...")
        
        # Use Ollama local LLM for chat responses
        try:
            ollama_service = get_ollama_service()
            print(f"🔍 Flask: Got ollama_service instance")
            
            logger.info(f"🔄 Flask: Calling ollama_service.chat_answer()...")
            print(f"🔄 Flask: Calling ollama_service.chat_answer()...")
            
            result = ollama_service.chat_answer(message, context)
            
            print(f"🔍 Flask: chat_answer returned: {type(result)}")
            print(f"🔍 Flask: Result answer: {result.get('answer', '')[:60]}...")
            
            logger.info(f"✅ Flask: Got response from Ollama")
            print(f"✅ Flask: Got response from Ollama")
            
            # Store chat in database for history
            try:
                chat_log = {
                    'user_message': message,
                    'ai_response': result.get('answer', ''),
                    'context': json.dumps(context or {})
                }
                # Could extend SymptomAnalysis db model to store chat
            except:
                pass
            
            return jsonify({
                'status': 'success',
                'user_message': message,
                'ai_response': result
            }), 200
        
        except Exception as ollama_err:
            logger.error(f"❌ Ollama error: {type(ollama_err).__name__}: {str(ollama_err)}")
            import traceback
            logger.error(f"   Traceback: {traceback.format_exc()}")
            
            # Return graceful fallback response - NEVER 500!
            return jsonify({
                'status': 'success',
                'user_message': message,
                'ai_response': {
                    'answer': 'I am temporarily unavailable. Please try again in a moment. For urgent health concerns, consult a healthcare professional.',
                    'follow_up_suggestions': ['Try again', 'Check my symptoms'],
                    'disclaimer': '⚠️ Fallback response - AI service temporarily unavailable'
                }
            }), 200
    
    except Exception as e:
        logger.error(f"❌ Fatal chat error: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"   Traceback: {traceback.format_exc()}")
        
        # ALWAYS return 200 with valid JSON - NEVER return 500
        return jsonify({
            'status': 'success',
            'user_message': data.get('message', '') if isinstance(data, dict) else '',
            'ai_response': {
                'answer': 'An error occurred. Please try again or consult a healthcare professional for urgent concerns.',
                'follow_up_suggestions': [],
                'disclaimer': '⚠️ Error occurred'
            }
        }), 200

@app.route('/api/ai/advice', methods=['POST'])
def generate_health_advice():
    """
    Generate personalized health advice
    
    Request:
    {
        "disease": "Flu",
        "symptoms": ["fever", "cough"],
        "risk_level": "Medium"
    }
    
    Response:
    {
        "advice": "You should...",
        "risk_level": "Medium",
        "disclaimer": "..."
    }
    """
    try:
        data = request.json
        disease = data.get('disease', 'Unknown')
        symptoms = data.get('symptoms', [])
        risk_level = data.get('risk_level', 'Unknown')
        
        ai_service = get_ai_service()
        result = ai_service.generate_health_advice(disease, symptoms, risk_level)
        
        return jsonify({
            'status': 'success',
            'disease': disease,
            'ai_advice': result
        }), 200
    
    except Exception as e:
        logger.error(f"Error generating advice: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/ai/medicine-explanation', methods=['POST'])
def explain_medicine():
    """
    Generate explanation for medicine detection results
    
    Request:
    {
        "medicine_name": "Aspirin",
        "detection_result": {
            "confidence": 0.92,
            "packaging_quality": "high",
            "is_recognized": true
        }
    }
    
    Response:
    {
        "explanation": "The medicine detected...",
        "confidence": 0.92,
        "disclaimer": "..."
    }
    """
    try:
        data = request.json
        medicine_name = data.get('medicine_name', 'Unknown')
        detection_result = data.get('detection_result', {})
        
        ai_service = get_ai_service()
        result = ai_service.explain_medicine_detection(medicine_name, detection_result)
        
        return jsonify({
            'status': 'success',
            'medicine_explanation': result
        }), 200
    
    except Exception as e:
        logger.error(f"Error explaining medicine: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# ===== ADVANCED SYMPTOM ANALYSIS WITH AI =====

@app.route('/api/advanced/symptom-analysis', methods=['POST'])
def advanced_symptom_analysis():
    """
    Complete advanced analysis combining ML + LLM
    
    Request:
    {
        "symptoms": "I have fever and cough"
    }
    
    Response includes:
    1. NLP Mapping
    2. ML Prediction
    3. LLM Explanation
    4. Health Advice
    """
    try:
        data = request.json
        symptoms_input = data.get('symptoms', '')
        
        if not symptoms_input:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Step 1: NLP Extraction (using LLM)
        ai_service = get_ai_service()
        known_symptoms = get_symptom_suggestions()
        extracted = ai_service.extract_symptoms_from_text(symptoms_input, known_symptoms)
        
        # Get the extracted symptoms
        extracted_symptoms = extracted.get('extracted_symptoms', [])
        
        if not extracted_symptoms:
            # Fallback to traditional NLP mapping
            symptom_mappings = map_user_symptoms(symptoms_input)
            _, _, extracted_symptoms = get_symptom_mapping_summary(symptom_mappings)
        
        # Step 2: ML Prediction
        mapped_symptoms_str = ','.join(extracted_symptoms)
        prediction_result = predict_disease_from_symptoms(mapped_symptoms_str)
        
        # Get primary disease
        results_list = prediction_result.get('results', [])
        primary_disease = results_list[0] if results_list else None
        
        # Step 3: LLM Explanation (if prediction found)
        ai_explanation = None
        health_advice = None
        
        if primary_disease:
            ai_explanation = ai_service.generate_explanation(
                primary_disease['disease'],
                extracted_symptoms,
                primary_disease['confidence']
            )
            
            health_advice = ai_service.generate_health_advice(
                primary_disease['disease'],
                extracted_symptoms,
                prediction_result.get('risk_level', 'Unknown')
            )
        
        # Prepare comprehensive response
        response = {
            'status': 'success',
            'user_input': symptoms_input,
            'analysis': {
                'nlp_extraction': {
                    'extracted_symptoms': extracted_symptoms,
                    'confidence': extracted.get('confidence', 0),
                    'method': 'LLM-based extraction'
                },
                'ml_prediction': {
                    'primary_disease': primary_disease,
                    'alternatives': results_list[1:] if len(results_list) > 1 else [],
                    'risk_level': prediction_result.get('risk_level'),
                    'emergency_alert': prediction_result.get('emergency_alert')
                },
                'ai_explanation': ai_explanation,
                'health_advice': health_advice
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in advanced analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
