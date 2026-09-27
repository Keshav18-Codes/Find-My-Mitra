from flask import Blueprint, request, jsonify
from utils.db import fetch_one, fetch_all, execute
from utils.auth import protected, current_user_id

friends_bp = Blueprint("friends", __name__)

@friends_bp.get("")
@protected
def friends():
    uid = current_user_id()
    rows = fetch_all("""SELECT u.id,u.name,u.email,u.profile_image,
                               COALESCE(ls.enabled,FALSE) AS location_sharing
                        FROM users u
                        JOIN friendships f ON
                          ((f.sender_id=%s AND f.receiver_id=u.id) OR
                           (f.receiver_id=%s AND f.sender_id=u.id))
                        LEFT JOIN location_sharing ls ON ls.user_id=u.id
                        WHERE f.status='accepted'""", (uid, uid))
    return jsonify(rows)

@friends_bp.post("/request")
@protected
def send_request():
    uid = current_user_id()
    rid = (request.get_json() or {}).get("receiver_id")
    try: rid = int(rid)
    except: return jsonify({"error":"receiver_id is required"}),400
    if rid == uid or not fetch_one("SELECT id FROM users WHERE id=%s", (rid,)):
        return jsonify({"error":"Invalid user"}),400
    existing = fetch_one("""SELECT id,status FROM friendships
                            WHERE (sender_id=%s AND receiver_id=%s)
                               OR (sender_id=%s AND receiver_id=%s)""",
                         (uid,rid,rid,uid))
    if existing:
        return jsonify({"error":"Friend request or friendship already exists"}),409
    execute("INSERT INTO friendships(sender_id,receiver_id,status) VALUES(%s,%s,'pending')",
            (uid,rid))
    execute("""INSERT INTO notifications(user_id,type,message)
               VALUES(%s,'friend_request','You received a new friend request')""",(rid,))
    return jsonify({"message":"Friend request sent"}),201

@friends_bp.get("/requests")
@protected
def requests():
    uid=current_user_id()
    return jsonify(fetch_all("""SELECT f.id,u.id AS sender_id,u.name,u.email
                                FROM friendships f JOIN users u ON u.id=f.sender_id
                                WHERE f.receiver_id=%s AND f.status='pending'
                                ORDER BY f.created_at DESC""",(uid,)))

@friends_bp.put("/request/<int:fid>")
@protected
def respond(fid):
    uid=current_user_id()
    action=(request.get_json() or {}).get("action")
    if action not in ("accepted","rejected"):
        return jsonify({"error":"action must be accepted or rejected"}),400
    row=fetch_one("""SELECT sender_id FROM friendships
                     WHERE id=%s AND receiver_id=%s AND status='pending'""",(fid,uid))
    if not row: return jsonify({"error":"Request not found"}),404
    execute("UPDATE friendships SET status=%s WHERE id=%s",(action,fid))
    if action=="accepted":
        execute("""INSERT INTO notifications(user_id,type,message)
                   VALUES(%s,'friend_accepted','Your friend request was accepted')""",
                (row["sender_id"],))
    return jsonify({"message":f"Request {action}"})

@friends_bp.delete("/<int:fid>")
@protected
def remove(fid):
    uid=current_user_id()
    execute("""DELETE FROM friendships
               WHERE id=%s AND (sender_id=%s OR receiver_id=%s)""",(fid,uid,uid))
    return jsonify({"message":"Friendship removed"})
