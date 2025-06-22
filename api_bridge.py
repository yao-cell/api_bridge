from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HF_TOKEN = "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"
MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

@app.route('/get_ai_advice', methods=['POST'])
def get_ai_advice():
    data = request.json
    label = data.get("label", "Unknown")
    prompt = (
        f"A user scanned a food labeled '{label}'.\n"
        "1. Is this healthy or unhealthy? Explain.\n"
        "2. Mention stroke risk (if any).\n"
        "3. Suggest healthier alternatives.\n"
        "4. Make all the answers short."
    )
    payload = {"inputs": prompt}
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        json=payload,
        headers=headers,
        timeout=60
    )
    try:
        result = resp.json()
        text = result[0].get("generated_text", "")
        return jsonify({"advice": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
