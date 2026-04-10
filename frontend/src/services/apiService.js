/**
 * API Service for Health Chat
 * Handles all communication with the Flask backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';
const CHAT_ENDPOINT = `${API_BASE_URL}/api/chat`;
const STATUS_ENDPOINT = `${API_BASE_URL}/api/health`;

/**
 * Configuration for API requests
 */
const API_CONFIG = {
  timeout: 35000, // 35 seconds - match backend timeout + buffer
  retries: 1,
};

/**
 * Check if API is reachable
 * @returns {Promise<boolean>}
 */
export async function checkAPIStatus() {
  try {
    const response = await fetch(STATUS_ENDPOINT, {
      method: 'GET',
      timeout: 5000,
    });
    return response.ok;
  } catch (error) {
    console.warn('API status check failed:', error);
    return false;
  }
}

/**
 * Send a message to the health assistant API
 * @param {string} message - The user's message
 * @param {object} context - Optional context about symptoms/disease
 * @returns {Promise<{status: string, reply: string, response_time: number, error?: string}>}
 */
export async function sendChatMessage(message, context = null) {
  if (!message || !message.trim()) {
    throw new Error('Message cannot be empty');
  }

  const payload = {
    message: message.trim(),
  };

  // Add context if provided
  if (context) {
    payload.context = context;
  }

  try {
    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);

    const response = await fetch(CHAT_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    // Handle non-OK responses
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('API endpoint not found. Make sure the Flask backend is running.');
      }
      if (response.status === 500) {
        throw new Error('Server error. Please check if the backend is running correctly.');
      }
      throw new Error(`Server returned ${response.status}: ${response.statusText}`);
    }

    // Parse JSON response
    const data = await response.json();

    // Check for errors in response
    if (data.status === 'error') {
      throw new Error(data.reply || data.error || 'Unknown error occurred');
    }

    // Return the AI response
    return {
      status: 'success',
      reply: data.reply || 'No response',
      response_time: data.response_time || 0,
    };
  } catch (error) {
    // Handle different types of errors
    if (error.name === 'AbortError') {
      throw new Error('Request timeout. The AI took too long to respond. Please try again.');
    }

    if (error instanceof TypeError) {
      // Network error
      throw new Error(
        'Cannot connect to the API. Make sure:\n' +
        '1. The Flask backend is running (python chat_app.py)\n' +
        '2. Ollama is running (ollama serve)\n' +
        '3. You\'re using http://localhost:5000 (not https)'
      );
    }

    // Re-throw the error as-is
    throw error;
  }
}

/**
 * Format error message for display
 * @param {Error} error - The error object
 * @returns {string} - Formatted error message
 */
export function formatErrorMessage(error) {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return (
      'Connection Error: Cannot reach the API. Please ensure:\n' +
      '• Flask backend is running: python chat_app.py\n' +
      '• Ollama is running: ollama serve\n' +
      '• API is at http://localhost:5000'
    );
  }

  if (error.message.includes('timeout')) {
    return (
      'Response Timeout: The AI took too long to respond.\n' +
      'This might mean:\n' +
      '• Ollama is still loading the model\n' +
      '• Your system is under heavy load\n' +
      '• The model is processing a complex response\n\n' +
      'Please try again in a moment.'
    );
  }

  return error.message || 'An unexpected error occurred. Please try again.';
}
