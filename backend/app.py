import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "dev-secret-change-me")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
CORS(app, resources={r"/api/*": {"origins": "*"}})
JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

from routes.auth import auth_bp
from routes.users import users_bp
from routes.friends import friends_bp
from routes.locations import locations_bp
from routes.notifications import notifications_bp
from routes.sos import sos_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(friends_bp, url_prefix="/api/friends")
app.register_blueprint(locations_bp, url_prefix="/api/location")
app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
app.register_blueprint(sos_bp, url_prefix="/api/sos")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Find My Friend API"}

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
