const canvas = document.getElementById('tactical-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');

let pitchMode = 'full', showZones = false, pitchTheme = 'green', currentTool = 'select';
let currentColor = '#facc15', currentStrokeWidth = 3;
let pitchRect = { x: 0, y: 0, w: 0, h: 0 };
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

const toolHints = {
    select: 'اسحب اللاعبين لتحريكهم. انقر مرتين لتعديل الرقم أو الاسم.',
    arrow: 'اضغط واسحب لرسم سهم حركة مستقيم.',
    curved: 'اضغط واسحب لرسم سهم ضغط قوسي.',
    pass: 'اضغط واسحب لرسم خط تمرير متقطع.',
    polygon: 'انقر لتحديد نقاط المنطقة ثم اضغط إغلاق وتظليل.',
    ruler: 'اضغط واسحب لقياس المسافة بالمتر (105×68م).',
    connect: 'اضغط واسحب لربط اللاعبين بخط.',
    text: 'انقر في أي مكان لإضافة نص.'
};

function initDefaultPieces() {
    pieces = [];
    formationTemplates['5-4-1'].forEach((p, i) => pieces.push({ id: 'r' + i, type: 'red', nx: p.nx, ny: p.ny, number: p.num, label: p.label }));
    formationTemplates['4-3-3'].forEach((p, i) => pieces.push({ id: 'b' + i, type: 'blue', nx: 1 - p.nx, ny: p.ny, number: p.num, label: p.label }));
    pieces.push({ id: 'ball1', type: 'ball', nx: 0.5, ny: 0.5, number: '', label: '' });
    document.getElementById('display-red-name').textContent = redTeamMeta.name;
    document.getElementById('display-red-form').textContent = redTeamMeta.formation;
    document.getElementById('display-blue-name').textContent = blueTeamMeta.name;
    document.getElementById('display-blue-form').textContent = blueTeamMeta.formation;
}

function resizeCanvas() {
    const rect = container.getBoundingClientRect();
    const availW = Math.max(320, rect.width - 40);
    const availH = Math.max(260, rect.height - 60);
    const ratio = pitchMode === 'full' ? (105 / 68) : (68 / 52.5);
    let finalH = availH, finalW = finalH * ratio;
    if (finalW > availW) { finalW = availW; finalH = finalW / ratio; }
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(finalW * dpr); canvas.height = Math.round(finalH * dpr);
    canvas.style.width = Math.round(finalW) + 'px'; canvas.style.height = Math.round(finalH) + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const m = Math.max(12, Math.min(finalW, finalH) * 0.025);
    pitchRect = { x: m, y: m, w: finalW - m * 2, h: finalH - m * 2, canvasW: finalW, canvasH: finalH };
    render();
}

const normToCanvas = (nx, ny) => ({ x: pitchRect.x + nx * pitchRect.w, y: pitchRect.y + ny * pitchRect.h });
const canvasToNorm = (cx, cy) => ({ nx: Math.max(0, Math.min(1, (cx - pitchRect.x) / pitchRect.w)), ny: Math.max(0, Math.min(1, (cy - pitchRect.y) / pitchRect.h)) });
const calculateMeters = (p1, p2) => Math.hypot((p2.nx - p1.nx) * (pitchMode === 'full' ? 105 : 52.5), (p2.ny - p1.ny) * 68).toFixed(1);

