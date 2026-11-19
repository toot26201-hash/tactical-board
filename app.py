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
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
            display: none !important;
        }
        iframe {
            width: 100% !important;
            border: none !important;
            display: block !important;
        }
    </style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

inject_code = """
<style>
  #board-main {
    height: calc(100vh - 48px) !important;
    max-height: calc(100vh - 48px) !important;
  }
  @keyframes floatIcon { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-6px); } }
  #features .grid > div .w-10 { animation: floatIcon 3s ease-in-out infinite; }
  #features .grid > div:nth-child(2) .w-10 { animation-delay: 0.6s; }
  #features .grid > div:nth-child(3) .w-10 { animation-delay: 1.2s; }
  #features .grid > div:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(212, 175, 55, 0.14); }
</style>

<script>
(function() {
  // ربط رسم قوس منطقة الجزاء ونقطة الجزاء وأقواس الركنيات مباشرة بعد رسم مستطيل الملعب في أي وضع (كامل / نصف / 2D / 3D)
  const origStroke = CanvasRenderingContext2D.prototype.stroke;
  let isDrawingExtras = false;

  CanvasRenderingContext2D.prototype.stroke = function() {
    origStroke.apply(this, arguments);
    if (isDrawingExtras) return;
    if (!this.canvas || this.canvas.id !== "tactical-canvas") return;
    if (typeof pitchRect === "undefined" || typeof normToCanvas !== "function") return;

    // التحقق أننا في مرحلة رسم خطوط الملعب (lineWidth === 2 واللون يطابق لون خطوط الملعب)
    const th = (typeof pitchThemes !== "undefined" && pitchThemes[pitchTheme]) ? pitchThemes[pitchTheme] : null;
    if (!th || this.lineWidth !== 2) return;

    // تجنب التكرار داخل نفس الفريم باستخدام طابع زمني للرسم
    const frameKey = Math.round(performance.now());
    if (this.canvas._lastExtraFrame === frameKey) return;
    this.canvas._lastExtraFrame = frameKey;

    isDrawingExtras = true;
    try {
      const mode = (typeof pitchMode !== "undefined") ? pitchMode : "full";
      const len = mode === "full" ? 105 : 52.5;
      const spotX = 11 / len;
      const arcRx = 9.15 / len;
      const arcRy = 9.15 / 68;
      const theta = Math.acos(5.5 / 9.15);
      const cRx = 1.2 / len, cRy = 1.2 / 68;

      this.save();
      this.strokeStyle = th.lines;
      this.fillStyle = th.lines;
      this.lineWidth = 2;
      this.setLineDash([]);

      const drawArcN = (cxN, cyN, rxN, ryN, a1, a2) => {
        this.beginPath();
        for (let i = 0; i <= 28; i++) {
          const ang = a1 + (a2 - a1) * (i / 28);
          const pt = normToCanvas(cxN + Math.cos(ang) * rxN, cyN + Math.sin(ang) * ryN);
          if (i === 0) this.moveTo(pt.x, pt.y); else this.lineTo(pt.x, pt.y);
        }
        origStroke.call(this);
      };

      const drawSpotN = (nx, ny) => {
        const pt = normToCanvas(nx, ny);
        this.beginPath();
        this.arc(pt.x, pt.y, 3, 0, Math.PI * 2);
        this.fill();
      };

      // قوس ونقطة جزاء المرمى الأيسر
      drawArcN(spotX, 0.5, arcRx, arcRy, -theta, theta);
      drawSpotN(spotX, 0.5);

      // أقواس الركنيات اليسرى
      drawArcN(0, 0, cRx, cRy, 0, Math.PI / 2);
      drawArcN(0, 1, cRx, cRy, -Math.PI / 2, 0);

      if (mode === "full") {
        drawSpotN(0.5, 0.5);
        drawArcN(1 - spotX, 0.5, arcRx, arcRy, Math.PI - theta, Math.PI + theta);
        drawSpotN(1 - spotX, 0.5);
        drawArcN(1, 0, cRx, cRy, Math.PI / 2, Math.PI);
        drawArcN(1, 1, cRx, cRy, Math.PI, Math.PI * 1.5);
      }
      this.restore();
    } finally {
      isDrawingExtras = false;
    }
  };

  // المحاكاة المتحركة في صفحة الهبوط
  function initLiveHeroSimulation() {
    const landing = document.getElementById("landing-page");
    if (!landing) return;
    const heroBox = landing.querySelector(".max-w-4xl.mx-auto.mt-10");
    if (!heroBox || heroBox.dataset.liveInit) return;
    heroBox.dataset.liveInit = "1";
    heroBox.innerHTML = `
      <div class="bg-[#0d2618] border-2 border-amber-500/40 rounded-xl p-3 relative overflow-hidden">
        <div class="flex items-center justify-between text-[11px] font-en text-amber-300 font-bold mb-2 px-1">
          <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>LIVE TACTICAL SIMULATION 3D</span>
          <span id="sim-phase-label" class="bg-slate-950/90 border border-amber-500/30 text-amber-300 px-2.5 py-0.5 rounded-full">Phase 1: Build-up</span>
        </div>
        <canvas id="hero-live-canvas" width="840" height="320" class="w-full h-auto rounded-lg border border-white/20 block"></canvas>
      </div>`;
    const hCanvas = document.getElementById("hero-live-canvas"), hCtx = hCanvas.getContext("2d"), phaseLbl = document.getElementById("sim-phase-label");
    const states = [
      { label: "Phase 1: Build-up • جذب الضغط وبناء اللعب", red: [{num:"1",role:"GK",x:0.08,y:0.50},{num:"4",role:"LCB",x:0.22,y:0.28},{num:"5",role:"RCB",x:0.22,y:0.72},{num:"6",role:"Pivot",x:0.34,y:0.50,glow:true},{num:"10",role:"Half-Space",x:0.54,y:0.30},{num:"7",role:"RW",x:0.60,y:0.80},{num:"9",role:"ST",x:0.66,y:0.50}], blue: [{num:"9",x:0.28,y:0.34},{num:"10",x:0.38,y:0.54},{num:"6",x:0.56,y:0.42},{num:"4",x:0.74,y:0.36},{num:"5",x:0.74,y:0.64}], ball: {x:0.24,y:0.28} },
      { label: "Phase 2: Line-Breaking Pass • تمريرة كاسرة للخطوط", red: [{num:"1",role:"GK",x:0.10,y:0.50},{num:"4",role:"LCB",x:0.26,y:0.25},{num:"5",role:"RCB",x:0.26,y:0.75},{num:"6",role:"Pivot",x:0.40,y:0.46,glow:true},{num:"10",role:"Half-Space",x:0.62,y:0.26,glow:true},{num:"7",role:"RW",x:0.72,y:0.78},{num:"9",role:"ST",x:0.74,y:0.46}], blue: [{num:"9",x:0.33,y:0.38},{num:"10",x:0.44,y:0.48},{num:"6",x:0.60,y:0.46},{num:"4",x:0.78,y:0.34},{num:"5",x:0.78,y:0.62}], ball: {x:0.61,y:0.26} },
      { label: "Phase 3: Third-Man Run • الاختراق في المساحة النصفية", red: [{num:"1",role:"GK",x:0.12,y:0.50},{num:"4",role:"LCB",x:0.30,y:0.28},{num:"5",role:"RCB",x:0.30,y:0.72},{num:"6",role:"Pivot",x:0.46,y:0.48},{num:"10",role:"Half-Space",x:0.68,y:0.24,glow:true},{num:"7",role:"RW",x:0.84,y:0.66,glow:true},{num:"9",role:"ST",x:0.83,y:0.44}], blue: [{num:"9",x:0.42,y:0.42},{num:"10",x:0.54,y:0.44},{num:"6",x:0.68,y:0.42},{num:"4",x:0.85,y:0.34},{num:"5",x:0.86,y:0.58}], ball: {x:0.83,y:0.65} }
    ];
    let startTime = performance.now();
    const lerp = (a, b, t) => a + (b - a) * t, ease = t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    function drawSim(now) {
      if (landing.classList.contains("hidden")) { requestAnimationFrame(drawSim); return; }
      const elapsed = (now - startTime) % (2600 * states.length), segIdx = Math.floor(elapsed / 2600), rawT = (elapsed % 2600) / 2600, moveT = rawT < 0.7 ? ease(rawT / 0.7) : 1;
      const sA = states[segIdx], sB = states[(segIdx + 1) % states.length];
      if (phaseLbl && phaseLbl.textContent !== sB.label) phaseLbl.textContent = sB.label;
      const W = hCanvas.width, H = hCanvas.height;
      hCtx.fillStyle = "#133824"; hCtx.fillRect(0, 0, W, H);
      for (let i = 0; i < 12; i += 2) { hCtx.fillStyle = "rgba(255,255,255,0.03)"; hCtx.fillRect((W / 12) * i, 0, W / 12, H); }
      hCtx.strokeStyle = "rgba(255,255,255,0.45)"; hCtx.lineWidth = 2; hCtx.strokeRect(14, 14, W - 28, H - 28);
      hCtx.beginPath(); hCtx.moveTo(W / 2, 14); hCtx.lineTo(W / 2, H - 14); hCtx.stroke();
      hCtx.beginPath(); hCtx.arc(W / 2, H / 2, 42, 0, Math.PI * 2); hCtx.stroke();
      hCtx.strokeRect(14, H * 0.24, 95, H * 0.52); hCtx.strokeRect(14, H * 0.37, 34, H * 0.26);
      hCtx.beginPath(); hCtx.arc(78, H / 2, 42, -0.92, 0.92); hCtx.stroke();
      hCtx.strokeRect(W - 109, H * 0.24, 95, H * 0.52); hCtx.strokeRect(W - 48, H * 0.37, 34, H * 0.26);
      hCtx.beginPath(); hCtx.arc(W - 78, H / 2, 42, Math.PI - 0.92, Math.PI + 0.92); hCtx.stroke();
      const curRed = sA.red.map((p, i) => ({...p, x: lerp(p.x, sB.red[i].x, moveT), y: lerp(p.y, sB.red[i].y, moveT), glow: sB.red[i].glow}));
      const curBlue = sA.blue.map((p, i) => ({...p, x: lerp(p.x, sB.blue[i].x, moveT), y: lerp(p.y, sB.blue[i].y, moveT)}));
      const curBall = {x: lerp(sA.ball.x, sB.ball.x, moveT), y: lerp(sA.ball.y, sB.ball.y, moveT)};
      const p6 = curRed[3], p10 = curRed[4], p7 = curRed[5];
      hCtx.save(); hCtx.strokeStyle = "rgba(250,204,21,0.75)"; hCtx.lineWidth = 2; hCtx.setLineDash([6, 4]);
      hCtx.beginPath(); hCtx.moveTo(p6.x * W, p6.y * H); hCtx.lineTo(p10.x * W, p10.y * H); hCtx.lineTo(p7.x * W, p7.y * H); hCtx.stroke(); hCtx.restore();
      hCtx.save(); hCtx.strokeStyle = "#facc15"; hCtx.lineWidth = 2.5;
      hCtx.beginPath(); hCtx.moveTo(sA.ball.x * W, sA.ball.y * H); hCtx.lineTo(curBall.x * W, curBall.y * H); hCtx.stroke(); hCtx.restore();
      curBlue.forEach(p => { const px = p.x * W, py = p.y * H; hCtx.beginPath(); hCtx.arc(px, py, 14, 0, Math.PI * 2); hCtx.fillStyle = "#0284c7"; hCtx.fill(); hCtx.strokeStyle = "#fff"; hCtx.lineWidth = 2; hCtx.stroke(); hCtx.fillStyle = "#fff"; hCtx.font = "bold 11px Inter, sans-serif"; hCtx.textAlign = "center"; hCtx.textBaseline = "middle"; hCtx.fillText(p.num, px, py); });
      const pulse = Math.sin(now / 180) * 3.5;
      curRed.forEach(p => { const px = p.x * W, py = p.y * H; if (p.glow) { hCtx.beginPath(); hCtx.arc(px, py, 20 + pulse, 0, Math.PI * 2); hCtx.fillStyle = "rgba(250,204,21,0.25)"; hCtx.fill(); hCtx.strokeStyle = "#facc15"; hCtx.lineWidth = 1.5; hCtx.stroke(); } hCtx.beginPath(); hCtx.arc(px, py, 15, 0, Math.PI * 2); hCtx.fillStyle = "#dc2626"; hCtx.fill(); hCtx.strokeStyle = "#fff"; hCtx.lineWidth = 2; hCtx.stroke(); hCtx.fillStyle = "#fff"; hCtx.font = "bold 11px Inter, sans-serif"; hCtx.textAlign = "center"; hCtx.textBaseline = "middle"; hCtx.fillText(p.num, px, py); if (p.role) { hCtx.font = "bold 9px Inter, sans-serif"; const tw = hCtx.measureText(p.role).width + 8; hCtx.fillStyle = "rgba(15,23,42,0.85)"; hCtx.fillRect(px - tw / 2, py + 17, tw, 13); hCtx.fillStyle = p.glow ? "#facc15" : "#e2e8f0"; hCtx.fillText(p.role, px, py + 23.5); } });
      hCtx.beginPath(); hCtx.arc(curBall.x * W, curBall.y * H, 7, 0, Math.PI * 2); hCtx.fillStyle = "#fff"; hCtx.fill(); hCtx.strokeStyle = "#0f172a"; hCtx.lineWidth = 2; hCtx.stroke();
      requestAnimationFrame(drawSim);
    }
    requestAnimationFrame(drawSim);
  }

  function syncIframeHeight() {
    const iframe = window.frameElement;
    if (!iframe) return;
    const landing = document.getElementById("landing-page");
    const isLandingVisible = landing && !landing.classList.contains("hidden");
    if (isLandingVisible) { iframe.style.height = (landing.scrollHeight + 40) + "px"; }
    else { iframe.style.height = "100vh"; if (typeof resizeCanvas === "function") resizeCanvas(); }
  }

  window.addEventListener("load", () => {
    initLiveHeroSimulation();
    syncIframeHeight();
    if (typeof render === "function") render();
  });
  setInterval(() => {
    initLiveHeroSimulation();
    syncIframeHeight();
  }, 300);
})();
</script>
"""

html_code = html_code + inject_code
components.html(html_code, height=1750, scrolling=False)
