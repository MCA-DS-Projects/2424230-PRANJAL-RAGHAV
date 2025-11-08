
# from flask import Flask
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_pymongo import PyMongo
# from dotenv import load_dotenv
# from backend.routes.location_routes import location_bp
# from backend.routes.weather_routes import weather_bp
# from backend.routes.location_routes import location_bp
# from backend.routes.auth_routes import auth_bp, init_mail
# from backend.routes.chat_routes import chat_bp
# import os
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from dotenv import load_dotenv

from routes.location_routes import location_bp
from routes.weather_routes import weather_bp
from routes.auth_routes import auth_bp, init_mail
from routes.chat_routes import chat_bp

import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Enable full CORS for all routes (for development)
CORS(
    app,
    origins="*",
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
)

# Initialize extensions
bcrypt = Bcrypt(app)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Initialize Mail
init_mail(app)

# Register blueprints
app.register_blueprint(auth_bp)
# app.register_blueprint(location_bp)       
app.register_blueprint(weather_bp)   
app.register_blueprint(location_bp)
app.register_blueprint(chat_bp)
     
@app.route("/")
def home():
    return {"message": "✅ Nutra Expert AI Backend Running Successfully"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
