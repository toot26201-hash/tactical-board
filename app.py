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

clean_pro_addon = """
<style>
  #pro-tactics-master-dock,
  #custom-equip-dock,
  #player-size-control-box,
  #btn-export-1080p-global,
  #btn-top3d-cam {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }
</style>

<script>
(function initCleanProTactics() {
  // مسح أي شريط قديم موجود جوه index.html أو اتضاف قبل كده
  function purgeOldDocks() {
    ["pro-tactics-master-dock", "custom-equip-dock", "player-size-control-box", "btn-export-1080p-global", "btn-top3d-cam"].forEach(id => {
      document.querySelectorAll("#" + id).forEach(el => el.remove());
    });
    // مسح أي عنصر عائم على اليمين فيه كلمة "معدات:"
    document.querySelectorAll("div").forEach(div => {
      if (div.id !== "clean-pro-bottom-bar" && div.textContent && div.textContent.includes("معدات:") && div.textContent.includes("مسح")) {
        div.remove();
      }
    });
  }
  purgeOldDocks();
  setInterval(purgeOldDocks, 500);

  window.__globalPlayerRadius = window.__globalPlayerRadius || 16;
  window.__cam3dAngle = 0;

  function redrawBoardSafely() {
    try {
      if (typeof render === "function") render();
      if (typeof tsDraw === "function") tsDraw();
    } catch (e) {}
  }

  // التحكم في حجم اللاعبين والكرات
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

  // الكاميرا العلوية 3D
  window.cycleTop3DCamera = function () {
    if (window.__cam3dAngle === 0) window.__cam3dAngle = 28;
    else if (window.__cam3dAngle === 28) window.__cam3dAngle = 42;
    else window.__cam3dAngle = 0;

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

    const btn = document.getElementById("btn-clean-top3d");
    if (btn) {
      if (window.__cam3dAngle === 0) {
        btn.textContent = "🎥 3D علوي: إيقاف";
        btn.style.background = "#0f172a";
      } else {
        btn.textContent = `🎥 3D علوي (${window.__cam3dAngle}°)`;
        btn.style.background = "#059669";
      }
    }
  };

  // تصدير الفيديو بجودة 1080p 60fps
  window.exportBoardOrStudio1080p = function () {
    const studio = document.getElementById("toot-training-studio");
    const isStudioOpen = studio && studio.classList.contains("active");
    const cvs = isStudioOpen ? document.getElementById("ts-canvas") : document.querySelector("canvas");
    if (!cvs || typeof MediaRecorder === "undefined") return;

    const btn = document.getElementById("btn-clean-1080p");
    if (btn) { btn.disabled = true; btn.textContent = "⏳ جاري التسجيل..."; }

    const origW = cvs.width, origH = cvs.height;
    const scaleFactor = Math.max(1, 1920 / Math.max(1, origW));
    cvs.width = Math.round(origW * scaleFactor);
    cvs.height = Math.round(origH * scaleFactor);
    const ctx = cvs.getContext("2d");
    if (ctx) ctx.scale(scaleFactor, scaleFactor);
    redrawBoardSafely();

    const stream = cvs.captureStream(60);
    const mime = MediaRecorder.isTypeSupported("video/webm;codecs=vp9") ? "video/webm;codecs=vp9" : "video/webm";
    const recorder = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 12000000 });
    const chunks = [];
    recorder.ondataavailable = e => { if (e.data && e.data.size > 0) chunks.push(e.data); };
    recorder.onstop = () => {
      cvs.width = origW; cvs.height = origH;
      redrawBoardSafely();
      const url = URL.createObjectURL(new Blob(chunks, { type: "video/webm" }));
      const a = document.createElement("a");
      a.href = url; a.download = "TootScouting-ProTactics-1080p60.webm"; a.click();
      URL.revokeObjectURL(url);
      if (btn) { btn.disabled = false; btn.textContent = "🎬 فيديو 1080p"; }
    };

    let durationMs = 4000;
    if (isStudioOpen && typeof tsState !== "undefined") {
      tsState.currentFrame = 0;
      if (!tsState.playing && typeof tsTogglePlay === "function") tsTogglePlay();
      durationMs = Math.max(3200, (tsState.keyframes?.length || 2) * 1400);
    } else if (typeof playAnimation === "function") {
      try { playAnimation(); } catch (e) {}
    }
    recorder.start();
    setTimeout(() => {
      recorder.stop();
      if (isStudioOpen && typeof tsState !== "undefined" && tsState.playing && typeof tsTogglePlay === "function") tsTogglePlay();
    }, durationMs);
  };

  // شريط واحد نظيف في أعلى يسار الملعب بعيد عن كل الأزرار السفلية والجانبية
  function injectCleanTopBar() {
    if (document.getElementById("clean-pro-bottom-bar")) return;
    const bar = document.createElement("div");
    bar.id = "clean-pro-bottom-bar";
    bar.dir = "rtl";
    bar.style.cssText =
      "position:fixed;top:12px;left:16px;display:inline-flex;align-items:center;gap:6px;background:rgba(15,23,42,0.92);backdrop-filter:blur(8px);border:1px solid #334155;border-radius:10px;padding:5px 10px;font-size:12px;color:#f8fafc;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,.5);";

    bar.innerHTML = `
      <span style="color:#94a3b8;font-weight:600;">حجم اللاعب:</span>
      <button type="button" onclick="changePlayerSize(-2)" style="background:#1e293b;color:#f8fafc;border:1px solid #475569;border-radius:6px;width:24px;height:24px;cursor:pointer;font-weight:bold;">-</button>
      <span id="player-size-label" onclick="resetPlayerSize()" style="min-width:34px;text-align:center;cursor:pointer;font-weight:700;color:#38bdf8;">16px</span>
      <button type="button" onclick="changePlayerSize(2)" style="background:#1e293b;color:#f8fafc;border:1px solid #475569;border-radius:6px;width:24px;height:24px;cursor:pointer;font-weight:bold;">+</button>
      <button id="btn-clean-top3d" type="button" onclick="cycleTop3DCamera()" style="background:#0f172a;color:#e2e8f0;border:1px solid #475569;border-radius:7px;padding:4px 9px;font-size:11px;font-weight:700;cursor:pointer;">🎥 3D علوي: إيقاف</button>
      <button id="btn-clean-1080p" type="button" onclick="exportBoardOrStudio1080p()" style="background:#7c3aed;color:#ffffff;border:none;border-radius:7px;padding:4px 10px;font-size:11px;font-weight:700;cursor:pointer;">🎬 فيديو 1080p</button>
    `;
    document.body.appendChild(bar);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", injectCleanTopBar);
  } else {
    injectCleanTopBar();
  }
  setTimeout(injectCleanTopBar, 400);
})();
</script>
"""

if "initCleanProTactics" not in html_code:
    html_code = html_code + clean_pro_addon

components.html(html_code, height=1750, scrolling=False)
