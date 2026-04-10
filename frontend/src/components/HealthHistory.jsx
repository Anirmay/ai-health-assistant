import React, { useState, useEffect, useContext } from 'react';
import { 
  loadHistory, 
  clearHistory, 
  deleteHistoryEntry, 
  getHistoryStats,
  getHistoryCount 
} from '../services/healthAnalysisService';
import { LanguageContext, ThemeContext } from '../App';
import toast from 'react-hot-toast';

/**
 * FEATURE 3: HISTORY PAGE (React)
 * 
 * Features:
 * - Load data from localStorage on mount
 * - Display each entry (symptoms, result, date)
 * - Show "No history yet" if empty
 * - Delete individual entries
 * - Clear all history
 * - Show statistics
 * - Modern glassmorphic UI design
 */
function HealthHistory() {
  const { language, t } = useContext(LanguageContext) || {};
  const { primaryColor, dangerColor, isDarkMode, bgPrimary, bgSecondary, textPrimary, textSecondary, textMuted } = useContext(ThemeContext) || {};
  
  const translationFunc = t || ((section, key) => key);
  
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState({
    totalEntries: 0,
    firstEntry: null,
    lastEntry: null,
    averageLength: 0
  });

  // Load history from localStorage on component mount (FEATURE 3)
  useEffect(() => {
    loadHistoryData();
  }, []);

  const loadHistoryData = () => {
    try {
      setIsLoading(true);
      const historyData = loadHistory();
      const historyStats = getHistoryStats();
      
      setHistory(historyData);
      setStats(historyStats);
    } catch (error) {
      console.error('Error loading history:', error);
      toast.error('Failed to load history');
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handle clearing all history (FEATURE 5)
   */
  const handleClearHistory = () => {
    if (window.confirm('Are you sure you want to delete all history? This cannot be undone.')) {
      try {
        clearHistory();
        setHistory([]);
        setStats({
          totalEntries: 0,
          firstEntry: null,
          lastEntry: null,
          averageLength: 0
        });
        toast.success('All history cleared');
      } catch (error) {
        console.error('Error clearing history:', error);
        toast.error('Failed to clear history');
      }
    }
  };

  /**
   * Handle deleting individual entry
   */
  const handleDeleteEntry = (entryId) => {
    try {
      const updatedHistory = deleteHistoryEntry(entryId);
      setHistory(updatedHistory);
      setStats(getHistoryStats());
      toast.success('Entry deleted');
    } catch (error) {
      console.error('Error deleting entry:', error);
      toast.error('Failed to delete entry');
    }
  };

  /**
   * Format date for display
   */
  const formatDate = (dateStr) => {
    try {
      return new Date(dateStr).toLocaleString();
    } catch {
      return dateStr;
    }
  };

  // Loading state with modern design
  if (isLoading) {
    return (
      <div style={{
        minHeight: "100vh",
        background: isDarkMode ? "radial-gradient(circle at center, #0a0f2c, #020617)" : "#F8F3E1",
        color: textPrimary,
        paddingTop: "60px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transition: "all 0.3s ease"
      }}>
        <div style={{
          textAlign: "center",
          padding: "40px"
        }}>
          <div style={{
            display: "flex",
            justifyContent: "center",
            gap: "8px",
            marginBottom: "20px"
          }}>
            <div style={{
              width: "12px",
              height: "12px",
              background: primaryColor,
              borderRadius: "50%",
              animation: "bounce 1.4s infinite"
            }}></div>
            <div style={{
              width: "12px",
              height: "12px",
              background: primaryColor,
              borderRadius: "50%",
              animation: "bounce 1.4s infinite 0.2s"
            }}></div>
            <div style={{
              width: "12px",
              height: "12px",
              background: primaryColor,
              borderRadius: "50%",
              animation: "bounce 1.4s infinite 0.4s"
            }}></div>
          </div>
          <p style={{ color: textMuted, fontSize: "16px" }}>{translationFunc('history', 'loading')}</p>
          <style>{`
            @keyframes bounce {
              0%, 80%, 100% { transform: translateY(0); }
              40% { transform: translateY(-20px); }
            }
          `}</style>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: isDarkMode ? "radial-gradient(circle at center, #0a0f2c, #020617)" : "#F8F3E1",
      color: textPrimary,
      paddingTop: "60px",
      paddingBottom: "40px",
      transition: "all 0.3s ease"
    }}>
      <div style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "25px"
      }}>
        {/* Header */}
        <div style={{
          marginBottom: "30px"
        }}>
          <h1 style={{ fontSize: "32px", fontWeight: "bold", marginBottom: "8px", color: textPrimary }}>
            📋 {translationFunc('history', 'title')}
          </h1>
          <p style={{ color: textMuted, fontSize: "16px" }}>
            {translationFunc('history', 'empty')}
          </p>
        </div>

        {/* Statistics Section - if history exists */}
        {history.length > 0 && (
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "15px",
            marginBottom: "30px"
          }}>
            <div style={{
              background: bgSecondary,
              border: `1px solid ${primaryColor}30`,
              borderRadius: "12px",
              padding: "20px",
              backdropFilter: "blur(10px)",
              transition: "all 0.3s ease"
            }}>
              <p style={{ color: textMuted, fontSize: "12px", marginBottom: "8px" }}>Total Entries</p>
              <p style={{ fontSize: "28px", fontWeight: "bold", color: primaryColor }}>{stats.totalEntries}</p>
            </div>
            <div style={{
              background: bgSecondary,
              border: `1px solid ${primaryColor}30`,
              borderRadius: "12px",
              padding: "20px",
              backdropFilter: "blur(10px)",
              transition: "all 0.3s ease"
            }}>
              <p style={{ color: textMuted, fontSize: "12px", marginBottom: "8px" }}>Last Entry</p>
              <p style={{ fontSize: "14px", color: textPrimary, wordBreak: "break-word" }}>{stats.lastEntry || 'N/A'}</p>
            </div>
            <div style={{
              background: bgSecondary,
              border: `1px solid ${primaryColor}30`,
              borderRadius: "12px",
              padding: "20px",
              backdropFilter: "blur(10px)",
              transition: "all 0.3s ease"
            }}>
              <p style={{ color: textMuted, fontSize: "12px", marginBottom: "8px" }}>Avg. Analysis Length</p>
              <p style={{ fontSize: "28px", fontWeight: "bold", color: primaryColor }}>{stats.averageLength}</p>
            </div>
          </div>
        )}

        {/* Empty State */}
        {history.length === 0 ? (
          <div style={{
            textAlign: "center",
            padding: "60px 20px",
            background: bgSecondary,
            borderRadius: "16px",
            border: `2px dashed ${primaryColor}30`,
            backdropFilter: "blur(10px)",
            transition: "all 0.3s ease"
          }}>
            <p style={{ fontSize: "28px", marginBottom: "12px" }}>📋</p>
            <p style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "8px", color: textPrimary }}>{translationFunc('history', 'empty')}</p>
            <p style={{ color: textMuted, fontSize: "16px" }}>
              {translationFunc('history', 'empty')}
            </p>
          </div>
        ) : (
          <>
            {/* History Entries */}
            <div style={{
              display: "flex",
              flexDirection: "column",
              gap: "16px",
              marginBottom: "30px"
            }}>
              {history
                .slice()
                .reverse() // Show newest first
                .map((entry, index) => (
                  <div
                    key={entry.id || index}
                    style={{
                      background: bgSecondary,
                      border: `1px solid ${primaryColor}30`,
                      borderLeft: `4px solid ${primaryColor}`,
                      borderRadius: "12px",
                      padding: "20px",
                      backdropFilter: "blur(10px)",
                      transition: "all 0.3s ease",
                      cursor: "pointer"
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = isDarkMode ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.04)";
                      e.currentTarget.style.boxShadow = `0 8px 32px ${primaryColor}1a`;
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = bgSecondary;
                      e.currentTarget.style.boxShadow = "none";
                    }}
                  >
                    {/* Entry Header */}
                    <div style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      marginBottom: "16px",
                      paddingBottom: "12px",
                      borderBottom: `1px solid ${primaryColor}20`
                    }}>
                      <div>
                        <p style={{ fontSize: "12px", color: primaryColor }}>
                          📅 {formatDate(entry.date)}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDeleteEntry(entry.id)}
                        style={{
                          padding: "6px 12px",
                          fontSize: "12px",
                          background: isDarkMode ? `${dangerColor}22` : `${dangerColor}15`,
                          color: isDarkMode ? "#fecaca" : dangerColor,
                          border: `1px solid ${dangerColor}50`,
                          borderRadius: "6px",
                          cursor: "pointer",
                          transition: "all 0.2s ease"
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.background = isDarkMode ? `${dangerColor}33` : `${dangerColor}25`;
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.background = isDarkMode ? `${dangerColor}22` : `${dangerColor}15`;
                        }}
                      >
                        🗑️ Delete
                      </button>
                    </div>

                    {/* Symptoms */}
                    <div style={{
                      marginBottom: "16px"
                    }}>
                      <h3 style={{ fontSize: "12px", color: primaryColor, fontWeight: "bold", marginBottom: "6px" }}>
                        Symptoms:
                      </h3>
                      <p style={{ color: textPrimary, lineHeight: "1.5" }}>
                        {entry.symptoms}
                      </p>
                    </div>

                    {/* Result */}
                    <div>
                      <h3 style={{ fontSize: "12px", color: primaryColor, fontWeight: "bold", marginBottom: "6px" }}>
                        ✨ AI Analysis:
                      </h3>
                      <pre style={{ 
                        color: textSecondary,
                        fontSize: "13px",
                        lineHeight: "1.6",
                        whiteSpace: "pre-wrap",
                        wordWrap: "break-word",
                        margin: 0
                      }}>
                        {entry.result}
                      </pre>
                    </div>
                  </div>
                ))}
            </div>

            {/* Clear History Button */}
            <div style={{ display: "flex", justifyContent: "center" }}>
              <button
                onClick={handleClearHistory}
                style={{
                  padding: "12px 28px",
                  fontSize: "14px",
                  fontWeight: "bold",
                  background: isDarkMode ? `linear-gradient(to right, ${dangerColor}cc, ${dangerColor}aa)` : `linear-gradient(to right, ${dangerColor}80, ${dangerColor}70)`,
                  color: isDarkMode ? "#fecaca" : "white",
                  border: `1px solid ${dangerColor}50`,
                  borderRadius: "10px",
                  cursor: "pointer",
                  transition: "all 0.3s ease"
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = isDarkMode ? `linear-gradient(to right, ${dangerColor}, ${dangerColor}dd)` : `linear-gradient(to right, ${dangerColor}, ${dangerColor}90)`;
                  e.currentTarget.style.boxShadow = `0 0 20px ${dangerColor}66`;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = isDarkMode ? `linear-gradient(to right, ${dangerColor}cc, ${dangerColor}aa)` : `linear-gradient(to right, ${dangerColor}80, ${dangerColor}70)`;
                  e.currentTarget.style.boxShadow = "none";
                }}
              >
                🗑️ Clear All History
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default HealthHistory;
