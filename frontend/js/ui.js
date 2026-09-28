function setLoading(btn, on, text) {
  if (on) {
    if (btn.classList.contains("loading")) return;
    btn.dataset.label = btn.textContent;
    btn.innerHTML = '<span class="spinner"></span>' + (text || "Loading…");
    btn.disabled = true;
    btn.classList.add("loading");
    btn.setAttribute("aria-busy", "true");
  } else {
    btn.textContent = btn.dataset.label || btn.textContent;
    btn.disabled = false;
    btn.classList.remove("loading");
    btn.removeAttribute("aria-busy");
  }
}