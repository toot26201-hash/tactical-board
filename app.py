from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ProTactics Board | لوحة التحليل التكتيكي",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {
            padding: 0.5rem 0.5rem 0rem 0.5rem;
            max-width: 100%;
        }
        iframe {
            border-radius: 12px;
            border: 1px solid #334155;
        }
    </style>
""", unsafe_allow_html=True)

html_content = Path("index.html").read_text(encoding="utf-8")
components.html(html_content, height=740, scrolling=False)
