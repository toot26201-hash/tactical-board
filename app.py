import re
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

# 1. إضافة تشكيلة 4-1-4-1
if '<option value="4-1-4-1">4-1-4-1</option>' not in html_code:
    html_code = html_code.replace(
        '<option value="4-3-3">4-3-3</option>',
        '<option value="4-3-3">4-3-3</option><option value="4-1-4-1">4-1-4-1</option>'
    )

tpl_4141 = '"4-1-4-1":[{nx:0.06,ny:0.5,num:"1",label:"GK"},{nx:0.21,ny:0.15,num:"3",label:"LB"},{nx:0.19,ny:0.38,num:"4",label:"CB"},{nx:0.19,ny:0.62,num:"5",label:"CB"},{nx:0.21,ny:0.85,num:"2",label:"RB"},{nx:0.29,ny:0.5,num:"6",label:"DM"},{nx:0.39,ny:0.15,num:"11",label:"LM"},{nx:0.38,ny:0.38,num:"8",label:"CM"},{nx:0.38,ny:0.62,num:"10",label:"CM"},{nx:0.39,ny:0.85,num:"7",label:"RM"},{nx:0.48,ny:0.5,num:"9",label:"ST"}],'
if '"4-1-4-1":[' not in html_code:
    html_code = html_code.replace('"4-3-3":[', tpl_4141 + '"4-3-3":[')

# 2. إضافة أزرار تغيير لون الأرقام (#) والأسماء (A) لكل فريق في الشريط العلوي
if 'id="quick-red-numcolor"' not in html_code:
    html_code = html_code.replace(
        '<input type="color" id="quick-red-secondary" value="#ffffff" onchange="quickKitUpdate(\'red\')" title="اللون الثانوي للطقم" class="w-5 h-5 cursor-pointer bg-transparent">',
        '''<input type="color" id="quick-red-secondary" value="#ffffff" onchange="quickKitUpdate('red')" title="اللون الثانوي للطقم" class="w-5 h-5 cursor-pointer bg-transparent">
        <label title="لون أرقام الفريق الأول" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">#<input type="color" id="quick-red-numcolor" value="#ffffff" onchange="quickTeamTextColor('red','num',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>
        <label title="لون أسماء الفريق الأول" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">A<input type="color" id="quick-red-lblcolor" value="#f8fafc" onchange="quickTeamTextColor('red','label',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>'''
    )

if 'id="quick-blue-numcolor"' not in html_code:
    html_code = html_code.replace(
        '<input type="color" id="quick-blue-secondary" value="#ffffff" onchange="quickKitUpdate(\'blue\')" title="اللون الثانوي للطقم" class="w-5 h-5 cursor-pointer bg-transparent">',
        '''<input type="color" id="quick-blue-secondary" value="#ffffff" onchange="quickKitUpdate('blue')" title="اللون الثانوي للطقم" class="w-5 h-5 cursor-pointer bg-transparent">
        <label title="لون أرقام الفريق الثاني" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">#<input type="color" id="quick-blue-numcolor" value="#ffffff" onchange="quickTeamTextColor('blue','num',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>
        <label title="لون أسماء الفريق الثاني" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">A<input type="color" id="quick-blue-lblcolor" value="#f8fafc" onchange="quickTeamTextColor('blue','label',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>'''
    )

# 3. إضافة خيار لون الرقم ولون الاسم داخل نافذة تعديل اللاعب الفردي
if 'id="edit-num-color"' not in html_code:
    target_modal_end = '<label class="flex items-center gap-1.5 text-xs text-amber-300"><input type="checkbox" id="edit-spotlight"> حلقة تمييز</label>'
    color_inputs_html = '''<div class="grid grid-cols-2 gap-1.5">
      <div class="flex items-center justify-between bg-slate-900 border border-slate-700 rounded px-2 py-1">
        <span class="text-[11px] text-slate-300">لون الرقم</span>
        <input type="color" id="edit-num-color" value="#ffffff" class="w-5 h-5 cursor-pointer bg-transparent">
      </div>
      <div class="flex items-center justify-between bg-slate-900 border border-slate-700 rounded px-2 py-1">
        <span class="text-[11px] text-slate-300">لون الاسم</span>
        <input type="color" id="edit-label-color" value="#f8fafc" class="w-5 h-5 cursor-pointer bg-transparent">
      </div>
    </div>
    ''' + target_modal_end
    html_code = html_code.replace(target_modal_end, color_inputs_html)

