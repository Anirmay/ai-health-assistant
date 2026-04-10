"""
Flask Backend API for AI Health Assistant
Provides REST API endpoints for health-related chat and analysis.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
from ollama_chat import OllamaChatService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for React frontend at localhost:5173
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    }
)

# Initialize Ollama Chat Service
ollama_service = OllamaChatService(
    api_url=os.getenv("OLLAMA_API_URL", "http://localhost:11434"),
    model=os.getenv("OLLAMA_MODEL", "llama3"),
    timeout=int(os.getenv("OLLAMA_TIMEOUT", "30")),
    temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.9")),
    top_p=float(os.getenv("OLLAMA_TOP_P", "0.9")),
    repeat_penalty=float(os.getenv("OLLAMA_REPEAT_PENALTY", "1.2")),
)

logger.info("=" * 60)
logger.info("🏥 AI Health Assistant Backend API")
logger.info("=" * 60)


# ============================================================================
# HEALTH CHECK & STATUS ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns: { "status": "healthy", "service": "AI Health Assistant" }
    """
    return jsonify({
        'status': 'healthy',
        'service': 'AI Health Assistant',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/status', methods=['GET'])
def api_status():
    """
    Get API and Ollama service status.
    """
    ollama_available = ollama_service.is_available()
    
    return jsonify({
        'api': 'online',
        'ollama': 'online' if ollama_available else 'offline',
        'model': ollama_service.model,
        'api_url': ollama_service.api_url,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get service statistics and metrics.
    """
    return jsonify({
        'service': 'AI Health Assistant',
        'stats': ollama_service.get_stats()
    }), 200


# ============================================================================
# MAIN CHAT ENDPOINT
# ============================================================================

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """
    Main chat endpoint for health-related questions.
    
    Request (POST):
    {
        "message": "I have a fever and cough"
    }
    
    Response:
    {
        "reply": "Here's what I suggest...",
        "status": "success",
        "response_time": 2.5
    }
    
    Error Response:
    {
        "reply": "I'm experiencing technical issues...",
        "status": "error",
        "error": "timeout"
    }
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Parse request
        data = request.get_json()
        
        if not data:
            logger.warning("❌ No JSON data in request")
            return jsonify({
                'reply': 'Please send a valid JSON request with a "message" field.',
                'status': 'error',
                'error': 'invalid_request'
            }), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            logger.warning("⚠️ Empty message received")
            return jsonify({
                'reply': 'Please ask me a health-related question.',
                'status': 'error',
                'error': 'empty_message'
            }), 400
        
        # Log incoming request
        logger.info(f"📨 Chat request from client: {user_message[:60]}...")
        
        # Get response from Ollama service
        response = ollama_service.chat(user_message)
        
        # Return response (with status 200 even for errors to ensure frontend gets response)
        status_code = 200 if response['status'] == 'success' else 200
        return jsonify(response), status_code
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in /chat endpoint: {type(e).__name__}: {str(e)}")
        
        # Return error response
        return jsonify({
            'reply': 'An unexpected error occurred. Please try again.',
            'status': 'error',
            'error': str(e)
        }), 500


# ============================================================================
# CONFIGURATION & DEBUGGING ENDPOINTS
# ============================================================================

@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get API configuration (for debugging).
    """
    return jsonify({
        'ollama': {
            'api_url': ollama_service.api_url,
            'model': ollama_service.model,
            'timeout': ollama_service.timeout,
            'temperature': ollama_service.temperature,
            'top_p': ollama_service.top_p,
            'repeat_penalty': ollama_service.repeat_penalty,
            'endpoint': ollama_service.endpoint
        },
        'cors_allowed_origins': [
            'http://localhost:5173',
            'http://localhost:3000',
            'http://127.0.0.1:5173'
        ]
    }), 200


@app.route('/api/reset-stats', methods=['POST'])
def reset_stats():
    """
    Reset service statistics.
    """
    ollama_service.reset_stats()
    logger.info("📊 Statistics reset by user")
    return jsonify({
        'status': 'success',
        'message': 'Statistics reset'
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'path': request.path,
        'method': request.method
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'path': request.path,
        'method': request.method,
        'allowed_methods': ['GET', 'POST', 'OPTIONS']
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 Internal Server Error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Please try again later'
    }), 500


# ============================================================================
# APP INITIALIZATION
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Starting Flask server on port {port}")
    logger.info(f"🔗 Health check: http://localhost:{port}/api/health")
    logger.info(f"💬 Chat endpoint: POST http://localhost:{port}/api/chat")
    logger.info(f"📊 Status: http://localhost:{port}/api/status")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=False
    )
