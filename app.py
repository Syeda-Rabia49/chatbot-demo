from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("knowledge.txt", "r") as f:
    knowledge = f.read()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Oakwood Essentials. Use this info: " + knowledge + " Rules: Keep answers short. Use clean bullet points on new lines. If the user makes a spelling mistake try to understand what they meant and answer anyway. Max 3 sentences or 4 bullet points."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=200
    )
    return jsonify({"reply": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True, port=5000)