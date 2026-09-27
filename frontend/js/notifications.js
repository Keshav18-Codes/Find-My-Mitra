const API = "http://localhost:5000/api";
const T = localStorage.getItem("token");
if (!T) location.href = "login.html";
const H = { Authorization: "Bearer " + T, "Content-Type": "application/json" };

function card(n) {
  const readClass = n.is_read ? "read" : "unread";
  const readBtn = n.is_read
    ? ""
    : `<button class="btn ghost small" data-id="${n.id}">Mark as read</button>`;
  return `<div class="card notif ${readClass}">
    <strong>${n.type.replace("_", " ")}</strong>
    <p>${n.message}</p>
    <small>${new Date(n.created_at).toLocaleString()}</small>
    ${readBtn}
  </div>`;
}

async function load() {
  const r = await fetch(API + "/notifications", { headers: H });
  const ns = await r.json();
  list.innerHTML = ns.map(card).join("") || "<p>No notifications.</p>";
  document.querySelectorAll("[data-id]").forEach(b => {
    b.onclick = async () => {
      await fetch(API + "/notifications/" + b.dataset.id + "/read", {
        method: "PUT",
        headers: H
      });
      load();
    };
  });
}

load();