# 4. دالة التحديث الجماعي للفريق
if 'function quickTeamTextColor(' not in html_code:
    team_color_fn = '''function quickTeamTextColor(team, target, color) {
  saveHistory();
  const _meta = team === "red" ? redTeamMeta : blueTeamMeta;
  if (target === "num") _meta.numColor = color;
  else _meta.labelColor = color;
  pieces.forEach(p => {
    if (p.type === team) {
      if (target === "num") p.numColor = color;
      else p.labelColor = color;
    }
  });
  syncCurrentFrame();
  render();
}
function quickKitUpdate('''
    html_code = html_code.replace('function quickKitUpdate(', team_color_fn)

# 5. تحديث دالة saveEditModal بأمان
old_save_edit = 'function saveEditModal(){const p=pieces.find(x=>x.id===editingPieceId);if(p){saveHistory();p.number=document.getElementById("edit-number").value;p.label=document.getElementById("edit-label").value;p.customColor=document.getElementById("edit-use-custom-color").checked?document.getElementById("edit-custom-color").value:null;p.spotlight=document.getElementById("edit-spotlight").checked;syncCurrentFrame();render();}closeEditModal();}'
new_save_edit = 'function saveEditModal(){const p=pieces.find(x=>x.id===editingPieceId);if(p){saveHistory();p.number=document.getElementById("edit-number").value;p.label=document.getElementById("edit-label").value;p.customColor=document.getElementById("edit-use-custom-color").checked?document.getElementById("edit-custom-color").value:null;p.spotlight=document.getElementById("edit-spotlight").checked;const nc=document.getElementById("edit-num-color");const lc=document.getElementById("edit-label-color");if(nc)p.numColor=nc.value;if(lc)p.labelColor=lc.value;syncCurrentFrame();render();}closeEditModal();}'
html_code = html_code.replace(old_save_edit, new_save_edit)

# 6. تطبيق ألوان الرقم والاسم أثناء رسم اللاعبين على الملعب
html_code = html_code.replace(
    'ctx.fillStyle="#fff";ctx.fillText(p.number||"",pos.x,pos.y);',
    'ctx.fillStyle=p.numColor||meta.numColor||"#ffffff";ctx.fillText(p.number||"",pos.x,pos.y);'
)
html_code = html_code.replace(
    'ctx.fillStyle="#f8fafc";ctx.fillText(p.label,pos.x,pos.y+r+10);',
    'ctx.fillStyle=p.labelColor||meta.labelColor||"#f8fafc";ctx.fillText(p.label,pos.x,pos.y+r+10);'
)

# 7. إضافة وضع "تدريب"
if 'id="btn-pitch-training"' not in html_code:
    html_code = html_code.replace(
        '<button onclick="setPitchMode(\'half\')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 px-2 py-0.5 rounded">نصف</button>',
        '<button onclick="setPitchMode(\'half\')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 px-2 py-0.5 rounded">نصف</button><button onclick="activateTrainingPitch()" id="btn-pitch-training" class="pitch-mode-btn text-emerald-300 px-2 py-0.5 rounded">تدريب</button>'
    )

if 'function activateTrainingPitch(' not in html_code:
    training_fn = '''function activateTrainingPitch() {
  saveHistory();
  drawings = [];
  links = [];
  pieces = [{ id: "ball_1", type: "ball", nx: 0.5, ny: 0.5, number: "", label: "" }];
  document.querySelectorAll(".pitch-mode-btn").forEach(b => b.classList.remove("bg-slate-700", "text-white"));
  const tBtn = document.getElementById("btn-pitch-training");
  if (tBtn) tBtn.classList.add("bg-slate-700", "text-white");
  syncCurrentFrame();
  render();
  showToast("تم تجهيز ملعب التدريب — أضف الأقماع واللاعبين حسب الدريل");
}
function setPitchMode('''
    html_code = html_code.replace('function setPitchMode(', training_fn)

# 8. منع خطأ تكرار تعريف المتغير m في الـ JavaScript
m_matches = list(re.finditer(r'\b(const|let|var)\s+m\b', html_code))
if len(m_matches) > 1:
    for match in m_matches[1:]:
        start, end = match.span(0)
        kw = match.group(1)
        html_code = html_code[:start] + f"{kw} _m_dup" + html_code[end:]

components.html(html_code, height=1750, scrolling=False)
