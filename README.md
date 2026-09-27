# Find My Friend

College project using HTML5, CSS3, Vanilla JavaScript, Python Flask, PostgreSQL, Leaflet/OpenStreetMap and Flask-SocketIO.

## Requirements
- Python 3.10+
- PostgreSQL 14+
- A modern browser

## Database
1. Create a PostgreSQL database named `find_my_friend`.
2. Connect to it and run `backend/database/schema.sql` after removing the first `CREATE DATABASE` line if the database already exists.
3. Copy `backend/.env.example` to `backend/.env`.
4. Update `DATABASE_URL` and `JWT_SECRET`.

## Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Backend runs on http://localhost:5000

## Frontend
Because the frontend is static HTML/JS, serve it from a local web server:

```bash
cd frontend
python -m http.server 5500
```

Open http://localhost:5500

## API Overview
- `POST /api/auth/register` – create an account
- `POST /api/auth/login` – log in, returns a JWT + user info
- `POST /api/auth/logout` – logout (client discards the token)
- `GET /api/auth/me` – current logged-in user
- `GET /api/users/search?q=` – search users by name/email
- `GET /api/users/profile` / `PUT /api/users/profile` – view/update profile
- `PUT /api/users/password` – change password
- `GET /api/friends` – list accepted friends
- `GET /api/friends/requests` – list incoming pending requests
- `POST /api/friends/request` – send a friend request
- `PUT /api/friends/request/<id>` – accept/reject (`{"action":"accepted"|"rejected"}`)
- `DELETE /api/friends/<id>` – remove a friendship
- `GET /api/location` / `POST /api/location` – get/update your own location
- `GET /api/location/friends` – locations of friends currently sharing
- `POST /api/location/sharing` – turn sharing on/off
- `GET /api/notifications` / `PUT /api/notifications/<id>/read`
- `POST /api/sos` – send an SOS alert to accepted friends
- `GET /api/sos` – your SOS history
- `GET /api/health` – health check

## Testing the app
1. **Register/Login**: open `register.html`, create two different accounts (use two browsers or an incognito window for the second), then log in with each.
2. **Friend requests**: from account A, go to Friends → search for account B by name/email → Add Friend. Log into account B → Friends → accept the request under "Friend Requests".
3. **Location sharing**: on the Dashboard, click "Enable Location Sharing" and allow the browser's location permission prompt. Open `map.html` on the other friend's account (once they've also enabled sharing) to see the marker appear.
4. **SOS**: go to the SOS page, click the button, confirm the prompt, and check the other account's Notifications page for the alert.

## Notes
- Browser geolocation generally works on localhost or HTTPS.
- Location sharing is opt-in.
- `backend/database/seed.sql` is provided as an optional starting point, but its sample password hashes are placeholders — register real accounts through the app to test properly.
- This is a college-project starter implementation; production deployment should add HTTPS, stricter CORS, CSRF strategy where applicable, rate limiting, secure cookie/token strategy, audit logging and stronger permission controls.
