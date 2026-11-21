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

sidebar_player_size_addon = """
<script>
(function initSidebarPlayerSizeAndHD() {
  window.__globalPlayerRadius = window.__globalPlayerRadius || 16;

  // 1. رفع جودة تصدير الفيديو تلقائياً في الخلفية عند الضغط على زرار "فيديو"
  if (typeof MediaRecorder !== "undefined") {
    const OrigMediaRecorder = window.MediaRecorder;
    window.MediaRecorder = function (stream, options) {
      const upgradedOptions = Object.assign({}, options || {}, {
        videoBitsPerSecond: 12000000
      });
      return new OrigMediaRecorder(stream, upgradedOptions);
    };
    window.MediaRecorder.prototype = OrigMediaRecorder.prototype;
    window.MediaRecorder.isTypeSupported = OrigMediaRecorder.isTypeSupported.bind(OrigMediaRecorder);
  }

  // 2. تعديل حجم اللاعبين وأرقامهم على السبورة
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
    const badge = document.getElementById("sidebar-player-size-label");
    if (badge) badge.textContent = window.__globalPlayerRadius + "px";
    redrawBoardSafely();
  };

  window.resetPlayerSize = function () {
    window.__globalPlayerRadius = 16;
    const badge = document.getElementById("sidebar-player-size-label");
    if (badge) badge.textContent = "16px";
    redrawBoardSafely();
  };

  // 3. دمج أزرار حجم اللاعب جوه القائمة الجانبية اليمنى تحت "سلم سرعة / حاجز قفز"
  function injectInsideRightSidebar() {
    if (document.getElementById("sidebar-player-size-box")) return;

    const allButtons = Array.from(document.querySelectorAll("button"));
    const targetBtn = allButtons.find(b => b.textContent && (b.textContent.includes("سلم سرعة") || b.textContent.includes("حاجز قفز")));

    const container = document.createElement("div");
    container.id = "sidebar-player-size-box";
    container.dir = "rtl";
    container.style.cssText =
      "margin-top:10px;padding:8px;background:#0f172a;border:1px solid #334155;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:6px;font-size:12px;color:#e2e8f0;width:100%;box-sizing:border-box;";

    container.innerHTML = `
      <span style="color:#94a3b8;font-weight:600;">حجم اللاعبين:</span>
      <div style="display:inline-flex;align-items:center;gap:6px;">
        <button type="button" onclick="changePlayerSize(-2)"
          style="background:#1e293b;color:#f8fafc;border:1px solid #475569;border-radius:6px;width:26px;height:26px;cursor:pointer;font-weight:bold;">-</button>
        <span id="sidebar-player-size-label" onclick="resetPlayerSize()" title="اضغط لإعادة الحجم الافتراضي"
          style="min-width:36px;text-align:center;cursor:pointer;font-weight:700;color:#38bdf8;">16px</span>
        <button type="button" onclick="changePlayerSize(2)"
          style="background:#1e293b;color:#f8fafc;border:1px solid #475569;border-radius:6px;width:26px;height:26px;cursor:pointer;font-weight:bold;">+</button>
      </div>
    `;

    if (targetBtn && targetBtn.parentElement && targetBtn.parentElement.parentElement) {
      targetBtn.parentElement.parentElement.appendChild(container);
    } else if (targetBtn && targetBtn.parentElement) {
      targetBtn.parentElement.appendChild(container);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectInsideRightSidebar);
  } else {
    injectInsideRightSidebar();
  }
  setTimeout(injectInsideRightSidebar, 500);
  setTimeout(injectInsideRightSidebar, 1500);
})();
</script>
"""

if "initSidebarPlayerSizeAndHD" not in html_code:
    html_code = html_code + sidebar_player_size_addon

components.html(html_code, height=1750, scrolling=False)