function drawPitch() {
    const { x, y, w, h, canvasW, canvasH } = pitchRect;
    if (w <= 0 || h <= 0) return;
    ctx.fillStyle = pitchTheme === 'green' ? '#0d2618' : '#0f172a';
    ctx.fillRect(0, 0, canvasW, canvasH);
    ctx.fillStyle = pitchTheme === 'green' ? '#133824' : '#151e32';
    ctx.fillRect(x, y, w, h);
    if (pitchTheme === 'green') {
        const s = pitchMode === 'full' ? 14 : 8, sw = w / s;
        for (let i = 0; i < s; i += 2) { ctx.fillStyle = 'rgba(255,255,255,0.025)'; ctx.fillRect(x + i * sw, y, sw, h); }
    }
    if (showZones) {
        const penH = (40.32 / 68) * h, goalH = (18.32 / 68) * h, topW = (h - penH) / 2, hsH = (penH - goalH) / 2;
        const y1 = y + topW, y2 = y1 + hsH, y3 = y2 + goalH, y4 = y3 + hsH;
        ctx.fillStyle = 'rgba(250,204,21,0.08)'; ctx.fillRect(x, y1, w, hsH); ctx.fillRect(x, y3, w, hsH);
        ctx.save(); ctx.strokeStyle = 'rgba(250,204,21,0.42)'; ctx.setLineDash([6, 6]); ctx.lineWidth = 1.2;
        [y1, y2, y3, y4].forEach(ly => { ctx.beginPath(); ctx.moveTo(x, ly); ctx.lineTo(x + w, ly); ctx.stroke(); });
        ctx.strokeStyle = 'rgba(56,189,248,0.35)';
        [x + w / 3, x + (2 * w) / 3].forEach(lx => { ctx.beginPath(); ctx.moveTo(lx, y); ctx.lineTo(lx, y + h); ctx.stroke(); });
        ctx.restore();
    }
    ctx.strokeStyle = pitchTheme === 'green' ? 'rgba(255,255,255,0.65)' : 'rgba(148,163,184,0.55)';
    ctx.lineWidth = 2; ctx.strokeRect(x, y, w, h);
    const len = pitchMode === 'full' ? 105 : 52.5, cR = Math.max(1, (9.15 / len) * w);
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
        const hl = 11 + (item.width || 3) * 1.5, ang = Math.atan2(p2.y - p1.y, p2.x - p1.x);
        ctx.save(); if (item.type === 'pass') ctx.setLineDash([8, 6]);
        ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x - Math.cos(ang) * hl * 0.6, p2.y - Math.sin(ang) * hl * 0.6); ctx.stroke(); ctx.restore();
        ctx.beginPath(); ctx.moveTo(p2.x, p2.y); ctx.lineTo(p2.x - hl * Math.cos(ang - 0.52), p2.y - hl * Math.sin(ang - 0.52)); ctx.lineTo(p2.x - hl * Math.cos(ang + 0.52), p2.y - hl * Math.sin(ang + 0.52)); ctx.closePath(); ctx.fill();
    } else if (item.type === 'curved') {
        const dx = p2.x - p1.x, dy = p2.y - p1.y, dist = Math.hypot(dx, dy);
        if (dist > 5) {
            const cpx = (p1.x + p2.x) / 2 + (-dy / dist) * (dist * 0.28), cpy = (p1.y + p2.y) / 2 + (dx / dist) * (dist * 0.28);
            ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.quadraticCurveTo(cpx, cpy, p2.x, p2.y); ctx.stroke();
            const ang = Math.atan2(p2.y - cpy, p2.x - cpx), hl = 11 + (item.width || 3) * 1.5;
            ctx.beginPath(); ctx.moveTo(p2.x, p2.y); ctx.lineTo(p2.x - hl * Math.cos(ang - 0.52), p2.y - hl * Math.sin(ang - 0.52)); ctx.lineTo(p2.x - hl * Math.cos(ang + 0.52), p2.y - hl * Math.sin(ang + 0.52)); ctx.closePath(); ctx.fill();
        }
    } else if (item.type === 'connect') {
        ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
    } else if (item.type === 'polygon') {
        ctx.beginPath(); item.points.forEach((pt, i) => { const c = normToCanvas(pt.nx, pt.ny); i === 0 ? ctx.moveTo(c.x, c.y) : ctx.lineTo(c.x, c.y); });
        ctx.closePath(); ctx.globalAlpha = 0.25; ctx.fill(); ctx.globalAlpha = 1; ctx.stroke();
    } else if (item.type === 'ruler') {
        ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
        const lbl = calculateMeters(item.points[0], item.points[1]) + ' m', mx = (p1.x + p2.x) / 2, my = (p1.y + p2.y) / 2;
        ctx.font = 'bold 12px Inter, sans-serif'; const tw = ctx.measureText(lbl).width + 12;
        ctx.fillStyle = '#0f172a'; ctx.fill
