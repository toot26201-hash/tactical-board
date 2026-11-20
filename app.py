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

# تنظيف أي إضافات تجريبية سابقة
html_code = re.sub(r'<button onclick="activateTrainingPitch\(\)"[^>]*>تدريب</button>', '', html_code)
html_code = re.sub(r'<button onclick="loadHalfSpaceBuildUpDrill\(\)"[^>]*>.*?</button>', '', html_code)
html_code = re.sub(r'<script>[\s\S]*?__renderGuaranteedPitch[\s\S]*?</script>', '', html_code)
html_code = re.sub(r'<script>[\s\S]*?loadHalfSpaceBuildUpDrill[\s\S]*?</script>', '', html_code)
html_code = re.sub(r'<style>\s*#auth-modal[\s\S]*?</style>', '', html_code)
html_code = re.sub(r'<script>[\s\S]*?__bypassLoginAndEnterBoard[\s\S]*?</script>', '', html_code)

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

# 4. إصلاح بلوك dblclick التالف في index.html
clean_dblclick = '''canvas.addEventListener("dblclick",e=>{const pos=getPointerPos(e),hit=[...pieces].reverse().find(p=>{const c=normToCanvas(p.nx,p.ny);return Math.hypot(pos.x-c.x,pos.y-c.y)<=22;});if(hit){editingPieceId=hit.id;document.getElementById("edit-number").value=hit.number||"";document.getElementById("edit-label").value=hit.label||"";document.getElementById("edit-use-custom-color").checked=!!hit.customColor;document.getElementById("edit-custom-color").value=hit.customColor||"#eab308";document.getElementById("edit-spotlight").checked=!!hit.spotlight;const __tm=hit.type==="red"?redTeamMeta:blueTeamMeta;const __nc=document.getElementById("edit-num-color");const __lc=document.getElementById("edit-label-color");if(__nc)__nc.value=hit.numColor||(__tm&&__tm.numColor)||"#ffffff";if(__lc)__lc.value=hit.labelColor||(__tm&&__tm.labelColor)||"#f8fafc";document.getElementById("edit-modal").classList.remove("hidden");}});'''
html_code = re.sub(
    r'canvas\.addEventListener\(\s*["\']dblclick["\'][\s\S]*?edit-modal[\s\S]*?\}\s*\)\s*;',
    clean_dblclick,
    html_code,
    count=1
)

# 5. تفادي ReferenceError الخاص بـ m داخل resizeCanvas
if 'window.__safe_m' not in html_code:
    html_code = re.sub(
        r'(function\s+resizeCanvas\s*\([^)]*\)\s*\{)',
        r'\1const m=window.__safe_m||(window.__safe_m={});',
        html_code,
        count=1
    )

# 6. دالة التحديث الجماعي للفريق
if 'function quickTeamTextColor(' not in html_code:
    team_color_fn = '''function quickTeamTextColor(team, target, color) {
  saveHistory();
  const __teamMeta = team === "red" ? redTeamMeta : blueTeamMeta;
  if (target === "num") __teamMeta.numColor = color;
  else __teamMeta.labelColor = color;
  pieces.forEach(p => {
    if (p.type === team) {
      if (target === "num") p.numColor = color;
      else p.labelColor = color;
    }
  });
  syncCurrentFrame();
  if (typeof render === "function") render();
}
function quickKitUpdate('''
    html_code = html_code.replace('function quickKitUpdate(', team_color_fn)

# 7. تحديث دالة saveEditModal بأمان
old_save_edit = 'function saveEditModal(){const p=pieces.find(x=>x.id===editingPieceId);if(p){saveHistory();p.number=document.getElementById("edit-number").value;p.label=document.getElementById("edit-label").value;p.customColor=document.getElementById("edit-use-custom-color").checked?document.getElementById("edit-custom-color").value:null;p.spotlight=document.getElementById("edit-spotlight").checked;syncCurrentFrame();render();}closeEditModal();}'
new_save_edit = 'function saveEditModal(){const p=pieces.find(x=>x.id===editingPieceId);if(p){saveHistory();p.number=document.getElementById("edit-number").value;p.label=document.getElementById("edit-label").value;p.customColor=document.getElementById("edit-use-custom-color").checked?document.getElementById("edit-custom-color").value:null;p.spotlight=document.getElementById("edit-spotlight").checked;const __nc=document.getElementById("edit-num-color");const __lc=document.getElementById("edit-label-color");if(__nc)p.numColor=__nc.value;if(__lc)p.labelColor=__lc.value;syncCurrentFrame();if(typeof render==="function")render();}closeEditModal();}'
html_code = html_code.replace(old_save_edit, new_save_edit)

