// /frontend/static/js/main.js
// Core client interactions for Neural Health Link (Mock Demo)

document.addEventListener("DOMContentLoaded", () => {
  const themeKey = "nhl-theme";
  const toggleBtn = document.querySelector("#themeToggle");
  const patientSelect = document.querySelector("#patientSelect");

  // === Theme toggler ===
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme || "light";
      const next = current === "light" ? "dark" : "light";
      document.documentElement.dataset.theme = next;
      localStorage.setItem(themeKey, next);
      applyTheme(next);
    });
  }

  const saved = localStorage.getItem(themeKey) || "light";
  document.documentElement.dataset.theme = saved;
  applyTheme(saved);

  function applyTheme(theme) {
    const root = document.documentElement;
    if (theme === "dark") {
      root.style.setProperty("--bg", "#0b0f18");
      root.style.setProperty("--text", "#e6eef8");
    } else {
      root.style.setProperty("--bg", "#e9f0ff");
      root.style.setProperty("--text", "#0a0a0a");
    }
  }

  // === Patient selection redirect ===
  if (patientSelect) {
    patientSelect.addEventListener("change", (e) => {
      const id = e.target.value;
      if (id) window.location.href = `/patient/${id}`;
    });
  }

  // === Chart auto glow ===
  const chartCanvas = document.querySelector("#relationChart");
  if (chartCanvas) {
    chartCanvas.addEventListener("mousemove", (e) => {
      const x = e.offsetX / chartCanvas.clientWidth;
      const y = e.offsetY / chartCanvas.clientHeight;
      chartCanvas.style.boxShadow = `0 0 25px 4px rgba(125,249,255,${0.3 + 0.2 * y})`;
    });
    chartCanvas.addEventListener("mouseleave", () => {
      chartCanvas.style.boxShadow = "0 6px 20px rgba(0,0,0,0.4)";
    });
  }

  // === Neon pulse header ===
  const neonBar = document.querySelector(".neon-bar");
  if (neonBar) {
    let hue = 180;
    setInterval(() => {
      hue = (hue + 1) % 360;
      neonBar.style.background = `linear-gradient(90deg, hsl(${hue},100%,60%), hsl(${(hue+60)%360},100%,60%))`;
      neonBar.style.boxShadow = `0 0 12px hsl(${hue},100%,60%), 0 0 22px hsl(${(hue+60)%360},100%,60%)`;
    }, 50);
  }
});
