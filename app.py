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

# حقن دالة رسم قوس منطقة الجزاء مباشرة داخل دالة render الأصلية
pitch_arc_code = """
  // رسم قوس منطقة الجزاء، نقطة الجزاء، نقطة السنتر، وأقواس الركنيات بأبعاد الفيفا
  (function() {
    const { w, h } = pitchRect;
    if (w <= 0 || h <= 0) return;
    const th = pitchThemes[pitchTheme] || pitchThemes.green;
    const len = pitchMode === "full" ? 105 : 52.5;
    const spotX = 11 / len;
    const arcRx = 9.15 / len;
    const arcRy = 9.15 / 68;
    const theta = Math.acos(5.5 / 9.15);

    ctx.save();
    ctx.strokeStyle = th.lines;
    ctx.fillStyle = th.lines;
    ctx.lineWidth = 2;

    function drawArcN(cxN, cyN, rxN, ryN, sAng, eAng) {
      ctx.beginPath();
      for (let i = 0; i <= 28; i++) {
        const ang = sAng + (eAng - sAng) * (i / 28);
        const pt = normToCanvas(cxN + Math.cos(ang) * rxN, cyN + Math.sin(ang) * ryN);
        if (i === 0) ctx.moveTo(pt.x, pt.y);
        else ctx.lineTo(pt.x, pt.y);
      }
      ctx.stroke();
    }

    function drawSpotN(nx, ny) {
      const pt = normToCanvas(nx, ny);
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 3, 0, Math.PI * 2);
      ctx.fill();
    }

    // قوس ونقطة جزاء المرمى الأيسر
    drawArcN(spotX, 0.5, arcRx, arcRy, -theta, theta);
    drawSpotN(spotX, 0.5);

    // أقواس الركنيات اليسرى
    const cRx = 1.2 / len, cRy = 1.2 / 68;
    drawArcN(0, 0, cRx, cRy, 0, Math.PI / 2);
    drawArcN(0, 1, cRx, cRy, -Math.PI / 2, 0);

    if (pitchMode === "full") {
      drawSpotN(0.5, 0.5);
      drawArcN(1 - spotX, 0.5, arcRx, arcRy, Math.PI - theta, Math.PI + theta);
      drawSpotN(1 - spotX, 0.5);
      drawArcN(1, 0, cRx, cRy, Math.PI / 2, Math.PI);
      drawArcN(1, 1
