import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ProTactics Board | لوحة التحليل التكتيكي",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            max-width: 100%;
        }
        iframe {
            border-radius: 12px;
            border: 1px solid #334155;
        }
    </style>
""", unsafe_allow_html=True)

HTML_CODE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ProTactics Board</title>
<style>
  :root {
    --bg-dark: #0f172a;
    --panel-bg: #1e293b;
    --border-color: #334155;
    --accent: #10b981;
    --danger: #ef4444;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  body {
    background-color: var(--bg-dark);
    color: var(--text-main);
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
  }
  .toolbar {
    background-color: var(--panel-bg);
    border-bottom: 1px solid var(--border-color);
    padding: 8px 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    justify-content: space-between;
    z-index: 10;
  }
  .tool-group {
    display: flex;
    align-items: center;
    gap: 5px;
    background: rgba(15, 23, 42, 0.6);
    padding: 4px 6px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
  }
  button, select {
    background-color: #334155;
    color: var(--text-main);
    border: 1px solid #475569;
    padding: 6px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12.5px;
    font-weight: 600;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  button:hover, select:hover { background-color: #475569; }
  button.active {
    background-color: var(--accent);
    border-color: var(--accent);
    color: #022c22;
  }
  button.eraser-active {
    background-color: var(--danger) !important;
    border-color: var(--danger) !important;
    color: white !important;
  }
  button.danger { background-color: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #fca5a5; }
  button.danger:hover { background-color: #ef4444; color: white; }
  button.export-btn { background-color: #2563eb; border-color: #3b82f6; }
  button.export-btn:hover { background-color: #1d4ed8; }
  input[type="color"] {
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    background: transparent;
  }
  .canvas-wrapper {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    position: relative;
    overflow: hidden;
  }
  canvas {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
    border-radius: 8px;
    max-width: 100%;
    max-height: 100%;
  }
  .hint-bar {
    background: var(--panel-bg);
    border-top: 1px solid var(--border-color);
    padding: 5px 14px;
    font-size: 12px;
    color: var(--text-muted);
    display: flex;
    justify-content: space-between;
  }
  .modal {
    display: none;
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: var(--panel-bg);
    border: 1px solid var(--border-color);
    padding: 20px;
    border-radius: 12px;
    z-index: 100;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8);
    width: 280px;
  }
  .modal h3 { margin-bottom: 12px; font-size: 15px; }
  .modal input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border-radius: 6px;
    border: 1px solid #475569;
    background: #0f172a;
    color: white;
  }
  .modal-actions { display: flex; gap: 8px; justify-content: flex-end; }
</style>
</head>
<body>

<div class="toolbar">
  <div class="tool-group">
    <button id="tool-select" class="active" onclick="setTool('select')">✋ تحريك</button>
    <button id="tool-arrow" onclick="setTool('arrow')">↗️ سهم</button>
    <button id="tool-dashed" onclick="setTool('dashed')">⇢ تمرير</button>
    <button id="tool-curve" onclick="setTool('curve')">↪️ قوس</button>
    <button id="tool-zone" onclick="setTool('zone')">⬡ مساحة</button>
    <button id="tool-measure" onclick="setTool('measure')">📏 قياس (م)</button>
    <button id="tool-eraser" onclick="setTool('eraser')" title="انقر على أي عنصر لحذفه">🗑️ ممحاة</button>
  </div>

  <div class="tool-group">
    <button onclick="addPlayer('red')">🔴 لاعب</button>
    <button onclick="addPlayer('blue')">🔵 خصم</button>
    <button onclick="addCone()">⚠️ قمع</button>
    <button onclick="addBall()">⚽ كرة</button>
    <input type="color" id="drawColor" value="#facc15" title="لون الرسم">
  </div>

  <div class="tool-group">
    <select id="pitchView" onchange="redraw()">
      <option value="full">ملعب كامل</option>
      <option value="half">نصف ملعب</option>
    </select>
    <button id="btn-zones" onclick="toggleZones()">📐 Half-spaces</button>
    <select id="formationSelect" onchange="applyFormation(this.value)">
      <option value="">-- تشكيل جاهز --</option>
      <option value="5-4-1">كتلة دفاعية 5-4-1</option>
      <option value="4-3-3">تشكيل 4-3-3</option>
      <option value="4-2-3-1">تشكيل 4-2-3-1</option>
      <option value="3-2-5">بناء هجومي 3-2-5</option>
    </select>
  </div>

  <div class="tool-group">
    <button onclick="undo()">↩️ تراجع</button>
    <button class="danger" onclick="clearDrawings()">🧹 مسح الرسومات</button>
    <button class="export-btn" onclick="exportImage()">📸 تصدير PNG</button>
  </div>
</div>

<div class="canvas-wrapper" id="canvasWrapper">
  <canvas id="tacticalCanvas"></canvas>
</div>

<div class="hint-bar">
  <span id="statusHint">💡 اسحب اللاعبين، أو انقر مرتين لتعديل الرقم والمركز | استخدم أداة (🗑️ ممحاة) لحذف أي عنصر بالنقر عليه</span>
  <span>ProTactics Studio</span>
</div>

<div class="modal" id="playerModal">
  <h3>تعديل بيانات اللاعب</h3>
  <input type="text" id="playerNumInput" placeholder="الرقم (مثال: 6)">
  <input type="text" id="playerRoleInput" placeholder="المركز (مثال: CB, WB, Pivot)">
  <div class="modal-actions">
    <button class="danger" onclick="deleteEditingPlayer()">حذف اللاعب</button>
    <button onclick="closeModal()">إلغاء</button>
    <button class="active" onclick="savePlayerEdit()">حفظ</button>
  </div>
</div>

<script>
const canvas = document.getElementById('tacticalCanvas');
const ctx = canvas.getContext('2d');
const wrapper = document.getElementById('canvasWrapper');

let currentTool = 'select';
let showHalfSpaces = false;
let pitchRect = { x: 20, y: 20, w: 800, h: 520 };

let items = [];
let drawings = [];
let historyStack = [];

let isDragging = false;
let draggedItem = null;
let selectedItem = null;
let selectedDrawing = null;
let hoveredTarget = null;

let startPos = null;
let currentPos = null;
let zonePoints = [];
let editingPlayer = null;

function initDefaultItems() {
  items = [
    { type: 'ball', x: 0.5, y: 0.5 },
    { type: 'player', team: 'red', x: 0.12, y: 0.5, num: '1', role: 'GK' },
    { type: 'player', team: 'red', x: 0.25, y: 0.12, num: '2', role: 'RWB' },
    { type: 'player', team: 'red', x: 0.22, y: 0.32, num: '4', role: 'RCB' },
    { type: 'player', team: 'red', x: 0.20, y: 0.50, num: '5', role: 'CB' },
    { type: 'player', team: 'red', x: 0.22, y: 0.68, num: '6', role: 'LCB' },
    { type: 'player', team: 'red', x: 0.25, y: 0.88, num: '3', role: 'LWB' },
    { type: 'player', team: 'red', x: 0.36, y: 0.25, num: '7', role: 'RM' },
    { type: 'player', team: 'red', x: 0.34, y: 0.42, num: '8', role: 'Pivot' },
    { type: 'player', team: 'red', x: 0.34, y: 0.58, num: '10', role: 'Pivot' },
    { type: 'player', team: 'red', x: 0.36, y: 0.75, num: '11', role: 'LM' },
    { type: 'player', team: 'red', x: 0.48, y: 0.50, num: '9', role: 'FWD' }
  ];
}

function saveHistory() {
  historyStack.push(JSON.stringify({ items, drawings }));
  if (historyStack.length > 30) historyStack.shift();
}

function undo() {
  if (historyStack.length > 0) {
    const prev = JSON.parse(historyStack.pop());
    items = prev.items;
    drawings = prev.drawings;
    selectedItem = null;
    selectedDrawing = null;
    redraw();
  }
}

function setTool(tool) {
  currentTool = tool;
  zonePoints = [];
  hoveredTarget = null;
  document.querySelectorAll('.toolbar button[id^="tool-"]').forEach(btn => {
    btn.classList.remove('active', 'eraser-active');
  });
  const activeBtn = document.getElementById('tool-' + tool);
  if (activeBtn) {
    if (tool === 'eraser') {
      activeBtn.classList.add('eraser-active');
      canvas.style.cursor = 'not-allowed';
      document.getElementById('statusHint').innerText = '🗑️ وضع الممحاة: انقر مباشرة على أي سهم أو مساحة أو لاعب أو قمع لحذفه فوراً';
    } else {
      activeBtn.classList.add('active');
      canvas.style.cursor = tool === 'select' ? 'grab' : 'crosshair';
      document.getElementById('statusHint').innerText = '💡 اسحب اللاعبين، أو انقر مرتين لتعديل الرقم والمركز | اضغط Delete لحذف العنصر المحدد';
    }
  }
  redraw();
}

function toggleZones() {
  showHalfSpaces = !showHalfSpaces;
  document.getElementById('btn-zones').classList.toggle('active', showHalfSpaces);
  redraw();
}

function resizeCanvas() {
  const rect = wrapper.getBoundingClientRect();
  const w = Math.max(rect.width - 20, 320);
  const h = Math.max(rect.height - 20, 220);
  canvas.width = w;
  canvas.height = h;
  const pad = 24;
  pitchRect = {
    x: pad,
    y: pad,
    w: Math.max(w - pad * 2, 100),
    h: Math.max(h - pad * 2, 100)
  };
  redraw();
}

window.addEventListener('resize', resizeCanvas);

function toPx(nx, ny) {
  return {
    x: pitchRect.x + nx * pitchRect.w,
    y: pitchRect.y + ny * pitchRect.h
  };
}

function toNorm(px, py) {
  return {
    x: Math.max(0.01, Math.min(0.99, (px - pitchRect.x) / pitchRect.w)),
    y: Math.max(0.01, Math.min(0.99, (py - pitchRect.y) / pitchRect.h))
  };
}

function drawPitch() {
  const { x, y, w, h } = pitchRect;
  const view = document.getElementById('pitchView').value;

  ctx.fillStyle = '#14532d';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const stripes = 12;
  const stripeW = w / stripes;
  for (let i = 0; i < stripes; i++) {
    ctx.fillStyle = i % 2 === 0 ? '#166534' : '#15803d';
    ctx.fillRect(x + i * stripeW, y, stripeW, h);
  }

  if (showHalfSpaces) {
    const zoneH = h / 5;
    const labels = ['الرواق الأيمن (Wide)', 'نصف المساحة (Half-Space)', 'العمق (Center)', 'نصف المساحة (Half-Space)', 'الرواق الأيسر (Wide)'];
    for (let i = 0; i < 5; i++) {
      ctx.fillStyle = (i === 1 || i === 3) ? 'rgba(250, 204, 21, 0.14)' : 'rgba(255, 255, 255, 0.04)';
      ctx.fillRect(x, y + i * zoneH, w, zoneH);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
      ctx.setLineDash([6, 6]);
      ctx.beginPath();
      ctx.moveTo(x, y + i * zoneH);
      ctx.lineTo(x + w, y + i * zoneH);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.55)';
      ctx.font = 'bold 11px sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(labels[i], x + w - 10, y + i * zoneH + 16);
    }
  }

  ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';
  ctx.lineWidth = 2;
  ctx.strokeRect(x, y, w, h);

  const centerR = Math.max(Math.min(w, h) * 0.12, 5);

  if (view === 'full') {
    ctx.beginPath();
    ctx.moveTo(x + w / 2, y);
    ctx.lineTo(x + w / 2, y + h);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(x + w / 2, y + h / 2, centerR, 0, Math.PI * 2);
    ctx.stroke();

    const penW = w * 0.16;
    const penH = h * 0.55;
    ctx.strokeRect(x, y + (h - penH) / 2, penW, penH);
    ctx.strokeRect(x, y + (h - penH * 0.45) / 2, penW * 0.36, penH * 0.45);

    ctx.strokeRect(x + w - penW, y + (h - penH) / 2, penW, penH);
    ctx.strokeRect(x + w - penW * 0.36, y + (h - penH * 0.45) / 2, penW * 0.36, penH * 0.45);
  } else {
    const penW = w * 0.32;
    const penH = h * 0.58;
    ctx.strokeRect(x, y + (h - penH) / 2, penW, penH);
    ctx.strokeRect(x, y + (h - penH * 0.45) / 2, penW * 0.36, penH * 0.45);
    ctx.beginPath();
    ctx.arc(x + w, y + h / 2, centerR * 1.3, Math.PI * 0.5, Math.PI * 1.5);
    ctx.stroke();
  }
}

function drawArrowHead(fromX, fromY, toX, toY, color) {
  const headlen = 12;
  const angle = Math.atan2(toY - fromY, toX - fromX);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(toX, toY);
  ctx.lineTo(toX - headlen * Math.cos(angle - Math.PI / 6), toY - headlen * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(toX - headlen * Math.cos(angle + Math.PI / 6), toY - headlen * Math.sin(angle + Math.PI / 6));
  ctx.closePath();
  ctx.fill();
}

function renderSingleDrawing(d, isHighlighted = false) {
  const color = isHighlighted ? '#ef4444' : d.color;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = isHighlighted ? 5 : 3;

  if (d.type === 'arrow' || d.type === 'dashed') {
    const p1 = toPx(d.x1, d.y1);
    const p2 = toPx(d.x2, d.y2);
    if (d.type === 'dashed') ctx.setLineDash([8, 6]);
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
    ctx.setLineDash([]);
    drawArrowHead(p1.x, p1.y, p2.x, p2.y, color);
  } else if (d.type === 'curve') {
    const p1 = toPx(d.x1, d.y1);
    const p2 = toPx(d.x2, d.y2);
    const midX = (p1.x + p2.x) / 2;
    const midY = (p1.y + p2.y) / 2 - 45;
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.quadraticCurveTo(midX, midY, p2.x, p2.y);
    ctx.stroke();
    drawArrowHead(midX, midY, p2.x, p2.y, color);
  } else if (d.type === 'zone' && d.points && d.points.length > 2) {
    ctx.beginPath();
    d.points.forEach((pt, idx) => {
      const px = toPx(pt.x, pt.y);
      if (idx === 0) ctx.moveTo(px.x, px.y);
      else ctx.lineTo(px.x, px.y);
    });
    ctx.closePath();
    ctx.fillStyle = isHighlighted ? 'rgba(239, 68, 68, 0.35)' : hexToRgba(d.color, 0.25);
    ctx.fill();
    ctx.stroke();
  } else if (d.type === 'measure') {
    const p1 = toPx(d.x1, d.y1);
    const p2 = toPx(d.x2, d.y2);
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
    ctx.setLineDash([]);

    const dxMeters = (d.x2 - d.x1) * 105;
    const dyMeters = (d.y2 - d.y1) * 68;
    const dist = Math.hypot(dxMeters, dyMeters).toFixed(1);
    const mx = (p1.x + p2.x) / 2;
    const my = (p1.y + p2.y) / 2;
    ctx.fillStyle = isHighlighted ? '#ef4444' : 'rgba(15, 23, 42, 0.85)';
    ctx.fillRect(mx - 28, my - 12, 56, 22);
    ctx.fillStyle = '#facc15';
    ctx.font = 'bold 12px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(dist + ' m', mx, my + 4);
  }
}

function drawItems() {
  items.forEach((item, index) => {
    const p = toPx(item.x, item.y);
    const isEraseHover = hoveredTarget && hoveredTarget.type === 'item' && hoveredTarget.index === index;
    const isSelected = selectedItem === item;

    if (isEraseHover || isSelected) {
      ctx.strokeStyle = isEraseHover ? '#ef4444' : '#38bdf8';
      ctx.lineWidth = 3;
      ctx.setLineDash([4, 3]);
      ctx.beginPath();
      ctx.arc(p.x, p.y, 22, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    if (item.type === 'player') {
      ctx.beginPath();
      ctx.arc(p.x, p.y, 16, 0, Math.PI *
