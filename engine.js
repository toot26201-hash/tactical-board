const canvas = document.getElementById('tactical-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');

let pitchMode = 'full', showZones = false, showOffside = false, offsideNx = 0.72;
let draggingOffside = false, pitchTheme = 'green', customPitchBg = '#133824', currentTool = 'select';
let currentColor = '#facc15', currentStrokeWidth = 3, showPitchLogos = true;
let pitchRect = { x: 0, y: 0, w: 0, h: 0 };

let redTeamMeta = { name: 'الفريق الأول', formation: '5-4-1', primary: '#dc2626', secondary: '#dc2626', striped: false, logoData: null };
let blueTeamMeta = { name: 'الفريق الثاني', formation: '4-3-3', primary: '#0284c7', secondary: '#ffffff', striped: false, logoData: null };

let redLogoImg = null, blueLogoImg = null;
let tempRedLogo = null, tempBlueLogo = null;

let pieces = [], drawings = [], historyStack = [];
let keyframes = [], currentFrameIdx = 0, isPlaying = false, animRaf = null;
let draggingPiece = null, dragOffset = { x: 0, y: 0 }, isDrawing = false, currentDraft = null;
let polygonPoints = [], editingPieceId = null, pendingTextPos = null;

const pitchThemes = {
    green:    { outer: '#0d2618', inner: '#133824', lines: 'rgba(255,255,255,0.68)', stripes: true,  stripeColor: 'rgba(255,255,255,0.03)' },
    classic:  { outer: '#14532d', inner: '#166534', lines: 'rgba(255,255,255,0.85)', stripes: true,  stripeColor: 'rgba(255,255,255,0.05)' },
    navy:     { outer: '#0f172a', inner: '#122c3d', lines: 'rgba(148,163,184,0.65)', stripes: false },
    midnight: { outer: '#09090b', inner: '#1a1a1a', lines: 'rgba(212,175,55,0.65)',  stripes: false },
    opta:     { outer: '#e2e8f0', inner: '#ffffff', lines: 'rgba(30,41,59,0.55)',    stripes: false },
    custom:   { outer: '#0b0f19', inner: customPitchBg, lines: 'rgba(255,255,255,0.75)', stripes: false }
};

const formationTemplates = {
    '5-4-1': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.12,num:'WB',label:'LWB'},{nx:0.20,ny:0.31,num:'CB',label:'LCB'},{nx:0.19,ny:0.5,num:'CB',label:'CB'},{nx:0.20,ny:0.69,num:'CB',label:'RCB'},{nx:0.22,ny:0.88,num:'WB',label:'RWB'},{nx:0.34,ny:0.20,num:'WM',label:'LM'},{nx:0.33,ny:0.41,num:'DM',label:'Pivot'},{nx:0.33,ny:0.59,num:'DM',label:'Pivot'},{nx:0.34,ny:0.80,num:'WM',label:'RM'},{nx:0.47,ny:0.5,num:'9',label:'FWD'}],
    '4-3-3': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.15,num:'3',label:'LB'},{nx:0.20,ny:0.38,num:'4',label:'CB'},{nx:0.20,ny:0.62,num:'5',label:'CB'},{nx:0.22,ny:0.85,num:'2',label:'RB'},{nx:0.33,ny:0.5,num:'6',label:'DM'},{nx:0.39,ny:0.30,num:'8',label:'CM'},{nx:0.39,ny:0.70,num:'10',label:'CM'},{nx:0.46,ny:0.16,num:'11',label:'LW'},{nx:0.48,ny:0.5,num:'9',label:'ST'},{nx:0.46,ny:0.84,num:'7',label:'RW'}],
    '3-5-2': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.20,ny:0.28,num:'CB',label:'LCB'},{nx:0.19,ny:0.5,num:'CB',label:'CB'},{nx:0.20,ny:0.72,num:'CB',label:'RCB'},{nx:0.34,ny:0.10,num:'WB',label:'LWB'},{nx:0.31,ny:0.5,num:'6',label:'DM'},{nx:0.36,ny:0.34,num:'8',label:'CM'},{nx:0.36,ny:0.66,num:'10',label:'CM'},{nx:0.34,ny:0.90,num:'WB',label:'RWB'},{nx:0.47,ny:0.38,num:'9',label:'ST'},{nx:0.47,ny:0.62,num:'11',label:'ST'}],
    '4-2-3-1': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.15,num:'3',label:'LB'},{nx:0.20,ny:0.38,num:'4',label:'CB'},{nx:0.20,ny:0.62,num:'5',label:'CB'},{nx:0.22,ny:0.85,num:'2',label:'RB'},{nx:0.32,ny:0.38,num:'6',label:'Pivot'},{nx:0.32,ny:0.62,num:'8',label:'Pivot'},{nx:0.41,ny:0.18,num:'11',label:'LW'},{nx:0.42,ny:0.5,num:'10',label:'CAM'},{nx:0.41,ny:0.82,num:'7',label:'RW'},{nx:0.48,ny:0.5,num:'9',label:'ST'}],
    '4-4-2': [{nx:0.06,ny:0.5,num:'1',label:'GK'},{nx:0.22,ny:0.15,num:'3',label:'LB'},{nx:0.20,ny:0.38,num:'4',label:'CB'},{nx:0.20,ny:0.62,num:'5',label:'CB'},{nx:0.22,ny:0.85,num:'2',label:'RB'},{nx:0.35,ny:0.16,num:'11',label:'LM'},{nx:0.34,ny:0.40,num:'6',label:'CM'},{nx:0.34,ny:0.60,num:'8',label:'CM'},{nx:0.35,ny:0.84,num:'7',label:'RM'},{nx:0.47,ny:0.38,num:'9',label:'ST'},{nx:0.47,ny:0.62,num:'10',label:'ST'}]
};

