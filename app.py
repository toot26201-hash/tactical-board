import streamlit as st

st.set_page_config(page_title="ProTactics Studio", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #e2e8f0; }
    h1 { color: #facc15; font-family: 'Cairo', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ ProTactics Studio - لوحة التحليل التكتيكي")
st.write("مرحباً بك يا محمود! هذا تطبيق بايثون المخصص لإدارة الوحدات التدريبية وتحليل المباريات.")

# لوحة تحكم بسيطة لتجربة الأدوات والتشكيلات
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("إعدادات الفريق والملعب")
    team_name = st.text_input("اسم الفريق", "الفريق الأول")
    formation = st.selectbox("الخطة التكتيكية", ["5-4-1", "4-3-3", "4-2-3-1", "3-5-2"])
    pitch_mode = st.radio("وضع الملعب", ["ملعب كامل", "نصف ملعب"])
    
    st.markdown("### أدوات التدريب والتميز")
    spotlight_player = st.checkbox("✨ تفعيل حلقة التمييز (Spotlight Pulse)")
    add_cone = st.checkbox("+ إضافة أقماع تدريبية")
    add_mannequin = st.checkbox("+ إضافة دمى دفاعية")
    add_minigoal = st.checkbox("+ إضافة مرمى صغير")

with col2:
    st.info(f"جاري عرض الملعب الحالي لخطة **{formation}** وفريق **{team_name}** ({pitch_mode}).")
    # محاكاة عرض الملعب التكتيكي
    st.image("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=80&w=1000&auto=format&fit=crop", caption="ProTactics Studio Pitch View")
