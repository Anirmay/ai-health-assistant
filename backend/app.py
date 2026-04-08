from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import numpy as np
from ml_models.symptom_disease_model import predict_disease_from_symptoms, get_symptom_suggestions
from ml_models.medicine_detector import verify_medicine
from ml_models.medicine_detector_enhanced import verify_medicine_enhanced
from ai_module.health_ai import get_ai_response
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
        symptoms = data.get('symptoms', '')
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Use enhanced ML model
        result = predict_disease_from_symptoms(symptoms)
        
        # Prepare data for database with proper serialization
        try:
            # Extract basic recommendations from results
            recommendations_list = []
            for r in result.get('results', []):
                recommendations_list.append(r.get('advice', ''))
            
            # Create a simplified results version for storage
            simplified_results = []
            for r in result.get('results', []):
                simplified_results.append({
                    'disease': r.get('disease'),
                    'confidence': r.get('confidence'),
                    'advice': r.get('advice')
                })
            
            # Store in database with simplified data
            analysis = SymptomAnalysis(
                user_symptoms=json.dumps(symptoms) if isinstance(symptoms, list) else symptoms,
                primary_disease=result.get('primary_disease', 'Unknown'),
                confidence=result.get('results', [{}])[0].get('confidence', 0) if result.get('results') else 0,
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
        
        # Return full results with reasoning
        return jsonify({
            'primary_disease': result.get('primary_disease'),
            'results': result.get('results', []),
            'risk_level': result.get('risk_level'),
            'emergency_alert': result.get('emergency_alert'),
            'when_to_see_doctor': result.get('when_to_see_doctor'),
            'symptom_count': result.get('symptom_count'),
            'data_quality_warning': result.get('data_quality_warning'),  # ← NEW FIELD
            'recommendations': [r.get('advice', '') for r in result.get('results', [])]
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
        
        return jsonify({
            'is_authentic': result.get('is_authentic'),
            'final_confidence': result.get('final_confidence'),
            'ocr_result': result.get('ocr_result'),
            'image_analysis': result.get('image_analysis'),
            'rule_checks': result.get('rule_checks'),
            'decision_logic': result.get('decision_logic'),
            'recommendation': result.get('recommendation'),
            'reasoning': result.get('reasoning', [])
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in medicine verification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = get_ai_response(message)
        
        return jsonify({
            'response': response,
            'success': True
        }), 200
    except Exception as e:
        logger.error(f"Error in AI chat: {str(e)}")
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
