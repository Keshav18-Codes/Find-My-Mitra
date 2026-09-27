from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import fetch_one, fetch_all, execute
from utils.auth import protected, current_user_id

users_bp = Blueprint("users", __name__)

@users_bp.get("/profile")
@protected
def profile():
    user = fetch_one("""SELECT id,name,email,profile_image,bio,created_at FROM users
                        WHERE id=%s""", (current_user_id(),))
    return jsonify(user)

@users_bp.put("/profile")
@protected
def update_profile():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    bio = data.get("bio", "")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    execute("UPDATE users SET name=%s,bio=%s WHERE id=%s",
            (name, bio, current_user_id()))
    return jsonify({"message": "Profile updated"})

@users_bp.put("/password")
@protected
def change_password():
    data = request.get_json() or {}
    current_password = data.get("current_password") or ""
    new_password = data.get("new_password") or ""
    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters"}), 400
    user = fetch_one("SELECT password_hash FROM users WHERE id=%s", (current_user_id(),))
    if not user or not check_password_hash(user["password_hash"], current_password):
        return jsonify({"error": "Current password is incorrect"}), 401
    execute("UPDATE users SET password_hash=%s WHERE id=%s",
            (generate_password_hash(new_password), current_user_id()))
    return jsonify({"message": "Password updated successfully"})

@users_bp.get("/search")
@protected
def search():
    q = (request.args.get("q") or "").strip()
    if len(q) < 2:
        return jsonify([])
    rows = fetch_all("""SELECT id,name,email,profile_image FROM users
                        WHERE id<>%s AND (name ILIKE %s OR email ILIKE %s)
                        ORDER BY name LIMIT 20""",
                     (current_user_id(), f"%{q}%", f"%{q}%"))
    return jsonify(rows)
