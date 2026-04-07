from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from ml_models.symptom_predictor import predict_disease
from ml_models.medicine_detector import verify_medicine
from ai_module.health_ai import get_ai_response
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

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
        
        result = predict_disease(symptoms)
        
        return jsonify({
            'disease': result['disease'],
            'confidence': result['confidence'],
            'risk_level': result['risk_level'],
            'recommendations': result['recommendations']
        }), 200
    except Exception as e:
        logger.error(f"Error in symptom analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-medicine', methods=['POST'])
def verify_medicine_handler():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image']
        result = verify_medicine(image)
        
        return jsonify({
            'is_authentic': result['is_authentic'],
            'confidence': result['confidence'],
            'details': result['details']
        }), 200
    except Exception as e:
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
    # TODO: Implement database queries
    return jsonify({'history': []}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
