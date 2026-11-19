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

live_animation_script = """
<style>
  @keyframes floatIcon {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
  }
  #features .grid > div .w-10 {
    animation: floatIcon 3s ease-in-out infinite;
  }
  #features .grid > div:nth-child(2) .w-10 { animation-delay: 0.6s; }
  #features .grid > div:nth-child(3) .w-10 { animation-delay: 1.2s; }
  #features .grid > div:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(212, 175, 55, 0.14);
  }
</style>

<script>
(function() {
    function initLiveHeroSimulation() {
        const landing = document.getElementById("landing-page");
        if (!landing) return;

        const heroBox = landing.querySelector(".max-w-4xl.mx-auto.mt-10");
        if (!heroBox || heroBox.dataset.liveInit) return;
        heroBox.dataset.liveInit = "1";

        heroBox.innerHTML = `
            <div class="bg-[#0d2618] border-2 border-amber-500/40 rounded-xl p-3 relative overflow-hidden">
                <div class="flex items-center justify-between text-[11px] font-en text-amber-300 font-bold mb-2 px-1">
                    <span class="flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                        LIVE TACTICAL SIMULATION 3D
                    </span>
                    <span id="sim-phase-label" class="bg-slate-950/90 border border-amber-500/30 text-amber-300 px-2.5 py-0.5 rounded-full">
                        Phase 1: Build-up • بناء اللعب
                    </span>
                </div>
                <canvas id="hero-live-canvas" width="840" height="320" class="w-full h-auto rounded-lg border border-white/20 block"></canvas>
            </div>
        `;

        const hCanvas = document.getElementById("hero-live-canvas");
        const hCtx = hCanvas.getContext("2d");
        const phaseLbl = document.getElementById("sim-phase-label");

        // مراحل الجملة التكتيكية المتحركة
        const states = [
            {
                label: "Phase 1: Build-up • جذب الضغط وبناء اللعب",
                red: [
                    { num: "1", role: "GK", x: 0.08, y: 0.50 },
                    { num: "4", role: "LCB", x: 0.22, y: 0.28 },
                    { num: "5", role: "RCB", x: 0.22, y: 0.72 },
                    { num: "6", role: "Pivot", x: 0.34, y: 0.50, glow: true },
                    { num: "10", role: "Half-Space", x: 0.54, y: 0.30 },
                    { num: "7", role: "RW", x: 0.60, y: 0.80 },
                    { num: "9", role: "ST", x: 0.66, y: 0.50 }
                ],
                blue: [
                    { num: "9", x: 0.28, y: 0.34 },
                    { num: "10", x: 0.38, y: 0.54 },
                    { num: "6", x: 0.56, y: 0.42 },
                    { num: "4", x: 0.74, y: 0.36 },
                    { num: "5", x: 0.74, y: 0.64 }
                ],
                ball: { x: 0.24, y: 0.28 }
            },
            {
                label: "Phase 2: Line-Breaking Pass • تمريرة كاسرة للخطوط",
                red: [
                    { num: "1", role: "GK", x: 0.10, y: 0.50 },
                    { num: "4", role: "LCB", x: 0.26, y: 0.25 },
                    { num: "5", role: "RCB", x: 0.26, y: 0.75 },
                    { num: "6", role: "Pivot", x: 0.40, y: 0.46, glow: true },
                    { num: "10", role: "Half-Space", x: 0.62, y: 0.26, glow: true },
                    { num: "7", role: "RW", x: 0.72, y: 0.78 },
                    { num: "9", role: "ST", x: 0.74, y: 0.46 }
                ],
                blue: [
                    { num: "9", x: 0.33, y: 0.38 },
                    { num: "10", x: 0.44, y: 0.48 },
                    { num: "6", x: 0.60, y: 0.46 },
                    { num: "4", x: 0.78, y: 0.34 },
                    { num: "5", x: 0.78, y: 0.62 }
                ],
                ball: { x: 0.61, y: 0.26 }
            },
            {
                label: "Phase 3: Third-Man Run • الاختراق في المساحة النصفية",
                red: [
                    { num: "1", role: "GK", x: 0.12, y: 0.50 },
                    { num: "4", role: "LCB", x: 0.30, y: 0.28 },
                    { num: "5", role: "RCB", x: 0.30, y: 0.72 },
                    { num: "6", role: "Pivot", x: 0.46, y: 0.48 },
                    { num: "10", role: "Half-Space", x: 0.68, y: 0.24, glow: true },
                    { num: "7", role: "RW", x: 0.84, y: 0.66, glow: true },
                    { num: "9", role: "ST", x: 0.83, y: 0.44 }
                ],
                blue: [
                    { num: "9", x: 0.42, y: 0.42 },
                    { num: "10", x: 0.54, y: 0.44 },
                    { num: "6", x: 0.68, y: 0.42 },
                    { num: "4", x: 0.85, y: 0.34 },
                    { num: "5", x: 0.86, y: 0.58 }
                ],
                ball: { x: 0.83, y: 0.65 }
            }
        ];

        let startTime = performance.now();
        const segDuration = 2600; // مدة كل مرحلة بالمللي ثانية

        function lerp(a, b, t) { return a + (b - a) * t; }
        function easeInOut(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

        function drawSim(now) {
            if (landing.classList.contains("hidden")) {
                requestAnimationFrame(drawSim);
                return;
            }
            const totalCycle = segDuration * states.length;
            const elapsed = (now - startTime) % totalCycle;
            const segIdx = Math.floor(elapsed / segDuration);
            const rawT = (elapsed % segDuration) / segDuration;
            // ثبات بسيط في نهاية كل حركة ثم انتقال سلس للمرحلة التالية
            const moveT = rawT < 0.7 ? easeInOut(rawT / 0.7) : 1;

            const sA = states[segIdx];
            const sB = states[(segIdx + 1) % states.length];
            if (phaseLbl && phaseLbl.textContent !== sB.label) {
                phaseLbl.textContent = sB.label;
            }

            const W = hCanvas.width, H = hCanvas.height;
            // رسم أرضية الملعب
            hCtx.fillStyle = "#133824";
            hCtx.fillRect(0, 0, W, H);
            for (let i = 0; i < 12; i += 2) {
                hCtx.fillStyle = "rgba(255,255,255,0.03)";
                hCtx.fillRect((W / 12) * i, 0, W / 12, H);
            }
            // خطوط الملعب
            hCtx.strokeStyle = "rgba(255,255,255,0.45)";
            hCtx.lineWidth = 2;
            hCtx.strokeRect(14, 14, W - 28, H - 28);
            hCtx.beginPath(); hCtx.moveTo(W / 2, 14); hCtx.lineTo(W / 2, H - 14); hCtx.stroke();
            hCtx.beginPath(); hCtx.arc(W / 2, H / 2, 42, 0, Math.PI * 2); hCtx.stroke();
            hCtx.strokeRect(14, H * 0.24, 95, H * 0.52);
            hCtx.strokeRect(W - 109, H * 0.24, 95, H * 0.52);

            // خطوط المساحات النصفية (Half-Spaces)
            hCtx.save();
            hCtx.strokeStyle = "rgba(250, 204, 21, 0.18)";
            hCtx.setLineDash([5, 5]);
            [0.24, 0.38, 0.62, 0.76].forEach(ry => {
                hCtx.beginPath(); hCtx.moveTo(14, H * ry); hCtx.lineTo(W - 14, H * ry); hCtx.stroke();
            });
            hCtx.restore();

            // حساب مواقع اللاعبين والكرة
            const curRed = sA.red.map((p, i) => ({
                ...p,
                x: lerp(p.x, sB.red[i].x, moveT),
                y: lerp(p.y, sB.red[i].y, moveT),
                glow: sB.red[i].glow
            }));
            const curBlue = sA.blue.map((p, i) => ({
                ...p,
                x: lerp(p.x, sB.blue[i].x, moveT),
                y: lerp(p.y, sB.blue[i].y, moveT)
            }));
            const curBall = {
                x: lerp(sA.ball.x, sB.ball.x, moveT),
                y: lerp(sA.ball.y, sB.ball.y, moveT)
            };

            // رسم خط ربط تكتيكي ديناميكي بين الارتكاز وصانع اللعب
            const p6 = curRed[3], p10 = curRed[4], p7 = curRed[5];
            hCtx.save();
            hCtx.strokeStyle = "rgba(250, 204, 21, 0.75)";
            hCtx.lineWidth = 2;
            hCtx.setLineDash([6, 4]);
            hCtx.beginPath();
            hCtx.moveTo(p6.x * W, p6.y * H);
            hCtx.lineTo(p10.x * W, p10.y * H);
            hCtx.lineTo(p7.x * W, p7.y * H);
            hCtx.stroke();
            hCtx.restore();

            // مسار الكرة المنحني
            hCtx.save();
            hCtx.strokeStyle = "#facc15";
            hCtx.lineWidth = 2.5;
            hCtx.beginPath();
            hCtx.moveTo(sA.ball.x * W, sA.ball.y * H);
            hCtx.lineTo(curBall.x * W, curBall.y * H);
            hCtx.stroke();
            hCtx.restore();

            // رسم الفريق الأزرق
            curBlue.forEach(p => {
                const px = p.x * W, py = p.y * H;
                hCtx.beginPath(); hCtx.arc(px, py, 14, 0, Math.PI * 2);
                hCtx.fillStyle = "#0284c7"; hCtx.fill();
                hCtx.strokeStyle = "#ffffff"; hCtx.lineWidth = 2; hCtx.stroke();
                hCtx.fillStyle = "#ffffff"; hCtx.font = "bold 11px Inter, sans-serif";
                hCtx.textAlign = "center"; hCtx.textBaseline = "middle";
                hCtx.fillText(p.num, px, py);
            });

            // رسم الفريق الأحمر مع نبض التمييز
            const pulse = Math.sin(now / 180) * 3.5;
            curRed.forEach(p => {
                const px = p.x * W, py = p.y * H;
                if (p.glow) {
                    hCtx.beginPath(); hCtx.arc(px, py, 20 + pulse, 0, Math.PI * 2);
                    hCtx.fillStyle = "rgba(250, 204, 21, 0.25)"; hCtx.fill();
                    hCtx.strokeStyle = "#facc15"; hCtx.lineWidth = 1.5; hCtx.stroke();
                }
                hCtx.beginPath(); hCtx.arc(px, py, 15, 0, Math.PI * 2);
                hCtx.fillStyle = "#dc2626"; hCtx.fill();
                hCtx.strokeStyle = "#ffffff"; hCtx.lineWidth = 2; hCtx.stroke();
                hCtx.fillStyle = "#ffffff"; hCtx.font = "bold 11px Inter, sans-serif";
                hCtx.textAlign = "center"; hCtx.textBaseline = "middle";
                hCtx.fillText(p.num, px, py);

                if (p.role) {
                    hCtx.font = "bold 9px Inter, sans-serif";
                    const tw = hCtx.measureText(p.role).width + 8;
                    hCtx.fillStyle = "rgba(15, 23, 42, 0.85)";
                    hCtx.fillRect(px - tw / 2, py + 17, tw, 13);
                    hCtx.fillStyle = p.glow ? "#facc15" : "#e2e8f0";
                    hCtx.fillText(p.role, px, py + 23.5);
                }
            });

            // رسم الكرة
            const bx = curBall.x * W, by = curBall.y * H;
            hCtx.beginPath(); hCtx.arc(bx, by, 7, 0, Math.PI * 2);
            hCtx.fillStyle = "#ffffff"; hCtx.fill();
            hCtx.strokeStyle = "#0f172a"; hCtx.lineWidth = 2; hCtx.stroke();

            requestAnimationFrame(drawSim);
        }

        requestAnimationFrame(drawSim);
    }

    function syncIframeHeight() {
        const iframe = window.frameElement;
        if (!iframe) return;
        const landing = document.getElementById("landing-page");
        const isLandingVisible = landing && !landing.classList.contains("hidden");
        if (isLandingVisible) {
            iframe.style.height = (landing.scrollHeight + 40) + "px";
        } else {
            iframe.style.height = "100vh";
            if (typeof resizeCanvas === "function") resizeCanvas();
        }
    }

    window.addEventListener("load", () => {
        initLiveHeroSimulation();
        syncIframeHeight();
    });
    setInterval(() => {
        initLiveHeroSimulation();
        syncIframeHeight();
    }, 300);
})();
</script>
</body>
"""

html_code = html_code.replace("</body>", live_animation_script)

components.html(html_code, height=1750, scrolling=False)
