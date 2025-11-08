from flask import Blueprint, request, jsonify
from groq import Groq
import os

chat_bp = Blueprint("chat", __name__, url_prefix="/api")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message","")

    prompt = f"""
You are Nutra Expert AI — Ayurvedic Master Nutrition Coach.
Reply short, practical and in Hinglish.
Max 50 words.

User: {user_msg}
"""

    r = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"reply": r.choices[0].message.content})
