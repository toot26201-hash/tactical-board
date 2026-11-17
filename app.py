import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ProTactics Pro - التحليل التكتيكي المتقدم",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0.3rem 0.5rem 0 0.5rem !important; max-width: 100% !important; }
        header[data-testid="stHeader"], footer { display: none; }
        iframe { border-radius: 12px; border: 1px solid #1e293b; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

with open("engine.js", "r", encoding="utf-8") as f:
    js_code = f.read()

full_page = html_code.replace("<!-- ENGINE_SCRIPT -->", f"<script>\n{js_code}\n</script>")
components.html(full_page, height=820, scrolling=False)
