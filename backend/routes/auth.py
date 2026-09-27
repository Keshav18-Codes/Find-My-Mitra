from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import fetch_one, execute
from utils.auth import protected, current_user_id
from utils.default_friends import ensure_default_friends

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not name or not email or len(password) < 6:
        return jsonify({"error": "Name, valid email and password of at least 6 characters are required"}), 400
    if fetch_one("SELECT id FROM users WHERE email=%s", (email,)):
        return jsonify({"error": "Email already registered"}), 409
    row = fetch_one(
        """INSERT INTO users(name,email,password_hash) VALUES(%s,%s,%s)
           RETURNING id,name,email,created_at""",
        (name, email, generate_password_hash(password))
    )
    ensure_default_friends(row["id"])
    return jsonify({"message": "Registration successful", "user": row}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = fetch_one("SELECT * FROM users WHERE email=%s", (email,))
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401
    ensure_default_friends(user["id"])
    token = create_access_token(identity=str(user["id"]))
    return jsonify({"token": token, "user": {
        "id": user["id"], "name": user["name"], "email": user["email"]
    }})

@auth_bp.post("/logout")
@protected
def logout():
    return jsonify({"message": "Logged out successfully"})

@auth_bp.get("/me")
@protected
def me():
    user = fetch_one(
        "SELECT id, name, email, profile_image, bio, created_at FROM users WHERE id=%s",
        (current_user_id(),)
    )
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)