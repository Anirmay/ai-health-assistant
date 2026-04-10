import { useNavigate, useLocation } from 'react-router-dom';
import { useContext } from 'react';
import { LanguageContext, ThemeContext } from '../App';

export default function ResultPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const result = location.state?.result || '';
  const symptoms = location.state?.symptoms || '';
  const { t } = useContext(LanguageContext);

  if (!result) {
    return (
      <div style={{
        minHeight: "100vh",
        background: "radial-gradient(circle at center, #0a0f2c, #020617)",
        color: "white",
        paddingTop: "60px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      }}>
        <div style={{
          maxWidth: "700px",
          margin: "auto",
          padding: "25px",
          background: "rgba(255,255,255,0.05)",
          borderRadius: "16px",
          backdropFilter: "blur(10px)",
          textAlign: "center"
        }}>
          <h2 style={{ fontSize: "24px", marginBottom: "20px" }}>⚠️ No Results</h2>
          <p style={{ color: "#aaa", marginBottom: "20px" }}>
            No analysis results found. Please go back and analyze symptoms first.
          </p>
          <button
            onClick={() => navigate('/')}
            style={{
              padding: "12px 24px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(to right, #06b6d4, #3b82f6)",
              color: "white",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            ← Back to Analyzer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: "radial-gradient(circle at center, #0a0f2c, #020617)",
      color: "white",
      paddingTop: "60px"
    }}>
      <div style={{
        maxWidth: "800px",
        margin: "auto",
        padding: "25px"
      }}>
        {/* Back Button */}
        <button
          onClick={() => navigate('/')}
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "1px solid #334155",
            background: "#0f172a",
            color: "#cbd5f5",
            cursor: "pointer",
            marginBottom: "20px",
            fontSize: "14px"
          }}
        >
          ← Back to Analyzer
        </button>

        {/* Header */}
        <div style={{
          background: "rgba(255,255,255,0.05)",
          borderRadius: "16px",
          backdropFilter: "blur(10px)",
          padding: "25px",
          marginBottom: "20px",
          border: "1px solid #1e293b"
        }}>
          <h1 style={{ fontSize: "32px", marginBottom: "10px" }}>
            🩺 Analysis Results
          </h1>
          <p style={{ color: "#aaa", marginBottom: "15px" }}>
            Based on your symptoms
          </p>
          
          {/* Symptoms Summary */}
          {symptoms && (
            <div style={{
              background: "#1e293b",
              padding: "12px",
              borderRadius: "8px",
              marginTop: "15px"
            }}>
              <p style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "5px" }}>
                YOUR SYMPTOMS:
              </p>
              <p style={{ color: "#e2e8f0" }}>
                {symptoms}
              </p>
            </div>
          )}
        </div>

        {/* Result Card */}
        <div style={{
          background: "rgba(255,255,255,0.05)",
          borderRadius: "16px",
          backdropFilter: "blur(10px)",
          padding: "25px",
          border: "1px solid #1e293b",
          borderLeft: "4px solid #06b6d4"
        }}>
          <h2 style={{ fontSize: "20px", marginBottom: "15px", color: "#06b6d4" }}>
            📋 AI Analysis
          </h2>
          
          <div style={{
            background: "#020617",
            padding: "15px",
            borderRadius: "10px",
            border: "1px solid #1e293b",
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
            lineHeight: "1.6",
            color: "#e2e8f0",
            fontFamily: "monospace",
            fontSize: "14px"
          }}>
            {result}
          </div>
        </div>

        {/* Important Disclaimer */}
        <div style={{
          background: "rgba(255,255,255,0.05)",
          borderRadius: "16px",
          backdropFilter: "blur(10px)",
          padding: "15px",
          marginTop: "20px",
          border: "1px solid #1e293b",
          borderLeft: "4px solid #fbbf24"
        }}>
          <p style={{
            color: "#fbbf24",
            fontSize: "12px",
            margin: 0
          }}>
            ⚠️ <strong>Important:</strong> This is not a medical diagnosis. Always consult a healthcare professional for proper diagnosis and treatment.
          </p>
        </div>

        {/* Action Buttons */}
        <div style={{
          display: "flex",
          gap: "10px",
          marginTop: "20px"
        }}>
          <button
            onClick={() => navigate('/')}
            style={{
              flex: 1,
              padding: "12px",
              borderRadius: "10px",
              border: "none",
              background: "linear-gradient(to right, #06b6d4, #3b82f6)",
              color: "white",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            🔄 Analyze Again
          </button>
          
          <button
            onClick={() => {
              const text = `Symptoms: ${symptoms}\n\nAnalysis:\n${result}`;
              const element = document.createElement('a');
              element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
              element.setAttribute('download', 'health-analysis.txt');
              element.style.display = 'none';
              document.body.appendChild(element);
              element.click();
              document.body.removeChild(element);
            }}
            style={{
              padding: "12px 20px",
              borderRadius: "10px",
              border: "1px solid #334155",
              background: "#0f172a",
              color: "#cbd5f5",
              cursor: "pointer",
              fontWeight: "bold"
            }}
          >
            💾 Download
          </button>
        </div>
      </div>
    </div>
  );
}