const toolHints = {
    select: 'اسحب اللاعبين أو خط التسلل لتحريكهم. انقر مرتين على اللاعب للتعديل.',
    arrow: 'اسحب لرسم سهم حركة مستقيم.',
    curved: 'اسحب لرسم سهم ضغط قوسي لغلق زوايا التمرير.',
    pass: 'اسحب لرسم خط تمرير متقطع.',
    shadow: 'اسحب من المدافع باتجاه زاوية الغلق لرسم ظل دفاعي (Cover Shadow).',
    vision: 'اسحب من اللاعب باتجاه نظره لرسم مخروط الرؤية (Field of Vision).',
    polygon: 'انقر لتحديد زوايا المساحة ثم اضغط إغلاق وتظليل.',
    ruler: 'اسحب لقياس المسافة الحقيقية بالمتر (105×68م).',
    connect: 'اسحب لربط اللاعبين بخط تكتيكي.',
    text: 'انقر لكتابة ملاحظة على الملعب.'
};

function loadLogoImage(team, dataUrl) {
    if (!dataUrl) {
        if (team === 'red') redLogoImg = null; else blueLogoImg = null;
        render(); return;
    }
    const img = new Image();
    img.onload = () => {
        if (team === 'red') redLogoImg = img; else blueLogoImg = img;
        render();
    };
    img.src = dataUrl;
}

function handleLogoUpload(team, event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {
        const res = e.target.result;
        if (team === 'red') {
            tempRedLogo = res;
            const prev = document.getElementById('preview-red-logo');
            prev.src = res; prev.classList.remove('hidden');
        } else {
            tempBlueLogo = res;
            const prev = document.getElementById('preview-blue-logo');
            prev.src = res; prev.classList.remove('hidden');
        }
    };
    reader.readAsDataURL(file);
}

function clearTeamLogo(team) {
    if (team === 'red') {
        tempRedLogo = null;
        const prev = document.getElementById('preview-red-logo');
        prev.src = ''; prev.classList.add('hidden');
    } else {
        tempBlueLogo = null;
        const prev = document.getElementById('preview-blue-logo');
        prev.src = ''; prev.classList.add('hidden');
    }
}

function initDefaultPieces() {
    pieces = [];
    formationTemplates['5-4-1'].forEach((p, i) => pieces.push({ id: 'red_' + i, type: 'red', nx: p.nx, ny: p.ny, number: p.num, label: p.label }));
    formationTemplates['4-3-3'].forEach((p, i) => pieces.push({ id: 'blue_' + i, type: 'blue', nx: 1 - p.nx, ny: p.ny, number: p.num, label: p.label }));
    pieces.push({ id: 'ball_1', type: 'ball', nx: 0.5, ny: 0.5, number: '', label: '' });
    keyframes = [{ pieces: JSON.parse(JSON.stringify(pieces)), drawings: [] }];
    currentFrameIdx = 0;
    updateTeamBanner();
    renderFramesBar();
}

function updateTeamBanner() {
    document.getElementById('display-red-name').textContent = redTeamMeta.name;
    document.getElementById('display-red-form').textContent = redTeamMeta.formation;
    document.getElementById('badge-red-color').style.backgroundColor = redTeamMeta.primary;
    const rLogo = document.getElementById('banner-red-logo');
    if (redTeamMeta.logoData) { rLogo.src = redTeamMeta.logoData; rLogo.classList.remove('hidden'); }
    else { rLogo.src = ''; rLogo.classList.add('hidden'); }

    document.getElementById('display-blue-name').textContent = blueTeamMeta.name;
    document.getElementById('display-blue-form').textContent = blueTeamMeta.formation;
    document.getElementById('badge-blue-color').style.backgroundColor = blueTeamMeta.primary;
    const bLogo = document.getElementById('banner-blue-logo');
    if (blueTeamMeta.logoData) { bLogo.src = blueTeamMeta.logoData; bLogo.classList.remove('hidden'); }
    else { bLogo.src = ''; bLogo.classList.add('hidden'); }
}

function setPitchTheme(theme) {
    pitchTheme = theme;
    if (theme !== 'custom' && pitchThemes[theme]) {
        document.getElementById('custom-pitch-color').value = pitchThemes[theme].inner;
    }
    render();
}

function setCustomPitchColor(hex) {
    customPitchBg = hex;
    pitchThemes.custom.inner = hex;
    pitchTheme = 'custom';
    document.getElementById('pitch-theme-select').value = 'custom';
    render();
}

function syncCurrentFrame() {
    if (keyframes[currentFrameIdx]) {
        keyframes[currentFrameIdx] = { pieces: JSON.parse(JSON.stringify(pieces)), drawings: JSON.parse(JSON.stringify(drawings)) };
    }
}

function addKeyframe() {
    syncCurrentFrame();
    const clone = { pieces: JSON.parse(JSON.stringify(pieces)), drawings: JSON.parse(JSON.stringify(drawings)) };
    keyframes.splice(currentFrameIdx + 1, 0, clone);
    currentFrameIdx++;
    renderFramesBar();
    showToast(`تمت إضافة الإطار ${currentFrameIdx + 1}`);
}

