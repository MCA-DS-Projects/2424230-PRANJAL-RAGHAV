from flask import Blueprint, request, jsonify
from groq import Groq
import os

chat_bp = Blueprint("chat", __name__, url_prefix="/api")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    prompt = f"""
You are Nutra Expert AI — a friendly health and nutrition assistant.
Reply ONLY in English.
Give short, practical, science-backed guidance related to diet, health, fitness, lifestyle, and wellness.
Avoid Hindi or Hinglish words completely.
Keep responses under 50 words.

User: {user_msg}
"""



    try:
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = r.choices[0].message.content
        return jsonify({"reply": reply}), 200

    except Exception as e:
        print("Chat Error:", e)
        return jsonify({"error": "AI Server Error"}), 500
