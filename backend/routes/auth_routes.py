
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from backend.db import users_collection
from backend.models.user_model import serialize_user
import os

# Initialize Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/api")
bcrypt = Bcrypt()
mail = Mail()

# === Initialize Mail and Serializer ===
def init_mail(app):
    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "True").lower() == "true",
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    )
    mail.init_app(app)

serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

# ======================
# ✅ USER REGISTRATION
# ======================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    email = data.get("email")
    password = data.get("password")
    fullName = data.get("fullName")
    phone = data.get("phone", "")
    healthGoals = data.get("healthGoals", [])

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = {
        "fullName": fullName,
        "email": email,
        "password": hashed_pw,
        "phone": phone,
        "healthGoals": healthGoals,
    }

    users_collection.insert_one(new_user)

    # Send welcome email
    try:
        msg = Message(
            subject="🎉 Welcome to Nutra Expert AI!",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email],
            body=f"Hi {fullName},\n\nWelcome to Nutra Expert AI! Your account has been successfully created."
        )
        mail.send(msg)
    except Exception as e:
        print("📧 Email Error:", e)

    return jsonify({"message": "Account created successfully"}), 201

# ======================
# ✅ USER LOGIN
# ======================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user": serialize_user(user)}), 200

# ======================
# 📨 FORGOT PASSWORD — send email link
# ======================
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "No account found with this email"}), 404

    token = serializer.dumps(email, salt="password-reset-salt")
    # reset_link = f"{os.getenv('FRONTEND_URL')}/reset_password.html?token={token}"
    reset_link = f"{os.getenv('FRONTEND_URL')}/reset_password/?token={token}"


    try:
        msg = Message(
            subject="🔑 Reset Your Nutra Expert AI Password",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email],
            body=f"Hi {user['fullName']},\n\nClick the link below to reset your password:\n{reset_link}\n\nThis link expires in 15 minutes."
        )
        mail.send(msg)
        print(f"📨 Sent reset link to: {email}")
        return jsonify({"message": "Reset link sent to your email."}), 200
    except Exception as e:
        print("Mail error:", e)
        return jsonify({"error": "Failed to send reset email"}), 500

# ======================
# 🔒 RESET PASSWORD (API)
# ======================
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        token = data.get("token")
        new_password = data.get("newPassword")

        if not token or not new_password:
            return jsonify({"error": "Token or new password missing"}), 400

        # Decode token
        try:
            email = serializer.loads(token, salt="password-reset-salt", max_age=900)
        except SignatureExpired:
            return jsonify({"error": "Reset link expired"}), 400
        except BadSignature:
            return jsonify({"error": "Invalid reset token"}), 400

        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"error": "User not found"}), 404

        hashed_pw = bcrypt.generate_password_hash(new_password).decode("utf-8")
        users_collection.update_one(
            {"email": email},
            {"$set": {"password": hashed_pw, "lastPasswordReset": "Just Now ✅"}}
        )

        print(f"✅ Password updated successfully for: {email}")
        return jsonify({"message": "Password reset successful"}), 200

    except Exception as e:
        print("🔥 Reset Password Error:", str(e))
        return jsonify({"error": "Server error while resetting password"}), 500
