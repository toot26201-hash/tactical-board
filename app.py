import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ProTactics", page_icon="⚽", layout="wide")
st.markdown("<style>.block-container{padding:0.3rem!important;max-width:100%!important;}header,footer{display:none;}iframe{width:100%!important;border:none;}</style>", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read().split("<script>")[0]

with open("board.js", "r", encoding="utf-8") as f:
    js = f.read().rsplit(";", 1)[0]

# إلحاق الجافاسكريبت مباشرة في نهاية HTML دون البحث عن </body>
full_html = f"{html}\n<script>\n{js};\ninitDefaultPieces();\nresizeCanvas();\nwindow.addEventListener('resize', resizeCanvas);\n</script>\n</body></html>"

components.html(full_html, height=740, scrolling=False)
