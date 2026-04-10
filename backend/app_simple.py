from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        symptoms = request.json.get("symptoms")

        prompt = f"""
You are a professional AI Health Assistant.

Patient symptoms: {symptoms}

Analyze carefully and respond with:

1. Possible Causes (max 3)
2. What the user should do now
3. Home remedies (if safe)
4. When to see a doctor

Rules:
- Be concise and helpful
- Do NOT repeat symptoms
- Use simple language
- Give a different response each time

Keep response under 6 lines.
"""

        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.9,
                "top_p": 0.9,
                "repeat_penalty": 1.2
            }
        }

        res = requests.post("http://localhost:11434/api/generate", json=payload)

        data = res.json()
        reply = data.get("response", "No response")

        return jsonify({"result": reply})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
