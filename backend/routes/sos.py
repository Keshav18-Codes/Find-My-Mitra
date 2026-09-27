from flask import Blueprint, request, jsonify
from utils.db import fetch_all, fetch_one, execute
from utils.auth import protected, current_user_id

sos_bp=Blueprint("sos",__name__)

@sos_bp.post("")
@protected
def create_sos():
    uid=current_user_id()
    data=request.get_json() or {}
    try:
        lat=float(data["latitude"]); lon=float(data["longitude"])
    except:
        return jsonify({"error":"Current location is required"}),400
    message=(data.get("message") or "Emergency SOS alert").strip()[:500]
    row=fetch_one("""INSERT INTO emergency_alerts(user_id,latitude,longitude,message)
                     VALUES(%s,%s,%s,%s) RETURNING id,created_at""",
                  (uid,lat,lon,message))
    friend_ids=fetch_all("""SELECT CASE WHEN sender_id=%s THEN receiver_id ELSE sender_id END AS id
                            FROM friendships
                            WHERE status='accepted' AND (sender_id=%s OR receiver_id=%s)""",
                         (uid,uid,uid))
    for f in friend_ids:
        execute("""INSERT INTO notifications(user_id,type,message)
                   VALUES(%s,'sos','Emergency SOS alert from your friend')""",(f["id"],))
    return jsonify({"message":"SOS sent","alert":row}),201

@sos_bp.get("")
@protected
def history():
    return jsonify(fetch_all("""SELECT id,latitude,longitude,message,created_at
                                FROM emergency_alerts WHERE user_id=%s
                                ORDER BY created_at DESC LIMIT 20""",(current_user_id(),)))
