from flask import Blueprint, request, jsonify
from utils.db import fetch_one, fetch_all, execute
from utils.auth import protected, current_user_id
from utils.default_friends import synthetic_friend_locations

locations_bp=Blueprint("locations",__name__)

@locations_bp.get("")
@protected
def get_location():
    row=fetch_one("""SELECT l.latitude,l.longitude,l.updated_at
                     FROM locations l
                     JOIN location_sharing s ON s.user_id=l.user_id
                     WHERE l.user_id=%s AND s.enabled=TRUE""",(current_user_id(),))
    return jsonify(row or {})

@locations_bp.post("/sharing")
@protected
def sharing():
    enabled=bool((request.get_json() or {}).get("enabled"))
    uid=current_user_id()
    execute("""INSERT INTO location_sharing(user_id,enabled)
               VALUES(%s,%s)
               ON CONFLICT(user_id) DO UPDATE SET enabled=EXCLUDED.enabled,
               updated_at=CURRENT_TIMESTAMP""",(uid,enabled))
    if not enabled:
        execute("DELETE FROM locations WHERE user_id=%s",(uid,))
    return jsonify({"enabled":enabled})

@locations_bp.post("")
@protected
def update_location():
    uid=current_user_id()
    if not fetch_one("SELECT 1 FROM location_sharing WHERE user_id=%s AND enabled=TRUE",(uid,)):
        return jsonify({"error":"Enable location sharing first"}),403
    data=request.get_json() or {}
    try:
        lat=float(data["latitude"]); lon=float(data["longitude"])
        if not (-90<=lat<=90 and -180<=lon<=180): raise ValueError
    except:
        return jsonify({"error":"Valid latitude and longitude are required"}),400
    execute("""INSERT INTO locations(user_id,latitude,longitude)
               VALUES(%s,%s,%s)
               ON CONFLICT(user_id) DO UPDATE SET latitude=EXCLUDED.latitude,
               longitude=EXCLUDED.longitude,updated_at=CURRENT_TIMESTAMP""",(uid,lat,lon))
    return jsonify({"message":"Location updated"})

@locations_bp.get("/friends")
@protected
def friend_locations():
    uid=current_user_id()
    rows=fetch_all("""SELECT u.id,u.name,l.latitude,l.longitude,l.updated_at
                                FROM users u
                                JOIN friendships f ON f.status='accepted'
                                  AND ((f.sender_id=%s AND f.receiver_id=u.id)
                                    OR (f.receiver_id=%s AND f.sender_id=u.id))
                                JOIN location_sharing s ON s.user_id=u.id AND s.enabled=TRUE
                                JOIN locations l ON l.user_id=u.id""",(uid,uid))
    me=fetch_one("SELECT latitude,longitude FROM locations WHERE user_id=%s",(uid,))
    if me:
        rows=list(rows)+synthetic_friend_locations(float(me["latitude"]),float(me["longitude"]))
    return jsonify(rows)