const API = "http://localhost:5000/api";
const t = localStorage.getItem("token");
if (!t) 
    location.href = "login.html";
const H = {
    Authorization: "Bearer " + t,
    "Content-Type": "application/json"
};
const get = p => fetch(API + p, {headers: H}).then(async r => {
    const d = await r.json();
    if (!r.ok) 
        throw Error(d.error);
    return d
});
const user = JSON.parse(localStorage.getItem("user") || "{}");
welcome.textContent = "Welcome, " + (
    user.name || "Friend"
) + " 👋";
async function load() {
    try {
        const f = await get("/friends");
        friendCount.textContent = f.length + " friend" + (
            f.length === 1
                ? ""
                : "s"
        );
        const p = await get("/location");
        sharing.textContent = p.updated_at
            ? "Location sharing is active"
            : "Location sharing is off";
        toggle.textContent = p.updated_at
            ? "Disable Location Sharing"
            : "Enable Location Sharing"
    } catch (e) {
        sharing.textContent = e.message
    }
}
function getPosition() {
  return new Promise((res, rej) =>
    navigator.geolocation.getCurrentPosition(res, rej, { enableHighAccuracy: true, timeout: 15000 }));
}
async function post(path, body) {
  const r = await fetch(API + path, { method: "POST", headers: H, body: JSON.stringify(body) });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.error || "Request failed");
  return d;
}

toggle.onclick = async () => {
  const turningOn = !toggle.textContent.startsWith("Disable");
  setLoading(toggle, true, turningOn ? "Getting your location…" : "Turning off…");
  sharing.textContent = turningOn ? "Waiting for your browser's location…" : "Turning off location sharing…";
  let ok = false;
  try {
    if (turningOn) {
      const pos = await getPosition();
      sharing.textContent = "Saving your location…";
      await post("/location/sharing", { enabled: true });
      await post("/location", { latitude: pos.coords.latitude, longitude: pos.coords.longitude });
    } else {
      await post("/location/sharing", { enabled: false });
    }
    ok = true;
  } catch (e) {
    sharing.textContent = e.code === 1
      ? "Location permission is blocked. Allow it in your browser's site settings."
      : e.code === 3 ? "Timed out getting your location. Try again." : e.message;
  }
  setLoading(toggle, false);
  if (ok) load();
};

logout.onclick = async () => {
  setLoading(logout, true, "Logging out…");
  try { await fetch(API + "/auth/logout", { method: "POST", headers: H }); } catch {}
  await new Promise(r => setTimeout(r, 400));   // lets the message show briefly
  localStorage.clear();
  location.href = "index.html";
};
load();