function selectKeyframe(idx) {
    if (isPlaying) stopAnimation();
    syncCurrentFrame();
    currentFrameIdx = idx;
    pieces = JSON.parse(JSON.stringify(keyframes[idx].pieces));
    drawings = JSON.parse(JSON.stringify(keyframes[idx].drawings));
    renderFramesBar();
    render();
}

function deleteCurrentKeyframe() {
    if (keyframes.length <= 1) return showToast('يجب بقاء إطار واحد على الأقل');
    keyframes.splice(currentFrameIdx, 1);
    currentFrameIdx = Math.max(0, currentFrameIdx - 1);
    pieces = JSON.parse(JSON.stringify(keyframes[currentFrameIdx].pieces));
    drawings = JSON.parse(JSON.stringify(keyframes[currentFrameIdx].drawings));
    renderFramesBar();
    render();
}

function renderFramesBar() {
    const bar = document.getElementById('frames-list');
    bar.innerHTML = '';
    keyframes.forEach((_, idx) => {
        const btn = document.createElement('button');
        btn.className = `frame-btn px-2.5 py-1 rounded text-xs font-en font-bold border border-slate-700 transition ${idx === currentFrameIdx ? 'active' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`;
        btn.textContent = `F${idx + 1}`;
        btn.onclick = () => selectKeyframe(idx);
        bar.appendChild(btn);
    });
}

function togglePlayAnimation() {
    if (isPlaying) { stopAnimation(); return; }
    if (keyframes.length < 2) return showToast('أضف إطاراً ثانياً أولاً لتحريك اللاعبين');
    syncCurrentFrame();
    isPlaying = true;
    document.getElementById('play-icon').className = 'fa-solid fa-stop';
    document.getElementById('play-label').textContent = 'إيقاف';

    let segIdx = 0;
    let startTime = performance.now();
    const duration = parseInt(document.getElementById('anim-speed').value) || 900;

    function step(now) {
        if (!isPlaying) return;
        const elapsed = now - startTime;
        const t = Math.min(1, elapsed / duration);
        const ease = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;

        const fA = keyframes[segIdx];
        const fB = keyframes[segIdx + 1];
        pieces = fB.pieces.map(pb => {
            const pa = fA.pieces.find(x => x.id === pb.id) || pb;
            return { ...pb, nx: pa.nx + (pb.nx - pa.nx) * ease, ny: pa.ny + (pb.ny - pa.ny) * ease };
        });
        drawings = fA.drawings;
        currentFrameIdx = segIdx;
        renderFramesBar();
        render();

        if (t < 1) {
            animRaf = requestAnimationFrame(step);
        } else {
            segIdx++;
            if (segIdx < keyframes.length - 1) {
                startTime = performance.now();
                animRaf = requestAnimationFrame(step);
            } else {
                currentFrameIdx = keyframes.length - 1;
                pieces = JSON.parse(JSON.stringify(keyframes[currentFrameIdx].pieces));
                drawings = JSON.parse(JSON.stringify(keyframes[currentFrameIdx].drawings));
                renderFramesBar();
                render();
                stopAnimation();
            }
        }
    }
    animRaf = requestAnimationFrame(step);
}

function stopAnimation() {
    isPlaying = false;
    if (animRaf) cancelAnimationFrame(animRaf);
    document.getElementById('play-icon').className = 'fa-solid fa-play';
    document.getElementById('play-label').textContent = 'تشغيل الحركة';
}

