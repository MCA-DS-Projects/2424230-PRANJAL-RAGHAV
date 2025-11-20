from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from backend.routes.food_routes import food_bp
from backend.routes.location_routes import location_bp
from backend.routes.weather_routes import weather_bp
from backend.routes.auth_routes import auth_bp, init_mail
from backend.routes.chat_routes import chat_bp
from backend.routes.favorite_routes import favorites_bp
import os

# Load environment variables
load_dotenv()

# We will serve frontend manually
app = Flask(__name__, static_folder=None)

CORS(app,
     origins="*",
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-ADMIN-SECRET"],
     expose_headers=["Content-Type", "Authorization", "X-ADMIN-SECRET"]
)

# Initialize extensions
bcrypt = Bcrypt(app)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Initialize Mail
init_mail(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(location_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(food_bp)
app.register_blueprint(favorites_bp)


@app.route("/api/health")
def health():
    return {"message": "✅ Nutra Expert AI Backend Running Successfully"}


# static/frontend serving (adjust FRONTEND_FOLDER if needed)
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Serve index.html at root
@app.route("/", defaults={"path": "index.html"})
def index(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# Serve any file under /Pages/... (important)
@app.route("/Pages/<path:filename>")
def serve_pages(filename):
    pages_folder = os.path.join(FRONTEND_FOLDER, "Pages")
    return send_from_directory(pages_folder, filename)

# Serve other static files (css, js, images, public, etc.)
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)


if __name__ == "__main__":
    app.run(
        host="10.229.231.206",   # your machine IP
        port=5000,
        ssl_context="adhoc",     # remove this if you prefer http
        debug=True
    )
