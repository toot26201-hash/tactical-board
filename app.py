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
html_code = html_code.replace(
    '<option value="4-3-3">4-3-3</option>',
    '<option value="4-3-3">4-3-3</option><option value="4-1-4-1">4-1-4-1</option>'
)
tpl_4141 = '"4-1-4-1":[{nx:0.06,ny:0.5,num:"1",label:"GK"},{nx:0.21,ny:0.15,num:"3",label:"LB"},{nx:0.19,ny:0.38,num:"4",label:"CB"},{nx:0.19,ny:0.62,num:"5",label:"CB"},{nx:0.21,ny:0.85,num:"2",label:"RB"},{nx:0.29,ny:0.5,num:"6",label:"DM"},{nx:0.39,ny:0.15,num:"11",label:"LM"},{nx:0.38,ny:0.38,num:"8",label:"CM"},{nx:0.38,ny:0.62,num:"10",label:"CM"},{nx:0.39,ny:0.85,num:"7",label:"RM"},{nx:0.48,ny:0.5,num:"9",label:"ST"}],'
html_code = html_code.replace('"4-3-3":[', tpl_4141 + '"4-3-3":[')

# 2. إضافة أزرار تغيير لون الأرقام (#) ولون الأسماء (A) لكل فريق في الشريط العلوي
html_code = html_code.replace(
    '<input type="color" id="quick-red-secondary" value="#ffffff" onchange="quickKitUpdate(\'red\')" class="w-5 h-5 cursor-pointer bg-transparent">',
    '''<input type="color" id="quick-red-secondary" value="#ffffff" onchange="quickKitUpdate('red')" title="اللون الثانوي للطقم" class="w-5 h-5 cursor-pointer bg-transparent">
        <label title="لون أرقام الفريق الأول" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">#<input type="color" id="quick-red-numcolor" value="#ffffff" onchange="quickTeamTextColor('red','num',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>
        <label title="لون أسماء الفريق الأول" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">A<input type="color" id="quick-red-lblcolor" value="#f8fafc" onchange="quickTeamTextColor('red','label',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>'''
)

html_code = html_code.replace(
    '<input type="color" id="quick-blue-secondary" value="#ffffff" onchange="quickKitUpdate(\'blue\')" class="w-5 h-5 cursor-pointer bg-transparent">',
    '''<input type="color" id="quick-blue-secondary" value="#ffffff" onchange="quickKitUpdate('blue')" title="اللون الثانوي للطقم" class="w-5 h-5 cursor-pointer bg-transparent">
        <label title="لون أرقام الفريق الثاني" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">#<input type="color" id="quick-blue-numcolor" value="#ffffff" onchange="quickTeamTextColor('blue','num',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>
        <label title="لون أسماء الفريق الثاني" class="flex items-center bg-slate-800 border border-slate-700 rounded px-1 cursor-pointer text-[10px] text-slate-300 font-en">A<input type="color" id="quick-blue-lblcolor" value="#f8fafc" onchange="quickTeamTextColor('blue','label',this.value)" class="w-3.5 h-4 cursor-pointer bg-transparent border-0 p-0"></label>'''
)

# 3. إضافة خيار لون الرقم ولون الاسم داخل نافذة تعديل اللاعب الفردي (Double Click)
old_edit_modal = '<input type="color" id="edit-custom-color" value="#eab308" class="w-6 h-5 cursor-pointer bg-transparent">\n    </div>'
new_edit_modal = '''<input type="color" id="edit-custom-color" value="#eab308" class="w-6 h-5 cursor-pointer bg-transparent">
    </div>
    <div class="grid grid-cols-2 gap-1.5">
      <div class="flex items-center justify-between bg-slate-900 border border-slate-700 rounded px-2 py-1">
        <span class="text-[11px] text-slate-300">لون الرقم</span>
        <input type="color" id="edit-num-color" value="#ffffff" class="w-5 h-5 cursor-pointer bg-transparent">
      </div>
      <div class="flex items-center justify-between bg-slate-900 border border-slate-700 rounded px-2 py-1">
        <span class="text-[11px] text-slate-300">لون الاسم</span>
        <input type="color" id="edit-label-color" value="#f8fafc" class="w-5 h-5 cursor-pointer bg-transparent">
      </div>
    </div>'''
html_code = html_code.replace(old_edit_modal, new_edit_modal)

# 4. دالة التحديث الجماعي للفريق + تحميل وحفظ ألوان اللاعب الفردي
team_color_fn = '''function quickTeamTextColor(team, target, color) {
  saveHistory();
  const meta = team === "red" ? redTeamMeta : blueTeamMeta;
  if (target === "num") meta.numColor = color;
  else meta.labelColor = color;
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

html_code = html_code.replace(
    'document.getElementById("edit-spotlight").checked=!!hit.spotlight;',
    'document.getElementById("edit-spotlight").checked=!!hit.spotlight;const m=hit.type==="red"?redTeamMeta:blueTeamMeta;document.getElementById("edit-num-color").value=hit.numColor||m.numColor||"#ffffff";document.getElementById("edit-label-color").value=hit.labelColor||m.labelColor||"#f8fafc";'
)
html_code = html_code.replace(
    'p.spotlight=document.getElementById("edit-spotlight").checked;',
    'p.spotlight=document.getElementById("edit-spotlight").checked;p.numColor=document.getElementById("edit-num-color").value;p.labelColor=document.getElementById("edit-label-color").value;'
)

# 5. الحفاظ على ألوان الفريق عند تغيير التشكيلة الفوري
html_code = html_code.replace(
    'customColor:ex[i]?ex[i].customColor:null',
    'customColor:ex[i]?ex[i].customColor:null,numColor:ex[i]?.numColor||(team==="red"?redTeamMeta.numColor:blueTeamMeta.numColor)||"#ffffff",labelColor:ex[i]?.labelColor||(team==="red"?redTeamMeta.labelColor:blueTeamMeta.labelColor)||"#f8fafc"'
)

# 6. تطبيق ألوان الرقم والاسم أثناء رسم اللاعبين على الملعب
html_code = html_code.replace(
    'ctx.fillStyle="#fff";ctx.fillText(p.number||"",pos.x,pos.y);',
    'ctx.fillStyle=p.numColor||meta.numColor||"#ffffff";ctx.fillText(p.number||"",pos.x,pos.y);'
)
html_code = html_code.replace(
    'ctx.fillStyle="#f8fafc";ctx.fillText(p.label,pos.x,pos.y+r+10);',
    'ctx.fillStyle=p.labelColor||meta.labelColor||"#f8fafc";ctx.fillText(p.label,pos.x,pos.y+r+10);'
)

components.html(html_code, height=1750, scrolling=False)