function loadSetPiece(type) {
    if (!type) return;
    saveHistory();
    drawings = [];
    if (type === 'corner_att') {
        setPitchMode('half');
        pieces = [
            { id: 'r_gk', type: 'red', nx: 0.05, ny: 0.5, number: '1', label: 'GK' },
            { id: 'r1', type: 'red', nx: 0.14, ny: 0.36, number: '4', label: 'Zonal' },
            { id: 'r2', type: 'red', nx: 0.14, ny: 0.46, number: '5', label: 'Zonal' },
            { id: 'r3', type: 'red', nx: 0.14, ny: 0.56, number: '6', label: 'Zonal' },
            { id: 'r4', type: 'red', nx: 0.22, ny: 0.32, number: '2', label: 'Man' },
            { id: 'r5', type: 'red', nx: 0.24, ny: 0.48, number: '8', label: 'Man' },
            { id: 'b_taker', type: 'blue', nx: 0.02, ny: 0.03, number: '10', label: 'Taker' },
            { id: 'b_short', type: 'blue', nx: 0.12, ny: 0.10, number: '7', label: 'Short' },
            { id: 'b1', type: 'blue', nx: 0.23, ny: 0.31, number: '4', label: 'Near Post' },
            { id: 'b2', type: 'blue', nx: 0.26, ny: 0.47, number: '9', label: 'Target' },
            { id: 'b3', type: 'blue', nx: 0.24, ny: 0.63, number: '5', label: 'Far Post' },
            { id: 'b_edge', type: 'blue', nx: 0.36, ny: 0.50, number: '8', label: 'Edge Box' },
            { id: 'ball_1', type: 'ball', nx: 0.03, ny: 0.04, number: '', label: '' }
        ];
        drawings.push({ type: 'curved', points: [{ nx: 0.03, ny: 0.04 }, { nx: 0.15, ny: 0.44 }], color: '#facc15', width: 3 });
        drawings.push({ type: 'arrow', points: [{ nx: 0.23, ny: 0.31 }, { nx: 0.13, ny: 0.38 }], color: '#38bdf8', width: 3 });
    } else if (type === 'fk_direct') {
        setPitchMode('half');
        pieces = [
            { id: 'r_gk', type: 'red', nx: 0.05, ny: 0.56, number: '1', label: 'GK' },
            { id: 'rw1', type: 'red', nx: 0.25, ny: 0.39, number: '4', label: 'Wall' },
            { id: 'rw2', type: 'red', nx: 0.25, ny: 0.43, number: '5', label: 'Wall' },
            { id: 'rw3', type: 'red', nx: 0.25, ny: 0.47, number: '6', label: 'Wall' },
            { id: 'rw4', type: 'red', nx: 0.25, ny: 0.51, number: '8', label: 'Wall' },
            { id: 'b_fk1', type: 'blue', nx: 0.44, ny: 0.42, number: '10', label: 'Shooter' },
            { id: 'b_fk2', type: 'blue', nx: 0.43, ny: 0.48, number: '7', label: 'Decoy' },
            { id: 'ball_1', type: 'ball', nx: 0.41, ny: 0.44, number: '', label: '' }
        ];
        drawings.push({ type: 'curved', points: [{ nx: 0.41, ny: 0.44 }, { nx: 0.04, ny: 0.41 }], color: '#facc15', width: 3 });
    } else if (type === 'gk_buildup') {
        setPitchMode('full');
        pieces = [
            { id: 'r_gk', type: 'red', nx: 0.05, ny: 0.5, number: '1', label: 'GK' },
            { id: 'r_cb1', type: 'red', nx: 0.14, ny: 0.32, number: '4', label: 'LCB' },
            { id: 'r_cb2', type: 'red', nx: 0.14, ny: 0.68, number: '5', label: 'RCB' },
            { id: 'r_dm', type: 'red', nx: 0.24, ny: 0.50, number: '6', label: 'Pivot' },
            { id: 'r_lb', type: 'red', nx: 0.28, ny: 0.12, number: '3', label: 'LB' },
            { id: 'r_rb', type: 'red', nx: 0.28, ny: 0.88, number: '2', label: 'RB' },
            { id: 'b_st', type: 'blue', nx: 0.22, ny: 0.42, number: '9', label: 'Press' },
            { id: 'b_lw', type: 'blue', nx: 0.25, ny: 0.22, number: '11', label: 'LW' },
            { id: 'b_rw', type: 'blue', nx: 0.25, ny: 0.78, number: '7', label: 'RW' },
            { id: 'ball_1', type: 'ball', nx: 0.07, ny: 0.5, number: '', label: '' }
        ];
        drawings.push({ type: 'shadow', points: [{ nx: 0.22, ny: 0.42 }, { nx: 0.25, ny: 0.52 }], color: '#ef4444', width: 3 });
    }
    syncCurrentFrame();
    render();
    showToast('تم تحميل القالب التكتيكي');
}

