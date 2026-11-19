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

# سكريبت ذكي لضبط ارتفاع الـ iframe تلقائياً: 1650px لصفحة الهبوط، و 100vh للسبورة بدون فراغ
auto_height_script = """
<script>
(function() {
    function syncIframeHeight() {
        const iframe = window.frameElement;
        if (!iframe) return;
        const landing = document.getElementById("landing-page");
        const isLandingVisible = landing && !landing.classList.contains("hidden");
        if (isLandingVisible) {
            iframe.style.height = "1650px";
        } else {
            iframe.style.height = "100vh";
            if (typeof resizeCanvas === "function") resizeCanvas();
        }
    }
    setInterval(syncIframeHeight, 300);
    window.addEventListener("load", syncIframeHeight);
})();
</script>
</body>
"""

html_code = html_code.replace("</body>", auto_height_script)

components.html(html_code, height=1650, scrolling=False)
