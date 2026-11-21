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
        header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
        iframe { width: 100% !important; border: none !important; display: block !important; }
    </style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

silent_hd_upgrade = """
<script>
(function silentProUpgrades() {
  // حذف أي شريط عائم قديم تماماً
  ["clean-pro-bottom-bar", "pro-tactics-master-dock", "custom-equip-dock", "player-size-control-box", "btn-export-1080p-global", "btn-top3d-cam"].forEach(id => {
    document.querySelectorAll("#" + id).forEach(el => el.remove());
  });

  // رفع جودة تسجيل MediaRecorder تلقائياً إلى 12 Mbps (Full HD) عند استخدام زرار "فيديو" الأصلي في الموقع
  if (typeof MediaRecorder !== "undefined") {
    const OrigMediaRecorder = window.MediaRecorder;
    window.MediaRecorder = function (stream, options) {
      const upgradedOptions = Object.assign({}, options || {}, {
        videoBitsPerSecond: 12000000
      });
      return new OrigMediaRecorder(stream, upgradedOptions);
    };
    window.MediaRecorder.prototype = OrigMediaRecorder.prototype;
    window.MediaRecorder.isTypeSupported = OrigMediaRecorder.isTypeSupported.bind(OrigMediaRecorder);
  }
})();
</script>
"""

if "silentProUpgrades" not in html_code:
    html_code = html_code + silent_hd_upgrade

components.html(html_code, height=1750, scrolling=False)
