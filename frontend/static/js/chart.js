// /frontend/static/js/chart.js
// Standalone chart rendering module for Neural Health Link (Mock Edition)
// Uses Chart.js (CDN included in report.html)

function renderRelationChart(canvasId, labels, data) {
  if (!window.Chart) {
    console.warn("Chart.js not loaded");
    return;
  }

  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  const gradient = ctx.getContext("2d").createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, "rgba(125,249,255,0.9)");
  gradient.addColorStop(1, "rgba(167,139,250,0.6)");

  const config = {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Relation Probability (%)",
          data: data,
          backgroundColor: gradient,
          borderColor: "rgba(125,249,255,0.9)",
          borderWidth: 1,
          borderRadius: 8,
          hoverBackgroundColor: "rgba(167,139,250,0.9)"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: "#e6eef8",
            font: { family: "Outfit", size: 14 }
          }
        },
        tooltip: {
          backgroundColor: "#0e1525",
          titleColor: "#7df9ff",
          bodyColor: "#e6eef8",
          borderColor: "#7df9ff44",
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return context.parsed.y + "% relation";
            }
          }
        }
      },
      scales: {
        x: {
          ticks: { color: "#99a3b7", font: { family: "Outfit" } },
          grid: { color: "#1b2340" }
        },
        y: {
          beginAtZero: true,
          ticks: { color: "#99a3b7", stepSize: 10 },
          grid: { color: "#1b2340" }
        }
      },
      animation: {
        duration: 1200,
        easing: "easeOutQuart"
      }
    }
  };

  new Chart(ctx, config);
}

// Example usage (can be called from report.html)
function initMockChart() {
  const labels = ["Cough", "Headache", "Shortness of Breath"];
  const data = [78, 64, 52];
  renderRelationChart("relationChart", labels, data);
}
