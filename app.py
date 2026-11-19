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
        html, body, [data-testid="stAppViewContainer"], .main {
            overflow: hidden !important;
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            height: 100vh !important;
        }
        header, footer, #MainMenu { visibility: hidden; display: none !important; }
        iframe {
            width: 100% !important;
            height: 100vh !important;
            border: none !important;
            display: block !important;
        }
    </style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=900, scrolling=True)