function resizeCanvas() {
    const rect = container.getBoundingClientRect();
    const bannerH = 44;
    const timelineH = 54;
    const availW = Math.max(320, rect.width - 28);
    const availH = Math.max(220, rect.height - bannerH - timelineH - 24);

    const targetRatio = pitchMode === 'full' ? (105 / 68) : (68 / 52.5);
    let finalW = availW;
    let finalH = availW / targetRatio;

    if (finalH > availH) {
        finalH = availH;
        finalW = availH * targetRatio;
    }

    if (finalW <= 10 || finalH <= 10) return;

    const dpr = window.devicePixelRatio || 1;
    canvas.width = finalW * dpr;
    canvas.height = finalH * dpr;
    canvas.style.width = `${finalW}px`;
    canvas.style.height = `${finalH}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const m = Math.max(10, Math.min(finalW, finalH) * 0.025);
    pitchRect = {
        x: m,
        y: m,
        w: finalW - m * 2,
        h: finalH - m * 2,
        canvasW: finalW,
        canvasH: finalH
    };
    render();
}

const normToCanvas = (nx, ny) => ({ x: pitchRect.x + nx * pitchRect.w, y: pitchRect.y + ny * pitchRect.h });
const canvasToNorm = (cx, cy) => ({ nx: Math.max(0, Math.min(1, (cx - pitchRect.x) / pitchRect.w)), ny: Math.max(0, Math.min(1, (cy - pitchRect.y) / pitchRect.h)) });
const calculateMeters = (p1, p2) => Math.hypot((p2.nx - p1.nx) * (pitchMode === 'full' ? 105 : 52.5), (p2.ny - p1.ny) * 68).toFixed(1);

function drawPitch() {
    const { x, y, w, h, canvasW, canvasH } = pitchRect;
    if (w <= 0 || h <= 0) return;

    const th = pitchThemes[pitchTheme] || pitchThemes.green;
    ctx.fillStyle = th.outer;
    ctx.fillRect(0, 0, canvasW, canvasH);
    ctx.fillStyle = th.inner;
    ctx.fillRect(x, y, w, h);

    if (th.stripes) {
        const s = pitchMode === 'full' ? 14 : 8, sw = w / s;
        for (let i = 0; i < s; i += 2) {
            ctx.fillStyle = th.stripeColor;
            ctx.fillRect(x + i * sw, y, sw, h);
        }
    }

    if (showZones) {
        const penH = (40.32 / 68) * h, goalH = (18.32 / 68) * h, topW = (h - penH) / 2, hsH = (penH - goalH) / 2;
        const y1 = y + topW, y2 = y1 + hsH, y3 = y2 + goalH, y4 = y3 + hsH;
        ctx.fillStyle = pitchTheme === 'opta' ? 'rgba(212,175,55,0.16)' : 'rgba(250,204,21,0.08)';
        ctx.fillRect(x, y1, w, hsH); ctx.fillRect(x, y3, w, hsH);
        ctx.save(); ctx.strokeStyle = pitchTheme === 'opta' ? 'rgba(180,130,20,0.6)' : 'rgba(250,204,21,0.42)';
        ctx.setLineDash([6, 6]); ctx.lineWidth = 1.2;
        [y1, y2, y3, y4].forEach(ly => { ctx.beginPath(); ctx.moveTo(x, ly); ctx.lineTo(x + w, ly); ctx.stroke(); });
        ctx.strokeStyle = 'rgba(56,189,248,0.4)';
        [x + w / 3, x + (2 * w) / 3].forEach(lx => { ctx.beginPath(); ctx.moveTo(lx, y); ctx.lineTo(lx, y + h); ctx.stroke(); });
        ctx.restore();
    }

    ctx.strokeStyle = th.lines;
    ctx.lineWidth = 2; ctx.strokeRect(x, y, w, h);
    const len = pitchMode === 'full' ? 105 : 52.5, cR = Math.max(1, (9.15 / len) * w);
    const penW = (16.5 / len) * w, penH = (40.32 / 68) * h, penY = y + (h - penH) / 2;
    const goalW = (5.5 / len) * w, goalH = (18.32 / 68) * h, goalY = y + (h - goalH) / 2;
    const spot = (11 / len) * w, netH = (7.32 / 68) * h;

    ctx.strokeRect(x, penY, penW, penH); ctx.strokeRect(x, goalY, goalW, goalH);
    ctx.fillStyle = th.lines; ctx.beginPath(); ctx.arc(x + spot, y + h / 2, 2.5, 0, Math.PI * 2); ctx.fill();
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

    if (showPitchLogos) {
        const logoSize = Math.max(26, Math.min(44, w * 0.048));
        ctx.save();
        ctx.globalAlpha = 0.82;
        if (redLogoImg) {
            ctx.drawImage(redLogoImg, x + 12, y + 12, logoSize, logoSize);
        }
        if (blueLogoImg) {
            ctx.drawImage(blueLogoImg, x + w - logoSize - 12, y + 12, logoSize, logoSize);
        }
        ctx.restore();
    }

    if (showOffside) {
        const ox = x + offsideNx * w;
        ctx.save();
        ctx.strokeStyle = '#f43f5e'; ctx.setLineDash([7, 5]); ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(ox, y); ctx.lineTo(ox, y + h); ctx.stroke();
        ctx.fillStyle = '#f43f5e'; ctx.fillRect(ox - 24, y + 4, 48, 15);
        ctx.fillStyle = '#fff'; ctx.font = 'bold 9px Inter, sans-serif'; ctx.textAlign = 'center';
        ctx.fillText('OFFSIDE', ox, y + 14);
        ctx.restore();
    }
}

function renderDrawingItem(item) {
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
    } else if (item.type === 'shadow') {
        const ang = Math.atan2(p2.y - p1.y, p2.x - p1.x), dist = Math.max(45, Math.hypot(p2.x - p1.x, p2.y - p1.y) * 2.4);
        const spread = 0.26;
        const grad = ctx.createRadialGradient(p1.x, p1.y, 5, p1.x, p1.y, dist);
        grad.addColorStop(0, hexToRgba(item.color, 0.42));
        grad.addColorStop(1, hexToRgba(item.color, 0.03));
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.arc(p1.x, p1.y, dist, ang - spread, ang + spread); ctx.closePath(); ctx.fill();
    } else if (item.type === 'vision') {
        const ang = Math.atan2(p2.y - p1.y, p2.x - p1.x), dist = Math.max(55, Math.hypot(p2.x - p1.x, p2.y - p1.y));
        const spread = 0.58;
        ctx.fillStyle = hexToRgba(item.color, 0.18);
        ctx.strokeStyle = hexToRgba(item.color, 0.55);
        ctx.setLineDash([4, 4]);
        ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.arc(p1.x, p1.y, dist, ang - spread, ang + spread); ctx.closePath(); ctx.fill(); ctx.stroke();
    } else if (item.type === 'connect') {
        ctx.setLineDash([4, 4]); ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
    } else if (item.type === 'polygon') {
        ctx.beginPath(); item.points.forEach((pt, i) => { const c = normToCanvas(pt.nx, pt.ny); i === 0 ? ctx.moveTo(c.x, c.y) : ctx.lineTo(c.x, c.y); });
        ctx.closePath(); ctx.fillStyle = hexToRgba(item.color, 0.24); ctx.fill(); ctx.stroke();
    } else if (item.type === 'ruler') {
        ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
        const lbl = calculateMeters(item.points[0], item.points[1]) + ' m', mx = (p1.x + p2.x) / 2, my = (p1.y + p2.y) / 2;
        ctx.font = 'bold 12px Inter, sans-serif'; const tw = ctx.measureText(lbl).width + 12;
        ctx.fillStyle = '#0f172a'; ctx.fillRect(mx - tw / 2, my - 11, tw, 22); ctx.strokeRect(mx - tw / 2, my - 11, tw, 22);
        ctx.fillStyle = item.color; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(lbl, mx, my);
    } else if (item.type === 'text') {
        ctx.font = 'bold 13px Cairo, sans-serif'; const tw = ctx.measureText(item.text).width + 16;
        ctx.fillStyle = 'rgba(15,23,42,0.9)'; ctx.fillRect(p1.x - tw / 2, p1.y - 13, tw, 26); ctx.strokeRect(p1.x - tw / 2, p1.y - 13, tw, 26);
        ctx.fillStyle = item.color; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(item.text, p1.x, p1.y);
    }
    ctx.restore();
}

function drawPieces() {
    const r = Math.max(13, Math.min(18, pitchRect.w * 0.021));
    pieces.forEach(p => {
        const pos = normToCanvas(p.nx, p.ny); ctx.save();
        if (p.type === 'red' || p.type === 'blue') {
            const meta = p.type === 'red' ? redTeamMeta : blueTeamMeta;
            ctx.beginPath(); ctx.arc(pos.x, pos.y, r, 0, Math.PI * 2); ctx.clip();
            ctx.fillStyle = meta.primary;
            ctx.fillRect(pos.x - r, pos.y - r, r * 2, r * 2);
            if (meta.striped) {
                ctx.fillStyle = meta.secondary;
                ctx.fillRect(pos.x - r * 0.45, pos.y - r, r * 0.35, r * 2);
                ctx.fillRect(pos.x + r * 0.15, pos.y - r, r * 0.35, r * 2);
            }
            ctx.restore(); ctx.save();
            ctx.beginPath(); ctx.arc(pos.x, pos.y, r, 0, Math.PI * 2);
            ctx.strokeStyle = pitchTheme === 'opta' ? '#0f172a' : '#fff'; ctx.lineWidth = 2; ctx.stroke();

            ctx.font = `bold ${r * 0.72}px Inter, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.strokeStyle = 'rgba(0,0,0,0.75)'; ctx.lineWidth = 3; ctx.strokeText(p.number || '', pos.x, pos.y);
            ctx.fillStyle = '#fff'; ctx.fillText(p.number || '', pos.x, pos.y);

            if (p.label) {
                ctx.font = 'bold 10px Cairo, sans-serif'; const lw = ctx.measureText(p.label).width + 8;
                ctx.fillStyle = 'rgba(15,23,42,0.88)'; ctx.fillRect(pos.x - lw / 2, pos.y + r + 3, lw, 14);
                ctx.fillStyle = '#f8fafc'; ctx.fillText(p.label, pos.x, pos.y + r + 10);
            }
        } else if (p.type === 'ball') {
            ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(pos.x, pos.y, r * 0.62, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 2; ctx.stroke();
        } else if (p.type === 'cone') {
            const cr = r * 0.65; ctx.fillStyle = '#f97316'; ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5;
            ctx.beginPath(); ctx.moveTo(pos.x, pos.y - cr); ctx.lineTo(pos.x + cr, pos.y + cr * 0.8); ctx.lineTo(pos.x - cr, pos.y + cr * 0.8); ctx.closePath(); ctx.fill(); ctx.stroke();
        }
        ctx.restore();
    });
}

