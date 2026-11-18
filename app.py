import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ProTactics Studio", page_icon="⚽", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.block-container{padding:0!important;max-width:100%!important;}header[data-testid='stHeader'],footer{display:none;}iframe{border:none!important;width:100%!important;height:100vh!important;display:block;}</style>", unsafe_allow_html=True)

APP_HTML = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700&family=Inter:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
body{font-family:'Cairo','Inter',sans-serif;background:#0b0f19;color:#e2e8f0;overflow:hidden;user-select:none;margin:0}
.font-en{font-family:'Inter',sans-serif}
.tool-btn.active{background:#2563eb;color:#fff;border-color:#60a5fa}
.toggle-pill.active{background:#1e293b;border-color:#38bdf8;color:#38bdf8}
.frame-btn.active{background:#10b981;color:#fff;border-color:#34d399}
canvas{touch-action:none;display:block}
</style>
</head>
<body class="h-screen flex flex-col bg-[#0b0f19]">
<header class="bg-[#111827] border-b border-slate-800 px-2.5 py-1.5 flex flex-wrap items-center justify-between gap-1.5 shrink-0">
  <div class="flex items-center gap-2">
    <span class="text-sm font-bold text-white">⚽ ProTactics <span class="text-[10px] text-amber-300 bg-amber-950 border border-amber-700 px-1.5 py-0.5 rounded-full">Studio</span></span>
  </div>
  <div class="flex flex-wrap items-center gap-1">
    <button onclick="openLineupModal()" class="bg-blue-600 hover:bg-blue-500 text-white text-[11px] px-2.5 py-1 rounded-lg font-bold">الأندية والتشكيلة</button>
    <select onchange="loadSetPiece(this.value);this.value='';" class="bg-slate-900 border border-slate-700 text-amber-300 text-[11px] px-2 py-1 rounded-lg font-semibold">
      <option value="">⚡ قوالب جاهزة</option>
      <option value="corner_att">ركنية هجومية</option>
      <option value="fk_direct">ركلة حرة وحائط صد</option>
      <option value="gk_buildup">بناء لعب من المرمى</option>
      <option value="high_press">ضغط عالي (4-3-3 vs 4-2-3-1)</option>
      <option value="counter_att">تحول هجومي سريع</option>
      <option value="throw_in">رمية تماس هجومية</option>
    </select>
    <div class="flex bg-slate-900 p-0.5 rounded-lg border border-slate-800">
      <button onclick="setPitchMode('full')" id="btn-pitch-full" class="pitch-mode-btn bg-slate-700 text-white text-[11px] px-2 py-0.5 rounded font-semibold">ملعب كامل</button>
      <button onclick="setPitchMode('half')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 text-[11px] px-2 py-0.5 rounded font-semibold">نصف ملعب</button>
    </div>
    <button onclick="toggleZones()" id="btn-toggle-zones" class="toggle-pill bg-slate-900 text-slate-300 border border-slate-700 text-[11px] px-2 py-1 rounded-lg font-semibold">5-Zones</button>
    <button onclick="toggleOffside()" id="btn-toggle-offside" class="toggle-pill bg-slate-900 text-slate-300 border border-slate-700 text-[11px] px-2 py-1 rounded-lg font-semibold">التسلل</button>
    <button onclick="toggleCompactness()" id="btn-toggle-compact" class="toggle-pill bg-slate-900 text-slate-300 border border-slate-700 text-[11px] px-2 py-1 rounded-lg font-semibold">التماسك</button>
    <button onclick="toggleNotesPanel()" id="btn-toggle-notes" class="toggle-pill bg-slate-900 text-slate-300 border border-slate-700 text-[11px] px-2 py-1 rounded-lg font-semibold">الملاحظات</button>
    <select id="pitch-theme-select" onchange="setPitchTheme(this.value)" class="bg-slate-900 border border-slate-700 text-slate-200 text-[11px] px-1.5 py-1 rounded-lg">
      <option value="green">أخضر عشبي</option><option value="classic">أخضر فاتح</option><option value="navy">كحلي تكتيكي</option><option value="midnight">أسود ليلي</option><option value="opta">أبيض Opta</option>
    </select>
  </div>
  <div class="flex items-center gap-1">
    <button onclick="exportJSON()" title="حفظ" class="bg-slate-800 text-sky-300 border border-slate-700 text-[11px] px-2 py-1 rounded-lg"><i class="fa-solid fa-floppy-disk"></i></button>
    <label title="فتح" class="bg-slate-800 text-purple-300 border border-slate-700 text-[11px] px-2 py-1 rounded-lg cursor-pointer"><i class="fa-solid fa-folder-open"></i><input type="file" accept=".json" onchange="importJSON(event)" class="hidden"></label>
    <button onclick="undoAction()" title="تراجع" class="bg-slate-800 text-slate-200 border border-slate-700 text-[11px] px-2 py-1 rounded-lg"><i class="fa-solid fa-rotate-left"></i></button>
    <button onclick="clearDrawings()" title="مسح الرسم" class="bg-slate-800 text-amber-300 border border-slate-700 text-[11px] px-2 py-1 rounded-lg"><i class="fa-solid fa-eraser"></i></button>
    <button onclick="resetBoard()" title="إعادة ضبط" class="bg-slate-800 text-red-400 border border-slate-700 text-[11px] px-2 py-1 rounded-lg"><i class="fa-solid fa-trash-can"></i></button>
    <button onclick="exportPNG()" class="bg-emerald-600 text-white font-bold text-[11px] px-2 py-1 rounded-lg">PNG</button>
    <button onclick="exportVideo()" id="btn-export-video" class="bg-rose-600 text-white font-bold text-[11px] px-2 py-1 rounded-lg">فيديو</button>
  </div>
</header>

<div class="flex-1 flex overflow-hidden">
  <aside class="bg-[#111827] border-l border-slate-800 p-2 flex flex-col gap-1.5 w-48 shrink-0 overflow-y-auto">
    <div class="grid grid-cols-2 gap-1">
      <button onclick="setTool('select')" id="tool-select" class="tool-btn active p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px]">تحريك</button>
      <button onclick="setTool('spotlight')" id="tool-spotlight" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px] text-amber-300">تمييز لاعب</button>
      <button onclick="setTool('arrow')" id="tool-arrow" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px]">سهم حركة</button>
      <button onclick="setTool('curved')" id="tool-curved" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px]">ضغط قوسي</button>
      <button onclick="setTool('pass')" id="tool-pass" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px]">تمرير</button>
      <button onclick="setTool('shadow')" id="tool-shadow" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px] text-rose-300">ظل دفاعي</button>
      <button onclick="setTool('vision')" id="tool-vision" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px] text-cyan-300">مخروط رؤية</button>
      <button onclick="setTool('polygon')" id="tool-polygon" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px]">تظليل مساحة</button>
      <button onclick="setTool('ruler')" id="tool-ruler" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px]">قياس متر</button>
      <button onclick="setTool('text')" id="tool-text" class="tool-btn p-1.5 rounded border border-slate-700 bg-slate-800 text-[11px]">نص شرح</button>
    </div>
    <div class="flex items-center justify-around bg-slate-900 p-1.5 rounded border border-slate-800">
      <button onclick="setColor('#facc15')" data-color="#facc15" class="color-btn w-4 h-4 rounded-full bg-yellow-400 ring-2 ring-white"></button>
      <button onclick="setColor('#ffffff')" data-color="#ffffff" class="color-btn w-4 h-4 rounded-full bg-white"></button>
      <button onclick="setColor('#ef4444')" data-color="#ef4444" class="color-btn w-4 h-4 rounded-full bg-red-500"></button>
      <button onclick="setColor('#38bdf8')" data-color="#38bdf8" class="color-btn w-4 h-4 rounded-full bg-sky-400"></button>
      <button onclick="setColor('#f97316')" data-color="#f97316" class="color-btn w-4 h-4 rounded-full bg-orange-500"></button>
    </div>
    <div class="grid grid-cols-2 gap-1">
      <button onclick="addPiece('red')" class="bg-red-950 text-red-300 border border-red-800 py-1 rounded text-[11px]">+ لاعب 1</button>
      <button onclick="addPiece('blue')" class="bg-sky-950 text-sky-300 border border-sky-800 py-1 rounded text-[11px]">+ لاعب 2</button>
      <button onclick="addPiece('ball')" class="bg-slate-800 text-slate-200 border border-slate-700 py-1 rounded text-[11px]">+ كرة</button>
      <button onclick="addPiece('cone')" class="bg-amber-950 text-amber-300 border border-amber-800 py-1 rounded text-[11px]">+ قمع</button>
      <button onclick="addPiece('mannequin')" class="bg-purple-950 text-purple-300 border border-purple-800 py-1 rounded text-[11px]">+ دمية</button>
      <button onclick="addPiece('minigoal')" class="bg-emerald-950 text-emerald-300 border border-emerald-800 py-1 rounded text-[11px]">+ مرمى صغير</button>
    </div>
  </aside>

  <main id="canvas-container" class="flex-1 relative bg-[#080c14] flex flex-col items-center justify-between p-2 overflow-hidden">
    <div class="w-full max-w-5xl flex items-center justify-between bg-slate-900 border border-slate-800 rounded-lg px-3 py-1 shrink-0">
      <div class="flex items-center gap-2">
        <img id="banner-red-logo" src="" class="hidden w-5 h-5 object-contain rounded">
        <span id="badge-red-color" class="w-2.5 h-2.5 rounded-full bg-red-600 inline-block"></span>
        <span id="display-red-name" class="text-xs font-bold text-white">الفريق الأول</span>
        <span id="display-red-form" class="text-[10px] font-en bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded">5-4-1</span>
        <span id="metrics-red" class="hidden text-[10px] font-en bg-red-950 border border-red-800 text-red-200 px-2 py-0.5 rounded"></span>
      </div>
      <span class="text-[11px] font-en font-bold text-slate-500">VS</span>
      <div class="flex items-center gap-2">
        <span id="metrics-blue" class="hidden text-[10px] font-en bg-sky-950 border border-sky-800 text-sky-200 px-2 py-0.5 rounded"></span>
        <span id="display-blue-form" class="text-[10px] font-en bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded">4-3-3</span>
        <span id="display-blue-name" class="text-xs font-bold text-white">الفريق الثاني</span>
        <span id="badge-blue-color" class="w-2.5 h-2.5 rounded-full bg-sky-600 inline-block"></span>
        <img id="banner-blue-logo" src="" class="hidden w-5 h-5 object-contain rounded">
      </div>
    </div>

    <div id="pitch-wrapper" class="flex-1 w-full flex items-center justify-center overflow-hidden my-1">
      <canvas id="tactical-canvas" class="rounded-xl shadow-2xl border border-slate-800"></canvas>
    </div>

    <div class="w-full max-w-5xl bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5 flex items-center justify-between gap-2 shrink-0">
      <div class="flex items-center gap-1.5">
        <button onclick="togglePlayAnimation()" id="btn-play-anim" class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-lg"><span id="play-label">▶ تشغيل</span></button>
        <button onclick="addKeyframe()" class="bg-blue-600 text-white text-xs font-semibold px-2.5 py-1 rounded-lg">+ إطار</button>
        <button onclick="deleteCurrentKeyframe()" class="bg-slate-800 text-red-400 text-xs px-2 py-1 rounded-lg">حذف</button>
      </div>
      <div id="frames-list" class="flex items-center gap-1 overflow-x-auto"></div>
      <select id="anim-speed" class="bg-slate-950 border border-slate-700 rounded px-1.5 py-0.5 text-xs text-white"><option value="1400">بطيء</option><option value="900" selected>متوسط</option><option value="500">سريع</option></
