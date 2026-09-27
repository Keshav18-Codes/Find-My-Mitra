const API = "http://localhost:5000/api";
const T = localStorage.getItem("token");
if (!T) location.href = "login.html";
const H = { Authorization: "Bearer " + T, "Content-Type": "application/json" };

fetch(API + "/users/profile", { headers: H })
  .then(r => r.json())
  .then(u => { name.value = u.name; email.value = u.email; bio.value = u.bio || ""; });

profile.onsubmit = async e => {
  e.preventDefault();
  const r = await fetch(API + "/users/profile", {
    method: "PUT",
    headers: H,
    body: JSON.stringify({ name: name.value, bio: bio.value })
  });
  const d = await r.json();
  msg.textContent = d.message || d.error;
};

passwordForm.onsubmit = async e => {
  e.preventDefault();
  pwMsg.textContent = "Updating...";
  const r = await fetch(API + "/users/password", {
    method: "PUT",
    headers: H,
    body: JSON.stringify({
      current_password: currentPassword.value,
      new_password: newPassword.value
    })
  });
  const d = await r.json();
  pwMsg.textContent = d.message || d.error;
  if (r.ok) passwordForm.reset();
};
