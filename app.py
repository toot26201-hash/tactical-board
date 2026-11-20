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

# إزالة أي تكرار لزر "تدريب"
training_btn_html = '<button onclick="activateTrainingPitch()" id="btn-pitch-training" class="pitch-mode-btn text-emerald-300 px-2 py-0.5 rounded">تدريب</button>'
html_code = re.sub(
    r'(<button onclick="activateTrainingPitch\(\)" id="btn-pitch-training"[^>]*>تدريب</button>)+',
    training_btn_html,
    html_code
)

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

# 4. إصلاح بلوك dblclick التالف أياً كان شكله في index.html
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
  render();
  if (typeof __renderGuaranteedPitch === "function") __renderGuaranteedPitch();
}
function quickKitUpdate('''
    html_code = html_code.replace('function quickKitUpdate(', team_color_fn)

# 7. تحديث دالة saveEditModal بأمان
old_save_edit = 'function saveEditModal(){const p=pieces.find(x=>x.id===editingPieceId);if(p){saveHistory();p.number=document.getElementById("edit-number").value;p.label=document.getElementById("edit-label").value;p.customColor=document.getElementById("edit-use-custom-color").checked?document.getElementById("edit-custom-color").value:null;p.spotlight=document.getElementById("edit-spotlight").checked;syncCurrentFrame();render();}closeEditModal();}'
new_save_edit = 'function saveEditModal(){const p=pieces.find(x=>x.id===editingPieceId);if(p){saveHistory();p.number=document.getElementById("edit-number").value;p.label=document.getElementById("edit-label").value;p.customColor=document.getElementById("edit-use-custom-color").checked?document.getElementById("edit-custom-color").value:null;p.spotlight=document.getElementById("edit-spotlight").checked;const __nc=document.getElementById("edit-num-color");const __lc=document.getElementById("edit-label-color");if(__nc)p.numColor=__nc.value;if(__lc)p.labelColor=__lc.value;syncCurrentFrame();render();if(typeof __renderGuaranteedPitch==="function")__renderGuaranteedPitch();}closeEditModal();}'
html_code = html_code.replace(old_save_edit, new_save_edit)

# 8. إضافة وضع "تدريب"
if 'id="btn-pitch-training"' not in html_code:
    html_code = html_code.replace(
        '<button onclick="setPitchMode(\'half\')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 px-2 py-0.5 rounded">نصف</button>',
        '<button onclick="setPitchMode(\'half\')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 px-2 py-0.5 rounded">نصف</button>' + training_btn_html
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
  if (typeof resizeCanvas === "function") resizeCanvas();
  if (typeof render === "function") render();
  if (typeof __renderGuaranteedPitch === "function") __renderGuaranteedPitch();
  showToast("تم تجهيز ملعب التدريب — أضف الأقماع واللاعبين حسب الدريل");
}
function setPitchMode('''
    html_code = html_code.replace('function setPitchMode(', training_fn)

# 9. طبقة رسم مضمونة للملعب واللاعبين والكورة داخل مساحة السبورة
guaranteed_layer = """
<script>
window.openAuthModal = window.openAuthModal || function(mode = 'login') {
  const modal = document.getElementById('auth-modal') || document.querySelector('[id*="auth"][class*="fixed"], [id*="login-modal"]');
  if (modal) {
    modal.classList.remove('hidden');
    modal.style.display = 'flex';
  }
};
window.openAuthFromLanding = window.openAuthFromLanding || function(mode = 'login') {
  window.openAuthModal(mode);
};

function __findBoardHost() {
  const canvases = Array.from(document.querySelectorAll("canvas"));
  let bestCvs = null;
  let bestArea = 0;
  canvases.forEach(c => {
    const r = c.getBoundingClientRect();
    const area = Math.max(0, r.width) * Math.max(0, r.height);
    if (area > bestArea) {
      bestArea = area;
      bestCvs = c;
    }
  });
  if (bestCvs && bestCvs.parentElement) {
    return { host: bestCvs.parentElement, rect: bestCvs.parentElement.getBoundingClientRect() };
  }
  const mainEl = document.querySelector("main") || document.body;
  return { host: mainEl, rect: mainEl.getBoundingClientRect() };
}

function __renderGuaranteedPitch() {
  try {
    const { host, rect } = __findBoardHost();
    if (!host) return;
    let overlay = document.getElementById("toot-guaranteed-pitch");
    if (!overlay) {
      overlay = document.createElement("canvas");
      overlay.id = "toot-guaranteed-pitch";
      overlay.style.position = "absolute";
      overlay.style.inset = "0";
      overlay.style.width = "100%";
      overlay.style.height = "100%";
      overlay.style.pointerEvents = "none";
      overlay.style.zIndex = "5";
      overlay.style.borderRadius = "12px";
      const computedPos = getComputedStyle(host).position;
      if (computedPos === "static") host.style.position = "relative";
      host.appendChild(overlay);
    }

    const w = Math.max(500, Math.floor(rect.width || host.clientWidth || 860));
    const h = Math.max(320, Math.floor(rect.height || host.clientHeight || 480));
    if (overlay.width !== w || overlay.height !== h) {
      overlay.width = w;
      overlay.height = h;
    }

    const c = overlay.getContext("2d");
    if (!c) return;
    c.clearRect(0, 0, w, h);

    // عشب الملعب بخطوط طولية خفيفة
    const stripeCount = 12;
    const stripeW = w / stripeCount;
    for (let i = 0; i < stripeCount; i++) {
      c.fillStyle = i % 2 === 0 ? "#15803d" : "#166534";
      c.fillRect(i * stripeW, 0, stripeW + 1, h);
    }

    const padX = Math.round(w * 0.05);
    const padY = Math.round(h * 0.06);
    const pw = w - padX * 2;
    const ph = h - padY * 2;

    c.strokeStyle = "rgba(255,255,255,0.9)";
    c.lineWidth = 2.5;
    c.strokeRect(padX, padY, pw, ph);

    // خط المنتصف ودائرة المنتصف
    c.beginPath();
    c.moveTo(w / 2, padY);
    c.lineTo(w / 2, padY + ph);
    c.stroke();

    c.beginPath();
    c.arc(w / 2, padY + ph / 2, Math.min(pw, ph) * 0.13, 0, Math.PI * 2);
    c.stroke();

    c.beginPath();
    c.arc(w / 2, padY + ph / 2, 4, 0, Math.PI * 2);
    c.fillStyle = "#ffffff";
    c.fill();

    // منطقتا الجزاء ومنطقتا المرمى
    const penW = pw * 0.16;
    const penH = ph * 0.62;
    c.strokeRect(padX, padY + (ph - penH) / 2, penW, penH);
    c.strokeRect(padX + pw - penW, padY + (ph - penH) / 2, penW, penH);

    const gW = pw * 0.06;
    const gH = ph * 0.3;
    c.strokeRect(padX, padY + (ph - gH) / 2, gW, gH);
    c.strokeRect(padX + pw - gW, padY + (ph - gH) / 2, gW, gH);

    // رسم اللاعبين والكورة إن وجدوا
    if (typeof pieces !== "undefined" && Array.isArray(pieces) && pieces.length > 0) {
      pieces.forEach(p => {
        const px = padX + ((typeof p.nx === "number" ? p.nx : 0.5) * pw);
        const py = padY + ((typeof p.ny === "number" ? p.ny : 0.5) * ph);
        if (p.type === "ball") {
          c.fillStyle = "#ffffff";
          c.beginPath();
          c.arc(px, py, 7, 0, Math.PI * 2);
          c.fill();
          c.strokeStyle = "#0f172a";
          c.lineWidth = 1.5;
          c.stroke();
        } else {
          const fillCol = p.customColor || (p.type === "red" ? "#ef4444" : "#3b82f6");
          c.fillStyle = fillCol;
          c.beginPath();
          c.arc(px, py, 14, 0, Math.PI * 2);
          c.fill();
          c.strokeStyle = "#ffffff";
          c.lineWidth = 2;
          c.stroke();

          if (p.number) {
            c.fillStyle = p.numColor || "#ffffff";
            c.font = "bold 11px sans-serif";
            c.textAlign = "center";
            c.textBaseline = "middle";
            c.fillText(String(p.number), px, py);
          }
          if (p.label) {
            c.fillStyle = p.labelColor || "#f8fafc";
            c.font = "bold 10px sans-serif";
            c.textAlign = "center";
            c.textBaseline = "top";
            c.fillText(String(p.label), px, py + 17);
          }
        }
      });
    }
  } catch (e) {}
}

window.addEventListener("load", () => {
  setTimeout(__renderGuaranteedPitch, 200);
  setTimeout(__renderGuaranteedPitch, 700);
  setTimeout(__renderGuaranteedPitch, 1500);
});
window.addEventListener("resize", () => setTimeout(__renderGuaranteedPitch, 120));
setTimeout(__renderGuaranteedPitch, 350);
</script>
"""
if "__renderGuaranteedPitch" not in html_code:
    html_code = html_code + guaranteed_layer

components.html(html_code, height=1750, scrolling=False)
