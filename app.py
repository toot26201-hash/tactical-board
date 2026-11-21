import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ProTactics 3D PRO | TootScouting",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
        iframe { width: 100% !important; border: none !important; display: block !important; }
    </style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()
player_size_addon = """
<script>
(function addPlayerAndBallSizeControls() {
  window.__globalPlayerRadius = window.__globalPlayerRadius || 16;

  const origArc = CanvasRenderingContext2D.prototype.arc;
  CanvasRenderingContext2D.prototype.arc = function (x, y, radius, startAngle, endAngle, counterclockwise) {
    let finalRadius = radius;
    const isFullCircle = Math.abs(startAngle) < 0.01 && Math.abs(endAngle - Math.PI * 2) < 0.05;
    if (isFullCircle && radius >= 5 && radius <= 22) {
      const scale = (window.__globalPlayerRadius || 16) / 16;
      finalRadius = Math.max(4, Math.min(36, radius * scale));
    }
    return origArc.call(this, x, y, finalRadius, startAngle, endAngle, counterclockwise);
  };

  const fontDesc = Object.getOwnPropertyDescriptor(CanvasRenderingContext2D.prototype, "font");
  if (fontDesc && fontDesc.set && fontDesc.get) {
    Object.defineProperty(CanvasRenderingContext2D.prototype, "font", {
      get: function () { return fontDesc.get.call(this); },
      set: function (val) {
        const scale = (window.__globalPlayerRadius || 16) / 16;
        if (typeof val === "string" && scale !== 1) {
          const scaledVal = val.replace(/(\\d+(?:\\.\\d+)?)px/g, (_, num) => {
            const px = parseFloat(num);
            if (px >= 9 && px <= 15) {
              return Math.max(7, Math.min(24, Math.round(px * scale * 10) / 10)) + "px";
            }
            return px + "px";
          });
          return fontDesc.set.call(this, scaledVal);
        }
        return fontDesc.set.call(this, val);
      }
    });
  }

  function redrawBoardSafely() {
    try {
      if (typeof render === "function") render();
      if (typeof tsDraw === "function") tsDraw();
    } catch (e) {}
  }

  window.changePlayerSize = function (delta) {
    window.__globalPlayerRadius = Math.max(9, Math.min(30, (window.__globalPlayerRadius || 16) + delta));
    const badge = document.getElementById("player-size-label");
    if (badge) badge.textContent = window.__globalPlayerRadius + "px";
    redrawBoardSafely();
  };

  window.resetPlayerSize = function () {
    window.__globalPlayerRadius = 16;
    const badge = document.getElementById("player-size-label");
    if (badge) badge.textContent = "16px";
    redrawBoardSafely();
  };

  function injectSizeButtons() {
    if (document.getElementById("player-size-control-box")) return;
    const box = document.createElement("div");
    box.id = "player-size-control-box";
    box.dir = "rtl";
    box.style.cssText =
      "position:fixed;bottom:16px;right:16px;display:inline-flex;align-items:center;gap:5px;background:#1e293b;border:1px solid #475569;border-radius:10px;padding:5px 10px;font-size:12px;color:#f8fafc;z-index:99999;box-shadow:0 8px 20px rgba(0,0,0,.45);";

    box.innerHTML = `
      <span style="color:#94a3b8;font-weight:600;">حجم اللاعب:</span>
      <button type="button" onclick="changePlayerSize(-2)"
        style="background:#0f172a;color:#f8fafc;border:1px solid #64748b;border-radius:6px;width:24px;height:24px;cursor:pointer;font-weight:bold;">-</button>
      <span id="player-size-label" onclick="resetPlayerSize()"
        style="min-width:36px;text-align:center;cursor:pointer;font-weight:700;color:#38bdf8;">16px</span>
      <button type="button" onclick="changePlayerSize(2)"
        style="background:#0f172a;color:#f8fafc;border:1px solid #64748b;border-radius:6px;width:24px;height:24px;cursor:pointer;font-weight:bold;">+</button>
    `;
    document.body.appendChild(box);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectSizeButtons);
  } else {
    injectSizeButtons();
  }
  setTimeout(injectSizeButtons, 500);
})();
</script>
"""

if "addPlayerAndBallSizeControls" not in html_code:
    html_code = html_code + player_size_addon
top3d_camera_addon = """
<script>
(function addTopDown3DCamera() {
  window.__cam3dAngle = 0;

  function apply3DTransform() {
    const targets = [
      document.getElementById("ts-canvas"),
      ...Array.from(document.querySelectorAll("canvas"))
    ].filter(Boolean);

    targets.forEach(cvs => {
      if (cvs.parentElement) {
        cvs.parentElement.style.perspective = "1400px";
        cvs.parentElement.style.transformStyle = "preserve-3d";
      }
      cvs.style.transition = "transform 0.45s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.45s ease";
      if (window.__cam3dAngle > 0) {
        cvs.style.transform = `rotateX(${window.__cam3dAngle}deg) scale(0.96)`;
        cvs.style.boxShadow = "0 28px 50px rgba(0, 0, 0, 0.65)";
      } else {
        cvs.style.transform = "rotateX(0deg) scale(1)";
        cvs.style.boxShadow = "";
      }
    });

    const btn = document.getElementById("btn-top3d-cam");
    if (btn) {
      if (window.__cam3dAngle === 0) {
        btn.textContent = "🎥 3D علوي: إيقاف";
        btn.style.background = "#0f172a";
        btn.style.color = "#e2e8f0";
      } else {
        btn.textContent = `🎥 3D علوي (${window.__cam3dAngle}°)`;
        btn.style.background = "#059669";
        btn.style.color = "#ffffff";
      }
    }
  }

  window.cycleTop3DCamera = function () {
    if (window.__cam3dAngle === 0) window.__cam3dAngle = 28;
    else if (window.__cam3dAngle === 28) window.__cam3dAngle = 42;
    else window.__cam3dAngle = 0;
    apply3DTransform();
  };

  function inject3DCameraButton() {
    if (document.getElementById("btn-top3d-cam")) return;
    const sizeBox = document.getElementById("player-size-control-box");
    const btn = document.createElement("button");
    btn.id = "btn-top3d-cam";
    btn.type = "button";
    btn.textContent = "🎥 3D علوي: إيقاف";
    btn.onclick = cycleTop3DCamera;
    btn.style.cssText =
      "background:#0f172a;color:#e2e8f0;border:1px solid #64748b;border-radius:7px;padding:3px 8px;margin-right:6px;font-size:11px;font-weight:700;cursor:pointer;";

    if (sizeBox) {
      sizeBox.appendChild(btn);
    } else {
      btn.style.position = "fixed";
      btn.style.bottom = "56px";
      btn.style.right = "16px";
      btn.style.zIndex = "99999";
      document.body.appendChild(btn);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject3DCameraButton);
  } else {
    inject3DCameraButton();
  }
  setTimeout(inject3DCameraButton, 700);
})();
</script>
"""

if "addTopDown3DCamera" not in html_code:
    html_code = html_code + top3d_camera_addon

components.html(html_code, height=1750, scrolling=False)