function render() {
    drawPitch();
    drawings.forEach(renderDrawingItem);
    if (currentDraft) renderDrawingItem(currentDraft);
    if (polygonPoints.length > 0) renderDrawingItem({ type: 'polygon', points: polygonPoints, color: currentColor, width: currentStrokeWidth });
    drawPieces();
}

function getPointerPos(e) {
    const rect = canvas.getBoundingClientRect();
    const cx = e.touches ? e.touches[0].clientX : e.clientX, cy = e.touches ? e.touches[0].clientY : e.clientY;
    return { x: cx - rect.left, y: cy - rect.top };
}

canvas.addEventListener('mousedown', e => {
    const pos = getPointerPos(e), norm = canvasToNorm(pos.x, pos.y);
    if (showOffside && Math.abs(pos.x - (pitchRect.x + offsideNx * pitchRect.w)) < 12) {
        draggingOffside = true; return;
    }
    if (currentTool === 'select') {
        const hit = [...pieces].reverse().find(p => { const c = normToCanvas(p.nx, p.ny); return Math.hypot(pos.x - c.x, pos.y - c.y) <= 22; });
        if (hit) { saveHistory(); draggingPiece = hit; const c = normToCanvas(hit.nx, hit.ny); dragOffset = { x: pos.x - c.x, y: pos.y - c.y }; }
    } else if (currentTool === 'polygon') {
        polygonPoints.push(norm); document.getElementById('polygon-controls').classList.remove('hidden'); render();
    } else if (currentTool === 'text') {
        pendingTextPos = norm; document.getElementById('annotation-input').value = ''; document.getElementById('text-modal').classList.remove('hidden');
    } else {
        isDrawing = true; currentDraft = { type: currentTool, points: [norm, norm], color: currentColor, width: currentStrokeWidth };
    }
});

