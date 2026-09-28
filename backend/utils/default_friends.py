import math
import secrets
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from utils.db import fetch_one, execute

EARTH_RADIUS_M = 6378137

DEFAULT_FRIENDS = [
    {"email": "manjiri.deshpande@fmfriend.local", "name": "Manjiri Deshpande", "distance_m": 500, "bearing_deg": 45},
    {"email": "bharati.parmar@fmfriend.local",     "name": "Bharati Parmar",     "distance_m": 800, "bearing_deg": 200},
]

def _get_or_create_default_user(entry):
    row = fetch_one("SELECT id FROM users WHERE email=%s", (entry["email"],))
    if row:
        return row["id"]
    row = fetch_one(
        """INSERT INTO users(name,email,password_hash,bio)
           VALUES(%s,%s,%s,%s) RETURNING id""",
        (entry["name"], entry["email"], generate_password_hash(secrets.token_hex(16)), "Demo friend")
    )
    return row["id"]

def ensure_default_friends(user_id):
    """Make sure the fixed demo friends exist and are accepted friends of user_id."""
    for entry in DEFAULT_FRIENDS:
        default_id = _get_or_create_default_user(entry)
        if default_id == user_id:
            continue
        existing = fetch_one(
            """SELECT id FROM friendships
               WHERE (sender_id=%s AND receiver_id=%s) OR (sender_id=%s AND receiver_id=%s)""",
            (user_id, default_id, default_id, user_id)
        )
        if not existing:
            execute(
                "INSERT INTO friendships(sender_id,receiver_id,status) VALUES(%s,%s,'accepted')",
                (user_id, default_id)
            )

def _offset_point(lat, lon, distance_m, bearing_deg):
    bearing = math.radians(bearing_deg)
    lat1, lon1 = math.radians(lat), math.radians(lon)
    ang = distance_m / EARTH_RADIUS_M
    lat2 = math.asin(math.sin(lat1)*math.cos(ang) + math.cos(lat1)*math.sin(ang)*math.cos(bearing))
    lon2 = lon1 + math.atan2(
        math.sin(bearing)*math.sin(ang)*math.cos(lat1),
        math.cos(ang) - math.sin(lat1)*math.sin(lat2)
    )
    return math.degrees(lat2), math.degrees(lon2)

def synthetic_friend_locations(my_lat, my_lon):
    now = datetime.now(timezone.utc).isoformat()
    out = []
    for entry in DEFAULT_FRIENDS:
        row = fetch_one("SELECT id FROM users WHERE email=%s", (entry["email"],))
        lat, lon = _offset_point(my_lat, my_lon, entry["distance_m"], entry["bearing_deg"])
        out.append({"id": row["id"] if row else None, "name": entry["name"],
                    "latitude": round(lat, 7), "longitude": round(lon, 7), "updated_at": now})
    return out