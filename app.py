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
        header, footer, #MainMenu { visibility: hidden; }
        iframe { width: 100% !important; height: 100vh !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=850, scrolling=False)