canvas.addEventListener('mousemove', e => {
    if (draggingOffside) { const pos = getPointerPos(e); offsideNx = canvasToNorm(pos.x, pos.y).nx; render(); return; }
    if (draggingPiece) { const pos = getPointerPos(e), n = canvasToNorm(pos.x - dragOffset.x, pos.y - dragOffset.y); draggingPiece.nx = n.nx; draggingPiece.ny = n.ny; render(); }
    else if (isDrawing && currentDraft) { const pos = getPointerPos(e); currentDraft.points[1] = canvasToNorm(pos.x, pos.y); render(); }
});

window.addEventListener('mouseup', () => {
    if (draggingOffside) { draggingOffside = false; return; }
    if (draggingPiece) { draggingPiece = null; syncCurrentFrame(); render(); }
    else if (isDrawing && currentDraft) {
        isDrawing = false;
        if (Math.hypot(currentDraft.points[1].nx - currentDraft.points[0].nx, currentDraft.points[1].ny - currentDraft.points[0].ny) > 0.015) {
            saveHistory(); drawings.push(currentDraft); syncCurrentFrame();
        }
        currentDraft = null; render();
    }
});

canvas.addEventListener('dblclick', e => {
    const pos = getPointerPos(e);
    const hit = [...pieces].reverse().find(p => { const c = normToCanvas(p.nx, p.ny); return Math.hypot(pos.x - c.x, pos.y - c.y) <= 22; });
    if (hit && (hit.type === 'red' || hit.type === 'blue')) {
        editingPieceId = hit.id; document.getElementById('edit-number').value = hit.number || ''; document.getElementById('edit-label').value = hit.label || '';
        document.getElementById('edit-modal').classList.remove('hidden');
    }
});

function exportJSON() {
    syncCurrentFrame();
    const data = { redTeamMeta, blueTeamMeta, pitchMode, keyframes };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `tactic_${Date.now()}.json`;
    a.click();
    showToast('تم حفظ ملف السيناريو والشعارات بنجاح');
}

function importJSON(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
        try {
            const data = JSON.parse(ev.target.result);
            if (data.redTeamMeta) {
                redTeamMeta = data.redTeamMeta;
                loadLogoImage('red', redTeamMeta.logoData);
            }
            if (data.blueTeamMeta) {
                blueTeamMeta = data.blueTeamMeta;
                loadLogoImage('blue', blueTeamMeta.logoData);
            }
            if (data.keyframes && data.keyframes.length) {
                keyframes = data.keyframes;
                currentFrameIdx = 0;
                pieces = JSON.parse(JSON.stringify(keyframes[0].pieces));
                drawings = JSON.parse(JSON.stringify(keyframes[0].drawings));
            }
            updateTeamBanner(); renderFramesBar(); resizeCanvas();
            showToast('تم تحميل السيناريو بنجاح');
        } catch { showToast('ملف غير صالح'); }
    };
    reader.readAsText(file);
}

