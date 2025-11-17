// /frontend/static/js/main.js
// Core client interactions for Neural Health Link (Mock Demo)

document.addEventListener("DOMContentLoaded", () => {
  const themeKey = "nhl-theme";
  const toggleBtn = document.querySelector("#themeToggle");
  const patientSelect = document.querySelector("#patientSelect");
  const body = document.body;
  const currentLang = (body && body.getAttribute("data-lang")) || "en";

  // ================= THEME HANDLING =================
  // Two fully defined palettes so text never becomes unreadable.
  function applyTheme(theme) {
    const root = document.documentElement;

    if (theme === "dark") {
      root.style.setProperty("--bg", "#050813");            // very dark background
      root.style.setProperty("--panel", "#151b2cdd");       // lighter than bg (cards)
      root.style.setProperty("--stroke", "#243656");        // grid / borders
      root.style.setProperty("--neon", "#7df9ff");          // cyan accent
      root.style.setProperty("--neon-2", "#a78bfa");        // violet accent
      root.style.setProperty("--text", "#e6eef8");          // main text
      root.style.setProperty("--muted", "#9fb0cf");         // secondary text
      root.style.setProperty("--success", "#30e0a1");
      root.style.setProperty("--warning", "#ffd166");
      root.style.setProperty("--danger", "#ff5d73");
    } else {
      // Light theme: soft clinic-style UI, still with neon accents
      root.style.setProperty("--bg", "#e9f0ff");
      root.style.setProperty("--panel", "#ffffffee");
      root.style.setProperty("--stroke", "#ccd5f0");
      root.style.setProperty("--neon", "#1f9cff");
      root.style.setProperty("--neon-2", "#8b5cf6");
      root.style.setProperty("--text", "#0a0a0a");
      root.style.setProperty("--muted", "#55627a");
      root.style.setProperty("--success", "#16a34a");
      root.style.setProperty("--warning", "#d97706");
      root.style.setProperty("--danger", "#dc2626");
    }

    document.documentElement.dataset.theme = theme;
  }

  // Initial theme: from localStorage or default to LIGHT
  const savedTheme = localStorage.getItem(themeKey) || "light";
  applyTheme(savedTheme);

  // Theme toggle button (if present in navbar)
  if (toggleBtn) {
    toggleBtn.textContent = savedTheme === "dark" ? "☀ Light" : "🌙 Dark";

    toggleBtn.addEventListener("click", () => {
      const current = document.documentElement.dataset.theme || "light";
      const next = current === "light" ? "dark" : "light";
      applyTheme(next);
      localStorage.setItem(themeKey, next);
      toggleBtn.textContent = next === "dark" ? "☀ Light" : "🌙 Dark";
    });
  }

  // ================= PATIENT SELECTION =================
  if (patientSelect) {
    patientSelect.addEventListener("change", (e) => {
      const id = e.target.value;
      if (id) window.location.href = `/patient/${id}`;
    });
  }

  // ================= CHART GLOW EFFECT =================
  const chartCanvas = document.querySelector("#relationChart");
  if (chartCanvas) {
    chartCanvas.style.boxShadow = "0 6px 20px rgba(0,0,0,0.4)";
    chartCanvas.addEventListener("mousemove", (e) => {
      const y = e.offsetY / chartCanvas.clientHeight;
      chartCanvas.style.boxShadow = `0 0 25px 4px rgba(125,249,255,${0.3 + 0.2 * (1 - y)})`;
    });
    chartCanvas.addEventListener("mouseleave", () => {
      chartCanvas.style.boxShadow = "0 6px 20px rgba(0,0,0,0.4)";
    });
  }

  // ================= NEON BAR ANIMATION =================
  const neonBar = document.querySelector(".neon-bar");
  if (neonBar) {
    let hue = 180;
    setInterval(() => {
      hue = (hue + 1) % 360;
      neonBar.style.background = `linear-gradient(90deg, hsl(${hue},100%,60%), hsl(${(hue + 60) % 360},100%,60%))`;
      neonBar.style.boxShadow = `0 0 12px hsl(${hue},100%,60%), 0 0 22px hsl(${(hue + 60) % 360},100%,60%)`;
    }, 50);
  }

  // ================= VOICE-TO-TEXT FOR REGISTER FORM =================
  initVoiceInputs(currentLang);
});

// Voice helper: used in register.html via .mic-btn[data-voice="field_name"]
function initVoiceInputs(langCode) {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    console.warn("SpeechRecognition API not supported in this browser.");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  // Map UI language to speech locale (rough mapping, all Indian contexts)
  const langMap = {
    en: "en-IN",
    hi: "hi-IN",
    bn: "bn-IN",
    as: "as-IN",
    or: "or-IN",
    ta: "ta-IN",
    te: "te-IN",
    kn: "kn-IN",
    ml: "ml-IN",
    gu: "gu-IN",
    pa: "pa-IN",
    mr: "mr-IN",
    ur: "ur-IN",
  };
  recognition.lang = langMap[langCode] || "en-IN";

  let activeTarget = null;

  document.querySelectorAll(".mic-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const fieldName = btn.getAttribute("data-voice");
      const target = document.querySelector(`[name="${fieldName}"]`);
      if (!target) return;

      activeTarget = target;
      try {
        recognition.start();
      } catch (err) {
        console.error("SpeechRecognition start error:", err);
      }
    });
  });

  recognition.addEventListener("result", (event) => {
    if (!activeTarget) return;
    const transcript = event.results[0][0].transcript;
    activeTarget.value = transcript;
    activeTarget.dispatchEvent(new Event("input", { bubbles: true }));
  });

  recognition.addEventListener("end", () => {
    activeTarget = null;
  });
}
