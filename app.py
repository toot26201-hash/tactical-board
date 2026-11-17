import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="ProTactics - لوحة التحليل التكتيكي", page_icon="⚽", layout="wide")

st.markdown("""
<style>
    .block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
    header[data-testid="stHeader"], footer { display: none; }
</style>
""", unsafe_allow_html=True)

# شريط التحكم العلوي
c1, c2, c3, c4, c5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
with c1:
    st.markdown("### ⚽ ProTactics Pro")
with c2:
    pitch_view = st.selectbox("عرض الملعب", ["ملعب كامل (105×68m)", "نصف ملعب (52.5×68m)"], label_visibility="collapsed")
with c3:
    red_form = st.selectbox("تشكيل الأحمر", ["5-4-1", "4-3-3", "4-2-3-1", "3-5-2", "4-4-2"], label_visibility="collapsed")
with c4:
    blue_form = st.selectbox("تشكيل الأزرق", ["4-3-3", "4-2-3-1", "5-4-1", "3-5-2", "4-4-2"], index=0, label_visibility="collapsed")
with c5:
    show_zones = st.checkbox("5-Zones & Half-spaces", value=False)

FORMATIONS = {
    "5-4-1": [(6,34,"1","GK"),(22,8,"2","RWB"),(20,21,"4","RCB"),(19,34,"5","CB"),(20,47,"6","LCB"),(22,60,"3","LWB"),(35,14,"7","RM"),(34,28,"8","Pivot"),(34,40,"10","Pivot"),(35,54,"11","LM"),(49,34,"9","FWD")],
    "4-3-3": [(6,34,"1","GK"),(22,10,"2","RB"),(20,26,"4","CB"),(20,42,"5","CB"),(22,58,"3","LB"),(34,34,"6","DM"),(40,20,"8","CM"),(40,48,"10","CM"),(48,11,"7","RW"),(50,34,"9","ST"),(48,57,"11","LW")],
    "4-2-3-1": [(6,34,"1","GK"),(22,10,"2","RB"),(20,26,"4","CB"),(20,42,"5","CB"),(22,58,"3","LB"),(33,26,"6","Pivot"),(33,42,"8","Pivot"),(43,12,"7","RW"),(44,34,"10","CAM"),(43,56,"11","LW"),(50,34,"9","ST")],
    "3-5-2": [(6,34,"1","GK"),(20,19,"4","RCB"),(19,34,"5","CB"),(20,49,"6","LCB"),(35,7,"2","RWB"),(32,34,"6","DM"),(37,23,"8","CM"),(37,45,"10","CM"),(35,61,"3","LWB"),(49,26,"9","ST"),(49,42,"11","ST")],
    "4-4-2": [(6,34,"1","GK"),(22,10,"2","RB"),(20,26,"4","CB"),(20,42,"5","CB"),(22,58,"3","LB"),(36,11,"7","RM"),(35,27,"6","CM"),(35,41,"8","CM"),(36,57,"11","LM"),(49,26,"9","ST"),(49,42,"10","ST")]
}

fig = go.Figure()

# رسم خطوط الملعب القانونية (105 × 68 متر)
line_color = "rgba(255,255,255,0.8)"
shapes = [
    dict(type="rect", x0=0, y0=0, x1=105, y1=68, line=dict(color=line_color, width=2.5), fillcolor="#133824", layer="below"),
    dict(type="line", x0=52.5, y0=0, x1=52.5, y1=68, line=dict(color=line_color, width=2)),
    dict(type="circle", x0=52.5-9.15, y0=34-9.15, x1=52.5+9.15, y1=34+9.15, line=dict(color=line_color, width=2)),
    dict(type="rect", x0=0, y0=13.84, x1=16.5, y1=54.16, line=dict(color=line_color, width=2)),
    dict(type="rect", x0=88.5, y0=13.84, x1=105, y1=54.16, line=dict(color=line_color, width=2)),
    dict(type="rect", x0=0, y0=24.84, x1=5.5, y1=43.16, line=dict(color=line_color, width=2)),
    dict(type="rect", x0=99.5, y0=24.84, x1=105, y1=43.16, line=dict(color=line_color, width=2)),
]

# عشب مخطط
for i in range(0, 105, 15):
    shapes.append(dict(type="rect", x0=i, y0=0, x1=min(105, i+7.5), y1=68, fillcolor="rgba(255,255,255,0.03)", line_width=0, layer="below"))

# تقسيمات 5-Zones & Half-spaces
if show_zones:
    for y_line in [13.84, 24.84, 43.16, 54.16]:
        shapes.append(dict(type="line", x0=0, y0=y_line, x1=105, y1=y_line, line=dict(color="rgba(250,204,21,0.55)", width=1.5, dash="dash")))
    shapes.append(dict(type="rect", x0=0, y0=13.84, x1=105, y1=24.84, fillcolor="rgba(250,204,21,0.08)", line_width=0))
    shapes.append(dict(type="rect", x0=0, y0=43.16, x1=105, y1=54.16, fillcolor="rgba(250,204,21,0.08)", line_width=0))

# إضافة لاعبي الفريق الأحمر والأزرق
red_p = FORMATIONS[red_form]
blue_p = [(105 - x, y, n, l) for x, y, n, l in FORMATIONS[blue_form]]

fig.add_trace(go.Scatter(
    x=[p[0] for p in red_p], y=[p[1] for p in red_p], mode="markers+text",
    marker=dict(size=28, color="#dc2626", line=dict(color="white", width=2)),
    text=[f"<b>{p[2]}</b><br><span style='font-size:10px'>{p[3]}</span>" for p in red_p],
    textposition="middle center", textfont=dict(color="white", size=11), name="الفريق الأحمر"
))

fig.add_trace(go.Scatter(
    x=[p[0] for p in blue_p], y=[p[1] for p in blue_p], mode="markers+text",
    marker=dict(size=28, color="#0284c7", line=dict(color="white", width=2)),
    text=[f"<b>{p[2]}</b><br><span style='font-size:10px'>{p[3]}</span>" for p in blue_p],
    textposition="middle center", textfont=dict(color="white", size=11), name="الفريق الأزرق"
))

# الكرة
fig.add_trace(go.Scatter(x=[52.5], y=[34], mode="markers", marker=dict(size=14, color="white", line=dict(color="black", width=2)), name="الكرة"))

x_range = [-2, 107] if "كامل" in pitch_view else [-2, 54]
fig.update_layout(
    shapes=shapes,
    xaxis=dict(range=x_range, showgrid=False, zeroline=False, visible=False),
    yaxis=dict(range=[-2, 70], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
    paper_bgcolor="#0b0f19", plot_bgcolor="#0d2618",
    margin=dict(l=10, r=10, t=10, b=10), height=640, showlegend=False,
    dragmode="drawline",
    newshape=dict(line=dict(color="#facc15", width=3))
)

st.plotly_chart(fig, use_container_width=True, config={
    "displayModeBar": True,
    "modeBarButtonsToAdd": ["drawline", "drawopenpath", "drawclosedpath", "drawcircle", "drawrect", "eraseshape"],
    "toImageButtonOptions": {"format": "png", "filename": "tactical_board", "scale": 2}
})