function setTool(t) { currentTool = t; document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active')); document.getElementById('tool-' + t)?.classList.add('active'); document.getElementById('tool-hint-text').textContent = toolHints[t] || ''; }
function setColor(hex) { currentColor = hex; document.querySelectorAll('.color-btn').forEach(b => b.classList.toggle('ring-2', b.dataset.color === hex)); }
function setPitchMode(m) { pitchMode = m; document.querySelectorAll('.pitch-mode-btn').forEach(b => b.classList.remove('bg-slate-700', 'text-white')); document.getElementById('btn-pitch-' + m).classList.add('bg-slate-700', 'text-white'); resizeCanvas(); }
function toggleZones() { showZones = !showZones; render(); }
function toggleOffside() { showOffside = !showOffside; render(); }
function saveHistory() { historyStack.push({ pieces: JSON.parse(JSON.stringify(pieces)), drawings: JSON.parse(JSON.stringify(drawings)) }); if (historyStack.length > 25) historyStack.shift(); }
function undoAction() { if (!historyStack.length) return; const prev = historyStack.pop(); pieces = prev.pieces; drawings = prev.drawings; syncCurrentFrame(); render(); }
function clearDrawings() { saveHistory(); drawings = []; polygonPoints = []; syncCurrentFrame(); render(); }
function resetBoard() { saveHistory(); drawings = []; initDefaultPieces(); render(); }
function addPiece(type) { saveHistory(); pieces.push({ id: type + Date.now(), type, nx: 0.5, ny: 0.5, number: type === 'red' || type === 'blue' ? '12' : '', label: '' }); syncCurrentFrame(); render(); }
function finishPolygon() { if (polygonPoints.length >= 3) { saveHistory(); drawings.push({ type: 'polygon', points: [...polygonPoints], color: currentColor, width: currentStrokeWidth }); syncCurrentFrame(); } cancelPolygon(); }
function cancelPolygon() { polygonPoints = []; document.getElementById('polygon-controls').classList.add('hidden'); render(); }
function closeTextModal() { document.getElementById('text-modal').classList.add('hidden'); }
function confirmTextAnnotation() { const v = document.getElementById('annotation-input').value.trim(); if (v && pendingTextPos) { saveHistory(); drawings.push({ type: 'text', points: [pendingTextPos], color: currentColor, text: v }); syncCurrentFrame(); render(); } closeTextModal(); }
function closeEditModal() { document.getElementById('edit-modal').classList.add('hidden'); }
function saveEditModal() { const p = pieces.find(x => x.id === editingPieceId); if (p) { saveHistory(); p.number = document.getElementById('edit-number').value; p.label = document.getElementById('edit-label').value; syncCurrentFrame(); render(); } closeEditModal(); }
function deleteSelectedPiece() { saveHistory(); pieces = pieces.filter(x => x.id !== editingPieceId); syncCurrentFrame(); closeEditModal(); render(); }

function openLineupModal() {
    document.getElementById('input-red-team-name').value = redTeamMeta.name;
    document.getElementById('select-red-formation').value = redTeamMeta.formation;
    document.getElementById('red-kit-primary').value = redTeamMeta.primary;
    document.getElementById('red-kit-secondary').value = redTeamMeta.secondary;
    document.getElementById('red-kit-striped').checked = redTeamMeta.striped;
    tempRedLogo = redTeamMeta.logoData;
    const prevR = document.getElementById('preview-red-logo');
    if (tempRedLogo) { prevR.src = tempRedLogo; prevR.classList.remove('hidden'); } else { prevR.src = ''; prevR.classList.add('hidden'); }

    document.getElementById('input-blue-team-name').value = blueTeamMeta.name;
    document.getElementById('select-blue-formation').value = blueTeamMeta.formation;
    document.getElementById('blue-kit-primary').value = blueTeamMeta.primary;
    document.getElementById('blue-kit-secondary').value = blueTeamMeta.secondary;
    document.getElementById('blue-kit-striped').checked = blueTeamMeta.striped;
    tempBlueLogo = blueTeamMeta.logoData;
    const prevB = document.getElementById('preview-blue-logo');
    if (tempBlueLogo) { prevB.src = tempBlueLogo; prevB.classList.remove('hidden'); } else { prevB.src = ''; prevB.classList.add('hidden'); }

    populateLineupInputs('red', redTeamMeta.formation, true);
    populateLineupInputs('blue', blueTeamMeta.formation, true);
    document.getElementById('lineup-modal').classList.remove('hidden');
}

function closeLineupModal() { document.getElementById('lineup-modal').classList.add('hidden'); }
function populateLineupInputs(team, form, keep) {
    const el = document.getElementById(team + '-players-list'), tpl = formationTemplates[form], cur = pieces.filter(p => p.type === team); el.innerHTML = '';
    tpl.forEach((s, i) => {
        const num = keep && cur[i] ? cur[i].number : s.num, lbl = keep && cur[i] ? cur[i].label : s.label;
        el.innerHTML += `<div class="flex gap-1.5"><input data-team="${team}" data-idx="${i}" data-f="num" value="${num}" class="w-12 bg-slate-950 border border-slate-700 rounded px-1.5 py-1 text-xs text-center text-white"><input data-team="${team}" data-idx="${i}" data-f="lbl" value="${lbl}" class="flex-1 bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs text-white"></div>`;
    });
}

function applyBothTeamsLineups() {
    saveHistory();
    redTeamMeta = {
        name: document.getElementById('input-red-team-name').value || 'الفريق الأول',
        formation: document.getElementById('select-red-formation').value,
        primary: document.getElementById('red-kit-primary').value,
        secondary: document.getElementById('red-kit-secondary').value,
        striped: document.getElementById('red-kit-striped').checked,
        logoData: tempRedLogo
    };
    blueTeamMeta = {
        name: document.getElementById('input-blue-team-name').value || 'الفريق الثاني',
        formation: document.getElementById('select-blue-formation').value,
        primary: document.getElementById('blue-kit-primary').value,
        secondary: document.getElementById('blue-kit-secondary').value,
        striped: document.getElementById('blue-kit-striped').checked,
        logoData: tempBlueLogo
    };
    loadLogoImage('red', redTeamMeta.logoData);
    loadLogoImage('blue', blueTeamMeta.logoData);

    pieces = pieces.filter(p => p.type !== 'red' && p.type !== 'blue');
    formationTemplates[redTeamMeta.formation].forEach((s, i) => pieces.push({ id: 'red_' + i, type: 'red', nx: s.nx, ny: s.ny, number: document.querySelector(`input[data-team="red"][data-idx="${i}"][data-f="num"]`).value, label: document.querySelector(`input[data-team="red"][data-idx="${i}"][data-f="lbl"]`).value }));
    formationTemplates[blueTeamMeta.formation].forEach((s, i) => pieces.push({ id: 'blue_' + i, type: 'blue', nx: 1 - s.nx, ny: s.ny, number: document.querySelector(`input[data-team="blue"][data-idx="${i}"][data-f="num"]`).value, label: document.querySelector(`input[data-team="blue"][data-idx="${i}"][data-f="lbl"]`).value }));
    updateTeamBanner(); syncCurrentFrame(); closeLineupModal(); render();
    showToast('تم تحديث بيانات وشعارات الأندية');
}

function exportPNG() {
    const a = document.createElement('a');
    a.download = `tactic_${Date.now()}.png`;
    a.href = canvas.toDataURL('image/png', 1.0);
    a.click();
    showToast('تم تصدير الصورة بالشعارات');
}

function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${alpha})`;
}

let toastTimer = null;
function showToast(msg) {
    const el = document.getElementById('toast-msg');
    el.textContent = msg; el.classList.remove('opacity-0');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.add('opacity-0'), 2000);
}

const ro = new ResizeObserver(() => resizeCanvas());
ro.observe(container);
window.addEventListener('resize', resizeCanvas);
window.addEventListener('load', () => {
    initDefaultPieces();
    resizeCanvas();
    setTimeout(resizeCanvas, 150);
});
initDefaultPieces();
setTimeout(resizeCanvas, 100);
