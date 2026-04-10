import { useState, useContext } from "react";
import { saveToHistory } from "../services/healthAnalysisService";
import { LanguageContext, ThemeContext } from "../App";
import toast from "react-hot-toast";

export default function Symptom() {
  const { language, t } = useContext(LanguageContext) || {};
  const { primaryColor, successColor, warningColor, dangerColor, isDarkMode, bgPrimary, bgSecondary, textPrimary, textSecondary, textMuted } = useContext(ThemeContext) || {};

  const translationFunc = t || ((section, key) => key);
  const [inputValue, setInputValue] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const symptomsList = [
    "fever", "cough", "headache", "fatigue",
    "sore throat", "body ache", "nausea",
    "diarrhea", "shortness of breath", "chest pain"
  ];

  const addSymptom = (symptom) => {
    if (!inputValue.includes(symptom)) {
      setInputValue((prev) =>
        prev ? prev + ", " + symptom : symptom
      );
    }
  };

  const analyzeSymptoms = async () => {
    if (!inputValue.trim()) {
      setError("Please enter your symptoms first");
      return;
    }

    setLoading(true);
    setError("");
    setResult("");

    try {
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ symptoms: inputValue }),
      });

      if (!res.ok) {
        throw new Error("Backend error. Please try again.");
      }

      const data = await res.json();
      
      if (!data.result) {
        throw new Error("No response from AI. Please try again.");
      }

      setResult(data.result);
      
      // Save to history
      try {
        saveToHistory({
          symptoms: inputValue,
          result: data.result
        });
        toast.success("Analysis saved to history!");
      } catch (historyError) {
        console.error('Error saving to history:', historyError);
        toast.error('Analysis complete but failed to save to history');
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "Error analyzing symptoms. Please check if backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const clearInput = () => {
    setInputValue("");
    setResult("");
    setError("");
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: isDarkMode ? "radial-gradient(circle at center, #0a0f2c, #020617)" : "#F8F3E1",
      color: textPrimary,
      paddingTop: "60px",
      transition: "all 0.3s ease"
    }}>
      <div style={{
        maxWidth: "700px",
        margin: "auto",
        padding: "25px",
        background: bgSecondary,
        borderRadius: "16px",
        backdropFilter: "blur(10px)",
        border: `1px solid ${isDarkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
        transition: "all 0.3s ease"
      }}>
        <h2 style={{ fontSize: "28px", marginBottom: "10px", color: textPrimary }}>
          🩺 {translationFunc('symptom', 'title')}
        </h2>
        <p style={{ color: textMuted, marginBottom: "20px" }}>
          {translationFunc('symptom', 'subtitle')}
        </p>

        <label style={{ color: textMuted, fontSize: "14px", display: "block", marginBottom: "8px" }}>
          {translationFunc('symptom', 'desc')}
        </label>
        <textarea
          placeholder={translationFunc('symptom', 'ph')}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          style={{
            width: "100%",
            height: "120px",
            borderRadius: "10px",
            padding: "12px",
            border: `1px solid ${primaryColor}40`,
            outline: "none",
            marginBottom: "15px",
            background: isDarkMode ? "#1e293b" : "#FCFAF5",
            color: textPrimary,
            transition: "all 0.2s",
            fontSize: "14px"
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = primaryColor;
            e.currentTarget.style.boxShadow = `0 0 0 2px ${primaryColor}20`;
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = `${primaryColor}40`;
            e.currentTarget.style.boxShadow = "none";
          }}
        />

        {/* SYMPTOM CHIPS */}
        <div style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "10px",
          marginBottom: "20px"
        }}>
          {symptomsList.map((symptom, index) => (
            <button
              key={index}
              onClick={() => addSymptom(symptom)}
              style={{
                padding: "8px 12px",
                borderRadius: "20px",
                border: `1px solid ${primaryColor}60`,
                background: isDarkMode ? "#0f172a" : `${primaryColor}15`,
                color: primaryColor,
                cursor: "pointer",
                transition: "all 0.2s"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = `${primaryColor}25`;
                e.currentTarget.style.border = `1px solid ${primaryColor}`;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = isDarkMode ? "#0f172a" : `${primaryColor}15`;
                e.currentTarget.style.border = `1px solid ${primaryColor}60`;
              }}
            >
              {symptom}
            </button>
          ))}
        </div>

        {/* BUTTONS */}
        <div style={{ display: "flex", gap: "10px" }}>
          <button
            onClick={analyzeSymptoms}
            disabled={loading}
            style={{
              flex: 1,
              padding: "12px",
              borderRadius: "10px",
              border: "none",
              background: loading 
                ? "#666666" 
                : `linear-gradient(to right, ${primaryColor}, ${primaryColor}cc)`,
              color: "white",
              fontWeight: "bold",
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1,
              transition: "all 0.2s"
            }}
            onMouseEnter={(e) => {
              if (!loading) e.currentTarget.style.boxShadow = `0 0 15px ${primaryColor}60`;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = "none";
            }}
          >
            {loading ? `🔄 ${translationFunc('symptom', 'analyzing')}` : `🔍 ${translationFunc('symptom', 'analyze')}`}
          </button>

          <button
            onClick={clearInput}
            disabled={loading}
            style={{
              padding: "12px 20px",
              borderRadius: "10px",
              border: `1px solid ${primaryColor}40`,
              background: bgSecondary,
              color: textPrimary,
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1,
              transition: "all 0.2s"
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = `${primaryColor}15`;
              e.currentTarget.style.borderColor = primaryColor;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = bgSecondary;
              e.currentTarget.style.borderColor = `${primaryColor}40`;
            }}
          >
            {translationFunc('symptom', 'clear')}
          </button>
        </div>

        {/* ERROR MESSAGE */}
        {error && (
          <div style={{
            marginTop: "15px",
            padding: "12px",
            background: isDarkMode ? `${dangerColor}22` : `${dangerColor}15`,
            borderRadius: "8px",
            border: `1px solid ${dangerColor}50`,
            color: isDarkMode ? "#fecaca" : dangerColor
          }}>
            ⚠️ {error}
          </div>
        )}

        {/* RESULT - CLASSICAL HIGHLIGHTED UI */}
        {result && (
          <div style={{
            marginTop: "25px",
            display: "flex",
            flexDirection: "column",
            gap: "16px"
          }}>
            {/* Main Title */}
            <div style={{
              padding: "16px",
              background: `linear-gradient(135deg, ${primaryColor}22, ${successColor}11)`,
              border: `2px solid ${primaryColor}`,
              borderRadius: "12px",
              textAlign: "center"
            }}>
              <h3 style={{ 
                color: primaryColor, 
                margin: "0",
                fontSize: "20px",
                fontWeight: "bold"
              }}>
                📊 AI Analysis Results
              </h3>
            </div>

            {/* Parse and Display Sections */}
            {(() => {
              const sections = {
                'Possible Conditions': { color: primaryColor, bgColor: `${primaryColor}15`, borderColor: primaryColor, icon: '🔍' },
                'What To Do': { color: successColor, bgColor: `${successColor}15`, borderColor: successColor, icon: '✅' },
                'Home Remedies': { color: warningColor, bgColor: `${warningColor}15`, borderColor: warningColor, icon: '🏠' },
                'When To See Doctor': { color: dangerColor, bgColor: `${dangerColor}15`, borderColor: dangerColor, icon: '⚠️' }
              };

              const lines = result.split('\n');
              const sectionDivs = [];
              let currentSection = null;
              let currentContent = [];

              for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                const trimmed = line.trim();

                // Check if this is a section header
                let foundSection = false;
                for (const [sectionName, config] of Object.entries(sections)) {
                  if (trimmed.includes(sectionName) || line.includes(sectionName)) {
                    if (currentSection && currentContent.length > 0) {
                      sectionDivs.push(
                        <SectionBox 
                          key={`section-${sectionDivs.length}`}
                          title={currentSection.name}
                          content={currentContent}
                          config={currentSection.config}
                          textPrimary={textPrimary}
                          textMuted={textMuted}
                        />
                      );
                    }
                    currentSection = { name: sectionName, config };
                    currentContent = [];
                    foundSection = true;
                    break;
                  }
                }

                if (!foundSection && currentSection) {
                  if (trimmed && !trimmed.startsWith('##')) {
                    currentContent.push(line);
                  }
                }
              }

              // Add the last section
              if (currentSection && currentContent.length > 0) {
                sectionDivs.push(
                  <SectionBox 
                    key={`section-${sectionDivs.length}`}
                    title={currentSection.name}
                    content={currentContent}
                    config={currentSection.config}
                    textPrimary={textPrimary}
                    textMuted={textMuted}
                  />
                );
              }

              return sectionDivs;
            })()}

            {/* Warning Footer */}
            <div style={{
              padding: "14px 16px",
              background: isDarkMode ? `${dangerColor}22` : `${dangerColor}15`,
              border: `2px solid ${dangerColor}`,
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              gap: "10px"
            }}>
              <span style={{ fontSize: "18px" }}>⚠️</span>
              <span style={{ color: isDarkMode ? "#fecaca" : dangerColor, fontSize: "12px", lineHeight: "1.5" }}>
                <strong>Medical Disclaimer:</strong> This analysis is for informational purposes only and is not a substitute for professional medical advice. Please consult a qualified healthcare professional for proper diagnosis and treatment.
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Helper component for rendering sections
function SectionBox({ title, content, config, textPrimary, textMuted }) {
  return (
    <div style={{
      background: config.bgColor,
      border: `2px solid ${config.borderColor}`,
      borderRadius: "10px",
      overflow: "hidden"
    }}>
      {/* Section Header */}
      <div style={{
        background: `linear-gradient(to right, ${config.borderColor}30, ${config.borderColor}10)`,
        padding: "12px 16px",
        borderBottom: `2px solid ${config.borderColor}`,
        display: "flex",
        alignItems: "center",
        gap: "8px"
      }}>
        <span style={{ fontSize: "18px" }}>{config.icon}</span>
        <h4 style={{
          color: config.color,
          margin: "0",
          fontSize: "16px",
          fontWeight: "bold",
          textTransform: "uppercase",
          letterSpacing: "0.5px"
        }}>
          {title}
        </h4>
      </div>

      {/* Section Content */}
      <div style={{ padding: "14px 16px" }}>
        {content.map((line, idx) => {
          const trimmed = line.trim();

          // Bullet points
          if (trimmed.startsWith('*')) {
            const text = trimmed.replace(/^\*+\s*/, '').trim();
            if (!text) return null;
            return (
              <div key={idx} style={{
                marginBottom: "10px",
                paddingLeft: "24px",
                position: "relative",
                color: textPrimary,
                lineHeight: "1.6"
              }}>
                <span style={{
                  position: "absolute",
                  left: "0",
                  color: config.color,
                  fontWeight: "bold",
                  fontSize: "16px"
                }}>●</span>
                {text}
              </div>
            );
          }

          // Number lists
          if (/^\d+\./.test(trimmed)) {
            const text = trimmed.replace(/^\d+\.\s*/, '').trim();
            if (!text) return null;
            return (
              <div key={idx} style={{
                marginBottom: "10px",
                paddingLeft: "24px",
                position: "relative",
                color: textPrimary,
                lineHeight: "1.6"
              }}>
                <span style={{
                  position: "absolute",
                  left: "0",
                  color: config.color,
                  fontWeight: "bold",
                  fontSize: "14px"
                }}>→</span>
                {text}
              </div>
            );
          }

          // Regular text
          if (trimmed) {
            return (
              <div key={idx} style={{
                marginBottom: "8px",
                color: textPrimary,
                lineHeight: "1.6"
              }}>
                {trimmed}
              </div>
            );
          }

          return null;
        })}
      </div>
    </div>
  );
}