# 8. إضافة زر "وضع التدريب" في الشريط العلوي
if 'id="btn-open-training-studio"' not in html_code:
    html_code = html_code.replace(
        '<button onclick="setPitchMode(\'half\')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 px-2 py-0.5 rounded">نصف</button>',
        '<button onclick="setPitchMode(\'half\')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 px-2 py-0.5 rounded">نصف</button><button onclick="openTrainingStudio()" id="btn-open-training-studio" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-2.5 py-0.5 rounded font-semibold mr-1">⚽ وضع التدريب</button>'
    )

# 9. استوديو التدريب المستقل مع الإبقاء على نظام تسجيل الدخول فعالاً
training_studio_module = """
<style>
  #toot-training-studio {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: #0b1120;
    color: #f8fafc;
    display: none;
    flex-direction: column;
    font-family: system-ui, -apple-system, sans-serif;
  }
  #toot-training-studio.active {
    display: flex;
  }
</style>

<div id="toot-training-studio" dir="rtl">
  <div class="flex items-center justify-between px-4 py-2.5 bg-slate-900 border-b border-slate-800">
    <div class="flex items-center gap-3">
      <button onclick="closeTrainingStudio()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-3 py-1.5 rounded-lg border border-slate-700">
        → العودة للسبورة التكتيكية
      </button>
      <span class="text-sm font-bold text-emerald-400">ProTactics Training Studio</span>
      <span class="text-xs text-slate-400">| TootScouting</span>
    </div>

    <div class="flex items-center gap-2">
      <button onclick="loadDrillPreset('squares5v5')" class="bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/40 text-xs px-2.5 py-1 rounded">
        قالب 5v5 المربعات
      </button>
      <button onclick="loadDrillPreset('halfspaces')" class="bg-sky-600/20 hover:bg-sky-600/30 text-sky-300 border border-sky-500/40 text-xs px-2.5 py-1 rounded">
        قالب Build-up Half-Spaces
      </button>
      <button onclick="tsClearBoard()" class="bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/40 text-xs px-2.5 py-1 rounded">
        مسح الكل
      </button>
    </div>
  </div>

  <div class="flex flex-wrap items-center gap-3 px-4 py-2 bg-slate-900/70 border-b border-slate-800 text-xs">
    <div class="flex items-center gap-1.5">
      <span class="text-slate-400">عنوان الدريل:</span>
      <input id="ts-title" type="text" value="Creating space through movement in 5v5" oninput="tsDraw()" class="bg-slate-800 border border-slate-700 rounded px-2.5 py-1 text-slate-100 w-72">
    </div>
    <div class="flex items-center gap-1.5">
      <span class="text-slate-400">المدة:</span>
      <input id="ts-duration" type="text" value="20 min" oninput="tsDraw()" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-100 w-20 text-center">
    </div>
    <div class="flex items-center gap-1.5">
      <span class="text-slate-400">العدد:</span>
      <input id="ts-players-count" type="text" value="10-20 players" oninput="tsDraw()" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-100 w-28 text-center">
    </div>
    <div class="flex items-center gap-1.5">
      <span class="text-slate-400">التصنيف:</span>
      <input id="ts-category" type="text" value="Small-sided games" oninput="tsDraw()" class="bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-100 w-36 text-center">
    </div>
  </div>

  <div class="flex flex-1 overflow-hidden">
    <div class="w-56 bg-slate-900 border-l border-slate-800 p-3 flex flex-col gap-2.5 overflow-y-auto text-xs">
      <div class="text-slate-400 font-semibold">أدوات الرسم والحركة</div>
      <div class="grid grid-cols-2 gap-1.5">
        <button id="ts-tool-move" onclick="tsSetTool('move')" class="ts-tool-btn bg-blue-600 text-white py-1.5 rounded font-medium">تحريك</button>
        <button id="ts-tool-pass" onclick="tsSetTool('pass')" class="ts-tool-btn bg-slate-800 text-slate-200 py-1.5 rounded">سهم تمرير</button>
        <button id="ts-tool-run" onclick="tsSetTool('run')" class="ts-tool-btn bg-slate-800 text-slate-200 py-1.5 rounded">سهم جري</button>
        <button id="ts-tool-dribble" onclick="tsSetTool('dribble')" class="ts-tool-btn bg-slate-800 text-slate-200 py-1.5 rounded">مراوغة</button>
      </div>

      <div class="text-slate-400 font-semibold mt-1">مربعات الأقماع الملوّنة</div>
      <div class="grid grid-cols-2 gap-1.5">
        <button onclick="tsAddConeZone('#facc15')" class="bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-300 border border-yellow-500/40 py-1.5 rounded">+ مربع أصفر</button>
        <button onclick="tsAddConeZone('#38bdf8')" class="bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 border border-sky-500/40 py-1.5 rounded">+ مربع أزرق</button>
        <button onclick="tsAddConeZone('#f87171')" class="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/40 py-1.5 rounded">+ مربع أحمر</button>
        <button onclick="tsAddConeZone('#ffffff')" class="bg-slate-700/60 hover:bg-slate-700 text-slate-200 border border-slate-500/40 py-1.5 rounded">+ مربع أبيض</button>
      </div>
      <button onclick="tsToggleLastZoneGlow()" class="bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 py-1.5 rounded">
        ✨ تبديل إضاءة المربع المحدد
      </button>

      <div class="text-slate-400 font-semibold mt-1">اللاعبون والكرات</div>
      <div class="grid grid-cols-2 gap-1.5">
        <button onclick="tsAddPlayer('blue')" class="bg-blue-700 hover:bg-blue-600 text-white py-1.5 rounded">+ لاعب أزرق</button>
        <button onclick="tsAddPlayer('yellow')" class="bg-amber-600 hover:bg-amber-500 text-white py-1.5 rounded">+ لاعب أصفر</button>
        <button onclick="tsAddPlayer('red')" class="bg-red-700 hover:bg-red-600 text-white py-1.5 rounded">+ لاعب أحمر</button>
        <button onclick="tsAddBall()" class="bg-slate-700 hover:bg-slate-600 text-white py-1.5 rounded">+ كرة</button>
      </div>

      <div class="text-slate-400 font-semibold mt-1">الأنيميشن والتصدير</div>
      <div class="grid grid-cols-2 gap-1.5">
        <button onclick="tsAddKeyframe()" class="bg-indigo-600 hover:bg-indigo-500 text-white py-1.5 rounded font-medium">+ لقطة حركة</button>
        <button id="ts-play-btn" onclick="tsTogglePlay()" class="bg-emerald-600 hover:bg-emerald-500 text-white py-1.5 rounded font-medium">▶ تشغيل</button>
      </div>
      <div id="ts-frames-bar" class="flex flex-wrap gap-1 mt-1"></div>
      <button onclick="tsExportPNG()" class="mt-auto bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 py-1.5 rounded">
        📷 حفظ صورة PNG
      </button>
    </div>

    <div class="flex-1 flex items-center justify-center p-4 bg-slate-950">
      <canvas id="ts-canvas" class="rounded-xl shadow-2xl border border-slate-800 max-w-full max-h-full cursor-pointer"></canvas>
    </div>
  </div>
</div>

<script>
const tsState = {
  tool: 'move',
  zones: [],
  players: [],
  arrows: [],
  keyframes: [],
  currentFrame: 0,
  selectedZoneId: null,
  dragging: null,
  drawingArrow: null,
  playing: false,
  playTimer: null
};

function openTrainingStudio() {
  const el = document.getElementById('toot-training-studio');
  if (!el) return;
  el.classList.add('active');
  if (tsState.zones.length === 0 && tsState.players.length === 0) {
    loadDrillPreset('squares5v5');
  } else {
    tsResize();
    tsDraw();
  }
}

function closeTrainingStudio() {
  if (tsState.playing) tsTogglePlay();
  const el = document.getElementById('toot-training-studio');
  if (el) el.classList.remove('active');
}

function tsSetTool(t) {
  tsState.tool = t;
  document.querySelectorAll('.ts-tool-btn').forEach(b => {
    b.classList.remove('bg-blue-600', 'text-white');
    b.classList.add('bg-slate-800', 'text-slate-200');
  });
  const activeBtn = document.getElementById('ts-tool-' + t);
  if (activeBtn) {
    activeBtn.classList.remove('bg-slate-800', 'text-slate-200');
    activeBtn.classList.add('bg-blue-600', 'text-white');
  }
}

function tsResize() {
  const cvs = document.getElementById('ts-canvas');
  if (!cvs || !cvs.parentElement) return;
  const r = cvs.parentElement.getBoundingClientRect();
  cvs.width = Math.max(760, Math.floor(r.width - 32));
  cvs.height = Math.max(460, Math.floor(r.height - 32));
}

function tsAddConeZone(color) {
  const id = 'z_' + Date.now() + Math.random().toString(36).slice(2, 5);
  tsState.zones.push({ id, x: 0.42, y: 0.40, w: 0.14, h: 0.18, color, glow: false });
  tsState.selectedZoneId = id;
  tsDraw();
}

function tsToggleLastZoneGlow() {
  const z = tsState.zones.find(item => item.id === tsState.selectedZoneId) || tsState.zones[tsState.zones.length - 1];
  if (z) {
    z.glow = !z.glow;
    tsDraw();
  }
}

function tsAddPlayer(team) {
  const count = tsState.players.filter(p => p.team === team).length + 1;
  tsState.players.push({
    id: 'p_' + Date.now() + Math.random().toString(36).slice(2, 5),
    team,
    num: String(count),
    x: 0.35 + Math.random() * 0.3,
    y: 0.35 + Math.random() * 0.3
  });
  tsDraw();
}

function tsAddBall() {
  tsState.players.push({
    id: 'b_' + Date.now() + Math.random().toString(36).slice(2, 5),
    team: 'ball',
    num: '',
    x: 0.5,
    y: 0.5
  });
  tsDraw();
}

function tsClearBoard() {
  if (tsState.playing) tsTogglePlay();
  tsState.zones = [];
  tsState.players = [];
  tsState.arrows = [];
  tsState.keyframes = [];
  tsState.currentFrame = 0;
  tsRenderFramesBar();
  tsDraw();
}

function loadDrillPreset(type) {
  if (tsState.playing) tsTogglePlay();
  tsState.arrows = [];
  if (type === 'squares5v5') {
    document.getElementById('ts-title').value = 'Creating space through movement in 5v5';
    document.getElementById('ts-duration').value = '20 min';
    document.getElementById('ts-players-count').value = '10-20 players';
    document.getElementById('ts-category').value = 'Small-sided games';

    tsState.zones = [
      { id: 'z1', x: 0.24, y: 0.22, w: 0.11, h: 0.15, color: '#facc15', glow: false },
      { id: 'z2', x: 0.44, y: 0.22, w: 0.11, h: 0.15, color: '#38bdf8', glow: false },
      { id: 'z3', x: 0.64, y: 0.22, w: 0.11, h: 0.15, color: '#facc15', glow: true },
      { id: 'z4', x: 0.24, y: 0.43, w: 0.11, h: 0.15, color: '#38bdf8', glow: false },
      { id: 'z5', x: 0.44, y: 0.43, w: 0.11, h: 0.15, color: '#facc15', glow: false },
      { id: 'z6', x: 0.64, y: 0.43, w: 0.11, h: 0.15, color: '#38bdf8', glow: false },
      { id: 'z7', x: 0.24, y: 0.64, w: 0.11, h: 0.15, color: '#facc15', glow: false },
      { id: 'z8', x: 0.44, y: 0.64, w: 0.11, h: 0.15, color: '#38bdf8', glow: false },
      { id: 'z9', x: 0.64, y: 0.64, w: 0.11, h: 0.15, color: '#facc15', glow: false }
    ];

    const f1Players = [
      { id: 'b_main', team: 'ball', num: '', x: 0.56, y: 0.29 },
      { id: 'y1', team: 'yellow', num: '6', x: 0.55, y: 0.28 },
      { id: 'y2', team: 'yellow', num: '8', x: 0.68, y: 0.29 },
      { id: 'y3', team: 'yellow', num: '10', x: 0.42, y: 0.52 },
      { id: 'y4', team: 'yellow', num: '7', x: 0.58, y: 0.68 },
      { id: 'y5', team: 'yellow', num: '11', x: 0.30, y: 0.36 },
      { id: 'bl1', team: 'blue', num: '4', x: 0.61, y: 0.33 },
      { id: 'bl2', team: 'blue', num: '5', x: 0.49, y: 0.48 },
      { id: 'bl3', team: 'blue', num: '6', x: 0.37, y: 0.41 },
      { id: 'bl4', team: 'blue', num: '8', x: 0.52, y: 0.63 },
      { id: 'bl5', team: 'blue', num: '9', x: 0.34, y: 0.67 }
    ];

    const f2Players = f1Players.map(p => {
      if (p.id === 'b_main') return { ...p, x: 0.69, y: 0.30 };
      if (p.id === 'y2') return { ...p, x: 0.70, y: 0.30 };
      if (p.id === 'y3') return { ...p, x: 0.49, y: 0.49 };
      if (p.id === 'bl1') return { ...p, x: 0.65, y: 0.35 };
      return { ...p };
    });

    const f3Players = f2Players.map(p => {
      if (p.id === 'b_main') return { ...p, x: 0.49, y: 0.50 };
      if (p.id === 'y3') return { ...p, x: 0.49, y: 0.50 };
      if (p.id === 'y4') return { ...p, x: 0.69, y: 0.51 };
      return { ...p };
    });

    tsState.players = JSON.parse(JSON.stringify(f1Players));
    tsState.keyframes = [
      { players: f1Players, zones: JSON.parse(JSON.stringify(tsState.zones)), arrows: [{ kind: 'pass', x1: 0.56, y1: 0.29, x2: 0.69, y2: 0.30 }] },
      { players: f2Players, zones: tsState.zones.map(z => ({ ...z, glow: z.id === 'z3' })), arrows: [{ kind: 'pass', x1: 0.69, y1: 0.30, x2: 0.49, y2: 0.50 }] },
      { players: f3Players, zones: tsState.zones.map(z => ({ ...z, glow: z.id === 'z6' })), arrows: [] }
    ];
    tsState.currentFrame = 0;
  } else {
    document.getElementById('ts-title').value = 'Build-up Play via Half-Spaces';
    document.getElementById('ts-duration').value = '25 min';
    document.getElementById('ts-players-count').value = '12-16 players';
    document.getElementById('ts-category').value = 'Tactical / Build-up';

    tsState.zones = [
      { id: 'hs_l', x: 0.28, y: 0.22, w: 0.44, h: 0.16, color: '#facc15', glow: true },
      { id: 'hs_r', x: 0.28, y: 0.62, w: 0.44, h: 0.16, color: '#38bdf8', glow: false }
    ];
    const p1 = [
      { id: 'b1', team: 'ball', num: '', x: 0.22, y: 0.38 },
      { id: 'r1', team: 'red', num: '1', x: 0.14, y: 0.50 },
      { id: 'r4', team: 'red', num: '4', x: 0.22, y: 0.38 },
      { id: 'r5', team: 'red', num: '5', x: 0.22, y: 0.62 },
      { id: 'r6', team: 'red', num: '6', x: 0.34, y: 0.50 },
      { id: 'r8', team: 'red', num: '8', x: 0.46, y: 0.30 },
      { id: 'r10', team: 'red', num: '10', x: 0.46, y: 0.70 },
      { id: 'r11', team: 'red', num: '11', x: 0.62, y: 0.16 },
      { id: 'r9', team: 'red', num: '9', x: 0.68, y: 0.50 },
      { id: 'bl9', team: 'blue', num: '9', x: 0.42, y: 0.44 },
      { id: 'bl10', team: 'blue', num: '10', x: 0.42, y: 0.56 },
      { id: 'bl8', team: 'blue', num: '8', x: 0.56, y: 0.36 },
      { id: 'bl6', team: 'blue', num: '6', x: 0.56, y: 0.64 }
    ];
    const p2 = p1.map(p => {
      if (p.id === 'b1') return { ...p, x: 0.52, y: 0.29 };
      if (p.id === 'r8') return { ...p, x: 0.52, y: 0.29 };
      if (p.id === 'r11') return { ...p, x: 0.72, y: 0.16 };
      return { ...p };
    });
    tsState.players = JSON.parse(JSON.stringify(p1));
    tsState.keyframes = [
      { players: p1, zones: JSON.parse(JSON.stringify(tsState.zones)), arrows: [{ kind: 'pass', x1: 0.22, y1: 0.38, x2: 0.52, y2: 0.29 }] },
      { players: p2, zones: JSON.parse(JSON.stringify(tsState.zones)), arrows: [{ kind: 'pass', x1: 0.52, y1: 0.29, x2: 0.72, y2: 0.16 }] }
    ];
    tsState.currentFrame = 0;
  }
  tsResize();
  tsRenderFramesBar();
  tsDraw();
}

function tsAddKeyframe() {
  tsState.keyframes.push({
    players: JSON.parse(JSON.stringify(tsState.players)),
    zones: JSON.parse(JSON.stringify(tsState.zones)),
    arrows: JSON.parse(JSON.stringify(tsState.arrows))
  });
  tsState.currentFrame = tsState.keyframes.length - 1;
  tsRenderFramesBar();
}

function tsSelectFrame(idx) {
  const kf = tsState.keyframes[idx];
  if (!kf) return;
  tsState.currentFrame = idx;
  tsState.players = JSON.parse(JSON.stringify(kf.players));
  tsState.zones = JSON.parse(JSON.stringify(kf.zones));
  tsState.arrows = JSON.parse(JSON.stringify(kf.arrows || []));
  tsRenderFramesBar();
  tsDraw();
}

function tsRenderFramesBar() {
  const bar = document.getElementById('ts-frames-bar');
  if (!bar) return;
  bar.innerHTML = '';
  tsState.keyframes.forEach((_, idx) => {
    const btn = document.createElement('button');
    btn.textContent = 'F' + (idx + 1);
    btn.className = idx === tsState.currentFrame
      ? 'bg-emerald-600 text-white px-2 py-0.5 rounded font-bold'
      : 'bg-slate-800 text-slate-300 px-2 py-0.5 rounded';
    btn.onclick = () => tsSelectFrame(idx);
    bar.appendChild(btn);
  });
}

function tsTogglePlay() {
  const btn = document.getElementById('ts-play-btn');
  if (tsState.playing) {
    tsState.playing = false;
    clearInterval(tsState.playTimer);
    if (btn) btn.textContent = '▶ تشغيل';
    return;
  }
  if (tsState.keyframes.length < 2) return;
  tsState.playing = true;
  if (btn) btn.textContent = '⏸ إيقاف';
  let step = 0;
  const stepsPerFrame = 30;
  tsState.playTimer = setInterval(() => {
    const fromIdx = tsState.currentFrame;
    const toIdx = (fromIdx + 1) % tsState.keyframes.length;
    const fA = tsState.keyframes[fromIdx];
    const fB = tsState.keyframes[toIdx];
    const t = step / stepsPerFrame;

    tsState.players = fA.players.map(pA => {
      const pB = fB.players.find(x => x.id === pA.id) || pA;
      return { ...pA, x: pA.x + (pB.x - pA.x) * t, y: pA.y + (pB.y - pA.y) * t };
    });
    tsState.zones = fB.zones;
    tsState.arrows = fA.arrows || [];
    tsDraw();

    step++;
    if (step > stepsPerFrame) {
      step = 0;
      tsState.currentFrame = toIdx;
      tsRenderFramesBar();
    }
  }, 35);
}

function tsDraw() {
  const cvs = document.getElementById('ts-canvas');
  if (!cvs) return;
  const c = cvs.getContext('2d');
  const w = cvs.width;
  const h = cvs.height;

  const grad = c.createRadialGradient(w * 0.5, h * 0.5, w * 0.08, w * 0.5, h * 0.5, w * 0.72);
  grad.addColorStop(0, '#5ea143');
  grad.addColorStop(1, '#447d30');
  c.fillStyle = grad;
  c.fillRect(0, 0, w, h);

  const bx = w * 0.14, by = h * 0.14, bw = w * 0.72, bh = h * 0.72;
  c.save();
  c.strokeStyle = 'rgba(255,255,255,0.8)';
  c.lineWidth = 2;
  c.setLineDash([7, 7]);
  c.strokeRect(bx, by, bw, bh);
  c.restore();

  [[bx, by], [bx + bw, by], [bx, by + bh], [bx + bw, by + bh]].forEach(([cx, cy]) => {
    tsDrawCone(c, cx, cy, '#ffffff');
  });

  [0.24, 0.27, 0.30, 0.56, 0.59, 0.62].forEach(ry => {
    tsDrawBall(c, bx + bw + 14, h * ry, 5.5);
  });

  tsState.zones.forEach(z => {
    const zx = z.x * w, zy = z.y * h, zw = z.w * w, zh = z.h * h;
    if (z.glow) {
      c.save();
      c.fillStyle = z.color === '#38bdf8' ? 'rgba(56,189,248,0.28)' : 'rgba(250,204,21,0.28)';
      c.shadowColor = z.color;
      c.shadowBlur = 16;
      c.fillRect(zx, zy, zw, zh);
      c.restore();
    }
    c.save();
    c.strokeStyle = z.color;
    c.lineWidth = 1.6;
    c.setLineDash([4, 4]);
    c.strokeRect(zx, zy, zw, zh);
    c.restore();

    [[zx, zy], [zx + zw, zy], [zx, zy + zh], [zx + zw, zy + zh]].forEach(([cx, cy]) => {
      tsDrawCone(c, cx, cy, z.color);
    });
  });

  tsState.arrows.forEach(a => {
    tsDrawArrow(c, a.x1 * w, a.y1 * h, a.x2 * w, a.y2 * h, a.kind);
  });

  tsState.players.forEach(p => {
    const px = p.x * w, py = p.y * h;
    if (p.team === 'ball') {
      tsDrawBall(c, px, py, 7);
    } else {
      const colors = {
        blue: { fill: '#1d4ed8', stroke: '#ffffff', text: '#ffffff' },
        yellow: { fill: '#facc15', stroke: '#1e293b', text: '#0f172a' },
        red: { fill: '#dc2626', stroke: '#ffffff', text: '#ffffff' }
      };
      const stCol = colors[p.team] || colors.blue;
      c.save();
      c.beginPath();
      c.arc(px, py, 13, 0, Math.PI * 2);
      c.fillStyle = stCol.fill;
      c.fill();
      c.lineWidth = 2;
      c.strokeStyle = stCol.stroke;
      c.stroke();
      c.fillStyle = stCol.text;
      c.font = 'bold 11px sans-serif';
      c.textAlign = 'center';
      c.textBaseline = 'middle';
      c.fillText(p.num || '', px, py);
      c.restore();
    }
  });

  const title = document.getElementById('ts-title')?.value || '';
  const dur = document.getElementById('ts-duration')?.value || '';
  const cnt = document.getElementById('ts-players-count')?.value || '';
  const cat = document.getElementById('ts-category')?.value || '';

  c.save();
  c.fillStyle = 'rgba(15, 23, 42, 0.72)';
  c.fillRect(14, 12, w - 28, 34);
  c.fillStyle = '#f8fafc';
  c.font = 'bold 13px sans-serif';
  c.textAlign = 'left';
  c.textBaseline = 'middle';
  c.fillText(title, 24, 29);

  c.fillStyle = '#cbd5e1';
  c.font = '12px sans-serif';
  c.textAlign = 'right';
  c.fillText(`${dur}  •  ${cnt}  •  ${cat}`, w - 24, 29);

  c.fillStyle = 'rgba(255,255,255,0.75)';
  c.font = 'bold 12px sans-serif';
  c.fillText('TootScouting • ProTactics PRO', w - 20, h - 16);
  c.restore();
}

function tsDrawCone(c, x, y, color) {
  c.save();
  c.beginPath();
  c.moveTo(x, y - 6);
  c.lineTo(x - 5, y + 4);
  c.lineTo(x + 5, y + 4);
  c.closePath();
  c.fillStyle = color;
  c.fill();
  c.strokeStyle = '#0f172a';
  c.lineWidth = 1;
  c.stroke();
  c.restore();
}

function tsDrawBall(c, x, y, r) {
  c.save();
  c.beginPath();
  c.arc(x, y, r, 0, Math.PI * 2);
  c.fillStyle = '#ffffff';
  c.fill();
  c.strokeStyle = '#0f172a';
  c.lineWidth = 1.5;
  c.stroke();
  c.restore();
}

function tsDrawArrow(c, x1, y1, x2, y2, kind) {
  c.save();
  c.strokeStyle = '#ffffff';
  c.fillStyle = '#ffffff';
  c.lineWidth = 2.2;
  if (kind === 'pass') c.setLineDash([6, 5]);
  c.beginPath();
  c.moveTo(x1, y1);
  c.lineTo(x2, y2);
  c.stroke();
  c.setLineDash([]);
  const ang = Math.atan2(y2 - y1, x2 - x1);
  c.beginPath();
  c.moveTo(x2, y2);
  c.lineTo(x2 - 9 * Math.cos(ang - 0.4), y2 - 9 * Math.sin(ang - 0.4));
  c.lineTo(x2 - 9 * Math.cos(ang + 0.4), y2 - 9 * Math.sin(ang + 0.4));
  c.closePath();
  c.fill();
  c.restore();
}

function tsExportPNG() {
  const cvs = document.getElementById('ts-canvas');
  if (!cvs) return;
  const link = document.createElement('a');
  link.download = 'TootScouting-Training-Drill.png';
  link.href = cvs.toDataURL('image/png');
  link.click();
}

(function initTrainingEvents() {
  window.addEventListener('load', () => {
    const cvs = document.getElementById('ts-canvas');
    if (!cvs) return;
    cvs.addEventListener('mousedown', e => {
      const r = cvs.getBoundingClientRect();
      const nx = (e.clientX - r.left) / r.width;
      const ny = (e.clientY - r.top) / r.height;

      if (tsState.tool !== 'move') {
        tsState.drawingArrow = { kind: tsState.tool, x1: nx, y1: ny, x2: nx, y2: ny };
        return;
      }

      const hitP = [...tsState.players].reverse().find(p => Math.hypot(p.x - nx, p.y - ny) < 0.035);
      if (hitP) {
        tsState.dragging = { type: 'player', item: hitP };
        return;
      }
      const hitZ = [...tsState.zones].reverse().find(z => nx >= z.x && nx <= z.x + z.w && ny >= z.y && ny <= z.y + z.h);
      if (hitZ) {
        tsState.selectedZoneId = hitZ.id;
        tsState.dragging = { type: 'zone', item: hitZ, ox: nx - hitZ.x, oy: ny - hitZ.y };
        tsDraw();
      }
    });

    cvs.addEventListener('mousemove', e => {
      const r = cvs.getBoundingClientRect();
      const nx = Math.max(0.05, Math.min(0.95, (e.clientX - r.left) / r.width));
      const ny = Math.max(0.08, Math.min(0.92, (e.clientY - r.top) / r.height));

      if (tsState.dragging) {
        if (tsState.dragging.type === 'player') {
          tsState.dragging.item.x = nx;
          tsState.dragging.item.y = ny;
        } else if (tsState.dragging.type === 'zone') {
          tsState.dragging.item.x = nx - tsState.dragging.ox;
          tsState.dragging.item.y = ny - tsState.dragging.oy;
        }
        tsDraw();
      } else if (tsState.drawingArrow) {
        tsState.drawingArrow.x2 = nx;
        tsState.drawingArrow.y2 = ny;
        tsDraw();
        const c = cvs.getContext('2d');
        tsDrawArrow(c, tsState.drawingArrow.x1 * cvs.width, tsState.drawingArrow.y1 * cvs.height, nx * cvs.width, ny * cvs.height, tsState.drawingArrow.kind);
      }
    });

    window.addEventListener('mouseup', () => {
      if (tsState.drawingArrow) {
        if (Math.hypot(tsState.drawingArrow.x2 - tsState.drawingArrow.x1, tsState.drawingArrow.y2 - tsState.drawingArrow.y1) > 0.02) {
          tsState.arrows.push(tsState.drawingArrow);
        }
        tsState.drawingArrow = null;
        tsDraw();
      }
      tsState.dragging = null;
    });
  });
})();
</script>
"""

if "toot-training-studio" not in html_code:
    html_code = html_code + training_studio_module

components.html(html_code, height=1750, scrolling=False)
