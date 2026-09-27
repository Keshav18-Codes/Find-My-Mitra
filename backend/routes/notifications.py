from flask import Blueprint, jsonify
from utils.db import fetch_all, execute
from utils.auth import protected, current_user_id

notifications_bp=Blueprint("notifications",__name__)

@notifications_bp.get("")
@protected
def notifications():
    return jsonify(fetch_all("""SELECT id,type,message,is_read,created_at
                                FROM notifications WHERE user_id=%s
                                ORDER BY created_at DESC LIMIT 50""",(current_user_id(),)))

@notifications_bp.put("/<int:nid>/read")
@protected
def read(nid):
    execute("UPDATE notifications SET is_read=TRUE WHERE id=%s AND user_id=%s",
            (nid,current_user_id()))
    return jsonify({"message":"Notification marked read"})
