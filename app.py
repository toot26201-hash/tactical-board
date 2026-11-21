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
    pro_studio_upgrades = """
<script>
(function addProUpgradesToBoardAndStudio() {
  // 1. التحكم في سمك الأسهم والخطوط
  window.__globalArrowWidth = window.__globalArrowWidth || 2;

  const lineWidthDesc = Object.getOwnPropertyDescriptor(CanvasRenderingContext2D.prototype, "lineWidth");
  if (lineWidthDesc && lineWidthDesc.set && lineWidthDesc.get) {
    Object.defineProperty(CanvasRenderingContext2D.prototype, "lineWidth", {
      get: function () { return lineWidthDesc.get.call(this); },
      set: function (val) {
        const scale = (window.__globalArrowWidth || 2) / 2;
        if (typeof val === "number" && scale !== 1 && val >= 1.5 && val <= 6) {
          return lineWidthDesc.set.call(this, Math.max(1, Math.min(12, val * scale)));
        }
        return lineWidthDesc.set.call(this, val);
      }
    });
  }

  function redrawAll() {
    try {
      if (typeof render === "function") render();
      if (typeof tsDraw === "function") tsDraw();
    } catch (e) {}
  }

  window.changeArrowWidth = function (delta) {
    window.__globalArrowWidth = Math.max(1, Math.min(8, (window.__globalArrowWidth || 2) + delta));
    const el = document.getElementById("arrow-width-label");
    if (el) el.textContent = window.__globalArrowWidth + "px";
    redrawAll();
  };

  window.resetArrowWidth = function () {
    window.__globalArrowWidth = 2;
    const el = document.getElementById("arrow-width-label");
    if (el) el.textContent = "2px";
    redrawAll();
  };

  function injectArrowWidthControl() {
    if (document.getElementById("arrow-width-control-box")) return;
    const sizeBox = document.getElementById("player-size-control-box");
    const box = document.createElement("div");
    box.id = "arrow-width-control-box";
    box.dir = "rtl";
    box.style.cssText =
      "display:inline-flex;align-items:center;gap:5px;background:#1e293b;border:1px solid #475569;border-radius:10px;padding:5px 10px;font-size:12px;color:#f8fafc;z-index:99999;box-shadow:0 8px 20px rgba(0,0,0,.45);";

    box.innerHTML = `
      <span style="color:#94a3b8;font-weight:600;">سمك الأسهم:</span>
      <button type="button" onclick="changeArrowWidth(-0.5)"
        style="background:#0f172a;color:#f8fafc;border:1px solid #64748b;border-radius:6px;width:24px;height:24px;cursor:pointer;font-weight:bold;">-</button>
      <span id="arrow-width-label" onclick="resetArrowWidth()"
        style="min-width:34px;text-align:center;cursor:pointer;font-weight:700;color:#facc15;">2px</span>
      <button type="button" onclick="changeArrowWidth(0.5)"
        style="background:#0f172a;color:#f8fafc;border:1px solid #64748b;border-radius:6px;width:24px;height:24px;cursor:pointer;font-weight:bold;">+</button>
    `;

    if (sizeBox && sizeBox.parentElement) {
      box.style.position = "fixed";
      box.style.bottom = "56px";
      box.style.right = "16px";
      document.body.appendChild(box);
    } else {
      box.style.position = "fixed";
      box.style.bottom = "56px";
      box.style.right = "16px";
      document.body.appendChild(box);
    }
  }

  // 2. إضافة قالب 5v3 التحول + زر تصدير الفيديو HD داخل استوديو التدريب
  function enhanceTrainingStudio() {
    const studio = document.getElementById("toot-training-studio");
    if (!studio) return;

    // إضافة زر قالب 5v3 التحول في الشريط العلوي للاستوديو
    const clearBtn = studio.querySelector('button[onclick="tsClearBoard()"]');
    if (clearBtn && !document.getElementById("btn-preset-5v3")) {
      const presetBtn = document.createElement("button");
      presetBtn.id = "btn-preset-5v3";
      presetBtn.type = "button";
      presetBtn.textContent = "قالب 5v3 التحول";
      presetBtn.className = "bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 text-xs px-2.5 py-1 rounded";
      presetBtn.onclick = function () {
        if (typeof tsState === "undefined") return;
        if (tsState.playing && typeof tsTogglePlay === "function") tsTogglePlay();
        document.getElementById("ts-title").value = "Attacking to Defensive Transition (5v3 Dual Zone)";
        document.getElementById("ts-duration").value = "20 min";
        document.getElementById("ts-players-count").value = "12-20 players";
        document.getElementById("ts-category").value = "Transition / Rondo";

        tsState.zones = [
          { id: "z_outer", x: 0.22, y: 0.20, w: 0.56, h: 0.60, color: "#ffffff", glow: false },
          { id: "z_inner", x: 0.34, y: 0.30, w: 0.32, h: 0.40, color: "#facc15", glow: true }
        ];

        const p1 = [
          { id: "b_t", team: "ball", num: "", x: 0.38, y: 0.36 },
          { id: "y_1", team: "yellow", num: "4", x: 0.37, y: 0.35 },
          { id: "y_2", team: "yellow", num: "5", x: 0.62, y: 0.35 },
          { id: "y_3", team: "yellow", num: "6", x: 0.50, y: 0.50 },
          { id: "y_4", team: "yellow", num: "8", x: 0.37, y: 0.65 },
          { id: "y_5", team: "yellow", num: "10", x: 0.62, y: 0.65 },
          { id: "bl_in1", team: "blue", num: "9", x: 0.45, y: 0.42 },
          { id: "bl_in2", team: "blue", num: "11", x: 0.55, y: 0.44 },
          { id: "bl_in3", team: "blue", num: "7", x: 0.48, y: 0.58 },
          { id: "bl_out1", team: "blue", num: "2", x: 0.26, y: 0.26 },
          { id: "bl_out2", team: "blue", num: "3", x: 0.74, y: 0.26 },
          { id: "bl_out3", team: "blue", num: "6", x: 0.26, y: 0.74 },
          { id: "bl_out4", team: "blue", num: "8", x: 0.74, y: 0.74 }
        ];

        const p2 = p1.map(p => {
          if (p.id === "b_t") return { ...p, x: 0.46, y: 0.43 };
          if (p.id === "bl_in1") return { ...p, x: 0.46, y: 0.43 };
          if (p.id === "bl_out1") return { ...p, x: 0.25, y: 0.32 };
          return { ...p };
        });

        const p3 = p2.map(p => {
          if (p.id === "b_t") return { ...p, x: 0.26, y: 0.32 };
          if (p.id === "bl_out1") return { ...p, x: 0.26, y: 0.32 };
          if (p.id === "bl_out2") return { ...p, x: 0.73, y: 0.34 };
          return { ...p };
        });

        tsState.players = JSON.parse(JSON.stringify(p1));
        tsState.arrows = [{ kind: "pass", x1: 0.37, y1: 0.35, x2: 0.62, y2: 0.35 }];
        tsState.keyframes = [
          { players: p1, zones: JSON.parse(JSON.stringify(tsState.zones)), arrows: [{ kind: "pass", x1: 0.37, y1: 0.35, x2: 0.62, y2: 0.35 }] },
          { players: p2, zones: JSON.parse(JSON.stringify(tsState.zones)), arrows: [{ kind: "pass", x1: 0.46, y1: 0.43, x2: 0.26, y2: 0.32 }] },
          { players: p3, zones: tsState.zones.map(z => ({ ...z, glow: z.id === "z_outer" })), arrows: [] }
        ];
        tsState.currentFrame = 0;
        if (typeof tsResize === "function") tsResize();
        if (typeof tsRenderFramesBar === "function") tsRenderFramesBar();
        if (typeof tsDraw === "function") tsDraw();
      };
      clearBtn.parentElement.insertBefore(presetBtn, clearBtn);
    }

    // 3. إضافة زر تصدير فيديو HD بجوار زر حفظ PNG
    const pngBtn = studio.querySelector('button[onclick="tsExportPNG()"]');
    if (pngBtn && !document.getElementById("btn-ts-export-video")) {
      const vidBtn = document.createElement("button");
      vidBtn.id = "btn-ts-export-video";
      vidBtn.type = "button";
      vidBtn.textContent = "🎬 تصدير فيديو HD";
      vidBtn.className = "bg-purple-600 hover:bg-purple-500 text-white py-1.5 rounded font-semibold mt-1";
      vidBtn.onclick = function () {
        const cvs = document.getElementById("ts-canvas");
        if (!cvs || typeof tsState === "undefined") return;
        if (tsState.keyframes.length < 2) {
          alert("أضف لقطتي حركة (Keyframes) على الأقل لتصدير الفيديو.");
          return;
        }
        if (typeof MediaRecorder === "undefined") {
          alert("المتصفح الحالي لا يدعم تسجيل الفيديو المباشر.");
          return;
        }
        vidBtn.disabled = true;
        vidBtn.textContent = "⏳ جاري تسجيل الفيديو...";
        const stream = cvs.captureStream(60);
        const recorder = new MediaRecorder(stream, {
          mimeType: MediaRecorder.isTypeSupported("video/webm;codecs=vp9") ? "video/webm;codecs=vp9" : "video/webm",
          videoBitsPerSecond: 6000000
        });
        const chunks = [];
        recorder.ondataavailable = e => { if (e.data && e.data.size > 0) chunks.push(e.data); };
        recorder.onstop = () => {
          const blob = new Blob(chunks, { type: "video/webm" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "TootScouting-Drill-HD.webm";
          a.click();
          URL.revokeObjectURL(url);
          vidBtn.disabled = false;
          vidBtn.textContent = "🎬 تصدير فيديو HD";
        };

        tsState.currentFrame = 0;
        if (!tsState.playing && typeof tsTogglePlay === "function") tsTogglePlay();
        recorder.start();

        const durationMs = Math.max(3000, tsState.keyframes.length * 1400);
        setTimeout(() => {
          recorder.stop();
          if (tsState.playing && typeof tsTogglePlay === "function") tsTogglePlay();
        }, durationMs);
      };
      pngBtn.parentElement.insertBefore(vidBtn, pngBtn);
    }
  }

  function initAllUpgrades() {
    injectArrowWidthControl();
    enhanceTrainingStudio();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAllUpgrades);
  } else {
    initAllUpgrades();
  }
  setTimeout(initAllUpgrades, 600);
})();
</script>
"""

if "addProUpgradesToBoardAndStudio" not in html_code:
    html_code = html_code + pro_studio_upgrades
components.html(html_code, height=1750, scrolling=False)
