import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ProTactics - لوحة التحليل والرسم التكتيكي",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        .block-container { padding: 0.3rem 0.5rem 0 0.5rem !important; max-width: 100% !important; }
        header[data-testid="stHeader"], footer { display: none; }
        iframe { border-radius: 12px; border: 1px solid #1e293b; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

if "<script>" in html_code:
    html_code = html_code.split("<script>")[0] + "</body></html>"

js_engine = """
<script>
const canvas = document.getElementById('tactical-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');

let pitchMode = 'full', showZones = false, pitchTheme = 'green', currentTool = 'select';
let currentColor = '#facc15', currentStrokeWidth = 3;
let pitchRect = { x: 20, y: 20, w: 884, h: 558, canvasW: 924, canvasH: 598 };
let redTeamMeta = { name: 'الفريق الأحمر', formation: '5-4-1' };
let blueTeamMeta = { name: 'الفريق الأزرق', formation: '4-3-3' };
let pieces = [], drawings = [], historyStack = [];
let draggingPiece = null, dragOffset = { x: 0, y: 0 }, isDrawing = false, currentDraft = null;
let polygonPoints = [], editingPieceId = null, pendingTextPos = null;

const formationTemplates = {
    '5-4-1': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.12,num:'WB',label:'LWB'},{nx:0.20,ny:0.31,num:'CB',label:'LCB'},{nx:0.19,ny:0.5,num:'CB',label:'CB'},{nx:0.20,ny:0.69,num:'CB',label:'RCB'},{nx:0.22,ny:0.88,num:'WB',label:'RWB'},{nx:0.34,ny:0.20,num:'WM',label:'LM'},{nx:0.33,ny:0.41,num:'DM',label:'Pivot'},{nx:0.33,ny:0.59,num:'DM',label:'Pivot'},{nx:0.34,ny:0.80,num:'WM',label:'RM'},{nx:0.47,ny:0.5,num:'9',label:'FWD'}],
    '4-3-3': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.15,num:'3',label:'LB'},{nx:0.20,ny:0.38,num:'4',label:'CB'},{nx:0.20,ny:0.62,num:'5',label:'CB'},{nx:0.22,ny:0.85,num:'2',label:'RB'},{nx:0.33,ny:0.5,num:'6',label:'DM'},{nx:0.39,ny:0.30,num:'8',label:'CM'},{nx:0.39,ny:0.70,num:'10',label:'CM'},{nx:0.46,ny:0.16,num:'11',label:'LW'},{nx:0.48,ny:0.5,num:'9',label:'ST'},{nx:0.46,ny:0.84,num:'7',label:'RW'}],
    '3-5-2': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.20,ny:0.28,num:'CB',label:'LCB'},{nx:0.19,ny:0.5,num:'CB',label:'CB'},{nx:0.20,ny:0.72,num:'CB',label:'RCB'},{nx:0.34,ny:0.10,num:'WB',label:'LWB'},{nx:0.31,ny:0.5,num:'6',label:'DM'},{nx:0.36,ny:0.34,num:'8',label:'CM'},{nx:0.36,ny:0.66,num:'10',label:'CM'},{nx:0.34,ny:0.90,num:'WB',label:'RWB'},{nx:0.47,ny:0.38,num:'9',label:'ST'},{nx:0.47,ny:0.62,num:'11',label:'ST'}],
    '4-2-3-1': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.15,num:'3',label:'LB'},{nx:0.20,ny:0.38,num:'4',label:'CB'},{nx:0.20,ny:0.62,num:'5',label:'CB'},{nx:0.22,ny:0.85,num:'2',label:'RB'},{nx:0.32,ny:0.38,num:'6',label:'Pivot'},{nx:0.32,ny:0.62,num:'8',label:'Pivot'},{nx:0.41,ny:0.18,num:'11',label:'LW'},{nx:0.42,ny:0.5,num:'10',label:'CAM'},{nx:0.41,ny:0.82,num:'7',label:'RW'},{nx:0.48,ny:0.5,num:'9',label:'ST'}],
    '4-4-2': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.15,num:'3',label:'LB'},{nx:0.20,ny:0.38,num:'4',label:'CB'},{nx:0.20,ny:0.62,num:'5',label:'CB'},{nx:0.22,ny:0.85,num:'2',label:'RB'},{nx:0.35,ny:0.16,num:'11',label:'LM'},{nx:0.34,ny:0.40,num:'6',label:'CM'},{nx:0.34,ny:0.60,num:'8',label:'CM'},{nx:0.35,ny:0.84,num:'7',label:'RM'},{nx:0.47,ny:0.38,num:'9',label:'ST'},{nx:0.47,ny:0.62,num:'10',label:'ST'}]
};

function initDefaultPieces() {
    pieces = [];
    formationTemplates['5-4-1'].forEach((p, i) => pieces.push({ id: 'r' + i, type: 'red', nx: p.nx, ny: p.ny, number: p.num, label: p.label }));
    formationTemplates['4-3-3'].forEach((p, i) => pieces.push({ id: 'b' + i, type: 'blue', nx: 1 - p.nx, ny: p.ny, number: p.num, label: p.label }));
    pieces.push({ id: 'ball1', type: 'ball', nx: 0.5, ny: 0.5, number: '', label: '' });
}

function resizeCanvas() {
    const rect = container.getBoundingClientRect();
    const availW = Math.max(450, (rect.width || 980) - 36);
    const availH = Math.max(400, (rect.height || 660) - 56);
    const ratio = pitchMode === 'full' ? (105 / 68) : (68 / 52.5);
    let finalH = availH, finalW = finalH * ratio;
    if (finalW > availW) { finalW = availW; finalH = finalW / ratio; }
    canvas.width = Math.round(finalW); canvas.height = Math.round(finalH);
    canvas.style.width = Math.round(finalW) + 'px'; canvas.style.height = Math.round(finalH) + 'px';
    const m = 18;
    pitchRect = { x: m, y: m, w: finalW - m * 2, h: finalH - m * 2, canvasW: finalW, canvasH: finalH };
    render();
}

const normToCanvas = (nx, ny) => ({ x: pitchRect.x + nx * pitchRect.w, y: pitchRect.y + ny * pitchRect.h });
const canvasToNorm = (cx, cy) => ({ nx: Math.max(0, Math.min(1, (cx - pitchRect.x) / pitchRect.w)), ny: Math.max(0, Math.min(1, (cy - pitchRect.y) / pitchRect.h)) });
const calculateMeters = (p1, p2) => Math.hypot((p2.nx - p1.nx) * (pitchMode === 'full' ? 105 : 52.5), (p2.ny - p1.ny) * 68).toFixed(1);

function drawPitch() {
    const { x, y, w, h, canvasW, canvasH } = pitchRect;
    ctx.fillStyle = pitchTheme === 'green' ? '#0d2618' : '#0f172a';
    ctx.fillRect(0, 0, canvasW, canvasH);
    ctx.fillStyle = pitchTheme === 'green' ? '#133824' : '#151e32';
    ctx.fillRect(x, y, w, h);
    if (pitchTheme === 'green') {
        const s = pitchMode === 'full' ? 14 : 8, sw = w / s;
        for (let i = 0; i < s; i += 2) { ctx.fillStyle = 'rgba(255,255,255,0.03)'; ctx.fillRect(x + i * sw, y, sw, h); }
    }
    if (showZones) {
        const penH = (40.32 / 68) * h, goalH = (18.32 / 68) * h, topW = (h - penH) / 2, hsH = (penH - goalH) / 2;
        const y1 = y + topW, y2 = y1 + hsH, y3 = y2 + goalH, y4 = y3 + hsH;
        ctx.fillStyle = 'rgba(250,204,21,0.09)'; ctx.fillRect(x, y1, w, hsH); ctx.fillRect(x, y3, w, hsH);
        ctx.save(); ctx.strokeStyle = 'rgba(250,204,21,0.45)'; ctx.setLineDash([6, 6]); ctx.lineWidth = 1.2;
        [y1, y2, y3, y4].forEach(ly => { ctx.beginPath(); ctx.moveTo(x, ly); ctx.lineTo(x + w, ly); ctx.stroke(); });
        ctx.strokeStyle = 'rgba(56,189,248,0.35)';
        [x + w / 3, x + (2 * w) / 3].forEach(lx => { ctx.beginPath(); ctx.moveTo(lx, y); ctx.lineTo(lx, y + h); ctx.stroke(); });
        ctx.restore();
    }
    ctx.strokeStyle = pitchTheme === 'green' ? 'rgba(255,255,255,0.72)' : 'rgba(148,163,184,0.6)';
    ctx.lineWidth = 2; ctx.strokeRect(x, y, w, h);
    const len = pitchMode === 'full' ? 105 : 52.5, cR = (9.15 / len) * w;
    const penW = (16.5 / len) * w, penH = (40.32 / 68) * h, penY = y + (h - penH) / 2;
    const goalW = (5.5 / len) * w, goalH = (18.32 / 68) * h, goalY = y + (h - goalH) / 2;
    const spot = (11 / len) * w, netH = (7.32 / 68) * h;
    ctx.strokeRect(x, penY, penW, penH); ctx.strokeRect(x, goalY, goalW, goalH);
    ctx.fillStyle = ctx.strokeStyle; ctx.beginPath(); ctx.arc(x + spot, y + h / 2, 2.5, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(x + spot, y + h / 2, cR, -0.92, 0.92); ctx.stroke();
    ctx.strokeRect(x - 6, y + (h - netH) / 2, 6, netH);
    if (pitchMode === 'full') {
        ctx.beginPath(); ctx.moveTo(x + w / 2, y); ctx.lineTo(x + w / 2, y + h); ctx.stroke();
        ctx.beginPath(); ctx.arc(x + w / 2, y + h / 2, cR, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.arc(x + w / 2, y + h / 2, 3, 0, Math.PI * 2); ctx.fill();
        ctx.strokeRect(x + w - penW, penY, penW, penH); ctx.strokeRect(x + w - goalW, goalY, goalW, goalH);
        ctx.beginPath(); ctx.arc(x + w - spot, y + h / 2, 2.5, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(x + w - spot, y + h / 2, cR, Math.PI - 0.92, Math.PI + 0.92); ctx.stroke();
        ctx.strokeRect(x + w, y + (h - netH) / 2, 6, netH);
    } else {
        ctx.beginPath(); ctx.arc(x + w, y + h / 2, cR, Math.PI * 0.5, Math.PI * 1.5); ctx.stroke();
    }
}

function renderItem(item) {
    ctx.save(); ctx.strokeStyle = item.color; ctx.fillStyle = item.color; ctx.lineWidth = item.width || 3; ctx.lineCap = 'round';
    const p1 = normToCanvas(item.points[0].nx, item.points[0].ny);
    const p2 = item.points[1] ? normToCanvas(item.points[1].nx, item.points[1].ny) : p1;
    if (item.type === 'arrow' || item.type === 'pass') {
        const hl = 11 + (item.width || 3) * 1.5, ang = Math.atan2(p2.y - p1.y, p2.x - p1.
