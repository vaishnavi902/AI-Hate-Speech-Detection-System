from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_text
import json
import os

app = Flask(__name__)
CORS(app)

FILE = "history.json"

# Save data
def save_data(entry):
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)

    with open(FILE, "r") as f:
        data = json.load(f)

    data.append(entry)

    with open(FILE, "w") as f:
        json.dump(data, f)

# Get history
def get_history():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)

@app.route('/predict-text', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']

    result = predict_text(text)

    save_data({
        "text": text,
        "result": result
    })

    return jsonify({"result": result})


@app.route('/history', methods=['GET'])
def history():
    return jsonify(get_history())


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data['message'].lower()

    if "hate" in message:
        reply = "Hate speech includes abusive or offensive language targeting a group."
    elif "why" in message:
        reply = "The system detects harmful keywords and patterns using AI model."
    elif "hello" in message:
        reply = "Hello! How can I help you?"
    else:
        reply = "I am here to help you understand the result."

    return jsonify({"reply": reply})

import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))