from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def protected(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as exc:
            return jsonify({"error": "Authentication required", "detail": str(exc)}), 401
    return wrapper

def current_user_id():
    return int(get_jwt_identity())
