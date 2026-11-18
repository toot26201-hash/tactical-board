const canvas = document.getElementById('tactical-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');

let pitchMode = 'full', showZones = false, showOffside = false, offsideNx = 0.72;
let showCompactness = false, draggingOffside = false, pitchTheme = 'green', customPitchBg = '#133824';
let currentTool = 'select', currentColor = '#facc15', currentStrokeWidth = 3, showPitchLogos = true;
let pitchRect = { x: 0, y: 0, w: 0, h: 0 };

let redTeamMeta = { name: 'الفريق الأول', formation: '5-4-1', primary: '#dc2626', secondary: '#dc2626', striped: false, logoData: null };
let blueTeamMeta = { name: 'الفريق الثاني', formation: '4-3-3', primary: '#0284c7', secondary: '#ffffff', striped: false, logoData: null };

let redLogoImg = null, blueLogoImg = null;
let tempRedLogo = null, tempBlueLogo = null;

let pieces = [], drawings = [], historyStack = [];
let keyframes = [], currentFrameIdx = 0, isPlaying = false, animRaf = null, isRecordingVideo = false;
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
    formationTemplates['5-4-1'].forEach((p, i) => pieces.push({ id: 'red_' + i, type: 'red', nx: p.nx, ny: p.ny, number: p.num, label: p.label, spotlight: false }));
    formationTemplates['4-3-3'].forEach((p, i) => pieces.push({ id: 'blue_' + i, type: 'blue', nx: 1 - p.nx, ny: p.ny, number: p.num, label: p.label, spotlight: false }));
    pieces.push({ id: 'ball_1', type: 'ball', nx: 0.5, ny: 0.5, number: '', label: '' });
    keyframes = [{ pieces: JSON.parse(JSON.stringify(pieces)), drawings: [], title: '', notes: '' }];
    currentFrameIdx = 0;
    loadFrameNotesToUI();
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

function toggleNotesPanel() {
    const panel = document.getElementById('notes-panel');
    panel.classList.toggle('hidden');
    document.getElementById('btn-toggle-notes').classList.toggle('active', !panel.classList.contains('hidden'));
    setTimeout(resizeCanvas, 50);
}

function updateFrameNotes() {
    if (!keyframes[currentFrameIdx]) return;
    keyframes[currentFrameIdx].title = document.getElementById('frame-title-input').value;
    keyframes[currentFrameIdx].notes = document.get
