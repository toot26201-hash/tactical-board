import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ProTactics", page_icon="⚽", layout="wide")
st.markdown("<style>.block-container{padding:0.3rem!important;max-width:100%!important;}header,footer{display:none;}iframe{width:100%!important;border:none;}</style>", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("board.js", "r", encoding="utf-8") as f:
    js = f.read()

if "<script>" in html:
    html = html.split("<script>")[0] + "</body></html>"

# التأكد من أن نهاية الجافاسكريبت تعمل حتى لو انقطعت أثناء اللصق
safe_js = js.rsplit(";", 1)[0] + ";\ninitDefaultPieces(); resizeCanvas(); window.addEventListener('resize', resizeCanvas);"

components.html(html.replace("</body>", f"<script>{safe_js}</script></body>"), height=740, scrolling=False)
