/**
 * Health Analysis Service
 * Handles symptom analysis, history management, and localStorage operations
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';
const ANALYZE_ENDPOINT = `${API_BASE_URL}/analyze`;
const STORAGE_KEY = 'healthHistory';

/**
 * FEATURE 1: SYMPTOM ANALYZER
 * Sends symptoms to the backend and gets AI analysis
 * @param {string} symptoms - User's symptoms description
 * @returns {Promise<{result: string}>}
 */
export async function analyzeSymptoms(symptoms) {
  if (!symptoms || !symptoms.trim()) {
    throw new Error('Please enter your symptoms');
  }

  try {
    const response = await fetch(ANALYZE_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        symptoms: symptoms.trim()
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to analyze symptoms');
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error('Error analyzing symptoms:', error);
    throw error;
  }
}

/**
 * FEATURE 2 & 5: LOCAL STORAGE MANAGEMENT
 */

/**
 * Get existing history from localStorage
 * @returns {Array} Array of health history entries
 */
export function getHealthHistory() {
  try {
    const history = localStorage.getItem(STORAGE_KEY);
    return history ? JSON.parse(history) : [];
  } catch (error) {
    console.error('Error reading history from localStorage:', error);
    return [];
  }
}

/**
 * Save a new entry to health history
 * @param {Object} entry - Entry object with symptoms, result, and date
 * @returns {Array} Updated history array
 */
export function saveToHistory(entry) {
  try {
    const history = getHealthHistory();
    
    // Validate entry
    if (!entry.symptoms || !entry.result) {
      throw new Error('Entry must contain symptoms and result');
    }

    // Create new entry with timestamp
    const newEntry = {
      id: Date.now(),
      symptoms: entry.symptoms,
      result: entry.result,
      date: new Date().toLocaleString(),
      timestamp: Date.now()
    };

    history.push(newEntry);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    
    return history;
  } catch (error) {
    console.error('Error saving to history:', error);
    throw error;
  }
}

/**
 * FEATURE 3: LOAD HISTORY
 * Get all history entries from localStorage
 * @returns {Array} All health history entries
 */
export function loadHistory() {
  return getHealthHistory();
}

/**
 * FEATURE 4: HISTORY COUNT
 * Get total number of history entries
 * @returns {number} Count of history entries
 */
export function getHistoryCount() {
  return getHealthHistory().length;
}

/**
 * FEATURE 5: CLEAR HISTORY
 * Remove all history from localStorage
 * @returns {void}
 */
export function clearHistory() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error('Error clearing history:', error);
    throw error;
  }
}

/**
 * Delete a single history entry
 * @param {number} entryId - ID of the entry to delete
 * @returns {Array} Updated history array
 */
export function deleteHistoryEntry(entryId) {
  try {
    const history = getHealthHistory();
    const filtered = history.filter(entry => entry.id !== entryId);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
    return filtered;
  } catch (error) {
    console.error('Error deleting history entry:', error);
    throw error;
  }
}

/**
 * Export history data as JSON
 * @returns {string} JSON string of history
 */
export function exportHistory() {
  try {
    const history = getHealthHistory();
    return JSON.stringify(history, null, 2);
  } catch (error) {
    console.error('Error exporting history:', error);
    throw error;
  }
}

/**
 * Get history statistics
 * @returns {Object} Statistics about the history
 */
export function getHistoryStats() {
  try {
    const history = getHealthHistory();
    const stats = {
      totalEntries: history.length,
      firstEntry: history.length > 0 ? history[0].date : null,
      lastEntry: history.length > 0 ? history[history.length - 1].date : null,
      averageLength: history.length > 0 
        ? Math.round(history.reduce((sum, entry) => sum + entry.result.length, 0) / history.length)
        : 0
    };
    return stats;
  } catch (error) {
    console.error('Error getting history stats:', error);
    return { totalEntries: 0, firstEntry: null, lastEntry: null, averageLength: 0 };
  }
}
