const canvas = document.getElementById('tactical-canvas');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvas-container');

let pitchMode = 'full';
let showZones = false;
let pitchTheme = 'green';
let currentTool = 'select';
let currentColor = '#facc15';
let currentStrokeWidth = 3;
let pitchRect = { x: 0, y: 0, w: 0, h: 0 };

let redTeamMeta = { name: 'الفريق الأحمر', formation: '5-4-1' };
let blueTeamMeta = { name: 'الفريق الأزرق', formation: '4-3-3' };

let pieces = [];
let drawings = [];
let historyStack = [];

let draggingPiece = null;
let dragOffset = { x: 0, y: 0 };
let isDrawing = false;
let currentDraft = null;
let polygonPoints = [];
let editingPieceId = null;
let pendingTextPos = null;

const formationTemplates = {
    '5-4-1': [
        { nx: 0.06, ny: 0.50, num: '1', label: 'GK' },
        { nx: 0.22, ny: 0.12, num: 'WB', label: 'LWB' },
        { nx: 0.20, ny: 0.31, num: 'CB', label: 'LCB' },
        { nx: 0.19, ny: 0.50, num: 'CB', label: 'CB' },
        { nx: 0.20, ny: 0.69, num: 'CB', label: 'RCB' },
        { nx: 0.22, ny: 0.88, num: 'WB', label: 'RWB' },
        { nx: 0.34, ny: 0.20, num: 'WM', label: 'LM' },
        { nx: 0.33, ny: 0.41, num: 'DM', label: 'Pivot' },
        { nx: 0.33, ny: 0.59, num: 'DM', label: 'Pivot' },
        { nx: 0.34, ny: 0.80, num: 'WM', label: 'RM' },
        { nx: 0.47, ny: 0.50, num: '9', label: 'FWD' }
    ],
    '4-3-3': [
        { nx: 0.06, ny: 0.50, num: '1', label: 'GK' },
        { nx: 0.22, ny: 0.15, num: '3', label: 'LB' },
        { nx: 0.20, ny: 0.38, num: '4', label: 'CB' },
        { nx: 0.20, ny: 0.62, num: '5', label: 'CB' },
        { nx: 0.22, ny: 0.85, num: '2', label: 'RB' },
        { nx: 0.33, ny: 0.50, num: '6', label: 'DM' },
        { nx: 0.39, ny: 0.30, num: '8', label: 'CM' },
        { nx: 0.39, ny: 0.70, num: '10', label: 'CM' },
        { nx: 0.46, ny: 0.16, num: '11', label: 'LW' },
        { nx: 0.48, ny: 0.50, num: '9', label: 'ST' },
        { nx: 0.46, ny: 0.84, num: '7', label: 'RW' }
    ],
    '3-5-2': [
        { nx: 0.06, ny: 0.50, num: '1', label: 'GK' },
        { nx: 0.20, ny: 0.28, num: 'CB', label: 'LCB' },
        { nx: 0.19, ny: 0.50, num: 'CB', label: 'CB' },
        { nx: 0.20, ny: 0.72, num: 'CB', label: 'RCB' },
        { nx: 0.34, ny: 0.10, num: 'WB', label: 'LWB' },
        { nx: 0.31, ny: 0.50, num: '6', label: 'DM' },
        { nx: 0.36, ny: 0.34, num: '8', label: 'CM' },
        { nx: 0.36, ny: 0.66, num: '10', label: 'CM' },
        { nx: 0.34, ny: 0.90, num: 'WB', label: 'RWB' },
        { nx: 0.47, ny: 0.38, num: '9', label: 'ST' },
        { nx: 0.47, ny: 0.62, num: '11', label: 'ST' }
    ],
    '4-2-3-1': [
        { nx: 0.06, ny: 0.50, num: '1', label: 'GK' },
        { nx: 0.22, ny: 0.15, num: '3', label: 'LB' },
        { nx: 0.20, ny: 0.38, num: '4', label: 'CB' },
        { nx: 0.20, ny: 0.62, num: '5', label: 'CB' },
        { nx: 0.22, ny: 0.85, num: '2', label: 'RB' },
        { nx: 0.32, ny: 0.38, num: '6', label: 'Pivot' },
        { nx: 0.32, ny: 0.62, num: '8', label: 'Pivot' },
        { nx: 0.41, ny: 0.18, num: '11', label: 'LW' },
        { nx: 0.42, ny: 0.50, num: '10', label: 'CAM' },
        { nx: 0.41, ny: 0.82, num: '7', label: 'RW' },
        { nx: 0.48, ny: 0.50, num: '9', label: 'ST' }
    ],
    '4-4-2': [
        { nx: 0.06, ny: 0.50, num: '1', label: 'GK' },
        { nx: 0.22, ny: 0.15, num: '3', label: 'LB' },
        { nx: 0.20, ny: 0.38, num: '4', label: 'CB' },
        { nx: 0.20, ny: 0.62, num: '5', label: 'CB' },
        { nx: 0.22, ny: 0.85, num: '2', label: 'RB' },
        { nx: 0.35, ny: 0.16, num: '11', label: 'LM' },
        { nx: 0.34, ny: 0.40, num: '6', label: 'CM' },
        { nx: 0.34, ny: 0.60, num: '8', label: 'CM' },
        { nx: 0.35, ny: 0.84, num: '7', label: 'RM' },
        { nx: 0.47, ny: 0.38, num: '9', label: 'ST' },
        { nx: 0.47, ny: 0.62, num: '10', label: 'ST' }
    ]
};

const toolHints = {
    select: 'اسحب اللاعبين لتحريكهم بحرية. انقر مرتين (Double Click) على أي لاعب لتعديل رقمه أو اسمه.',
    arrow: 'اضغط واسحب على الملعب لرسم سهم حركة مستقيم.',
    curved: 'اضغط واسحب لرسم سهم حركة مقوس (Curved Run) للضغط القوسي وغلق زوايا التمرير.',
    pass: 'اضغط واسحب لرسم خط تمرير متقطع بين اللاعبين.',
    polygon: 'انقر في عدة نقاط لتحديد زوايا منطقة، ثم اضغط "إغلاق وتظليل".',
    ruler: 'اضغط واسحب بين خطين أو لاعبين لقياس المسافة بالمتر (105×68م).',
    connect: 'اضغط واسحب من لاعب إلى آخر لربطهم بخط تكتيكي.',
    text: 'انقر في أي مكان على الملعب لكتابة ملاحظة تكتيكية.'
};

function initDefaultPieces() {
    pieces = [];
    formationTemplates['5-4-1'].forEach((p, idx) => {
        pieces.push({ id: 'red_' + idx, type: 'red', nx: p.nx, ny: p.ny, number: p.num, label: p.label });
    });
    formationTemplates['4-3-3'].forEach((p, idx) => {
        pieces.push({ id: 'blue_' + idx, type: 'blue', nx: 1 - p.nx, ny: p.ny, number: p.num, label: p.label });
    });
    pieces.push({ id: 'ball_1', type: 'ball', nx: 0.50, ny: 0.50, number: '', label: '' });
    updateTeamBanner();
}

function updateTeamBanner() {
    document.getElementById('display-red-name').textContent = redTeamMeta.name || 'الفريق الأحمر';
    document.getElementById('display-red-form').textContent = redTeamMeta.formation;
    document.getElementById('display-blue-name').textContent = blueTeamMeta.name || 'الفريق الأزرق';
    document.getElementById('display-blue-form').textContent = blueTeamMeta.formation;
}

function openLineupModal() {
    document.getElementById('input-red-team-name').value = redTeamMeta.name;
    document.getElementById('select-red-formation').value = redTeamMeta.formation;
    document.getElementById('input-blue-team-name').value = blueTeamMeta.name;
    document.getElementById('select-blue-formation').value = blueTeamMeta.formation;
    populateLineupInputs('red', redTeamMeta.formation, true);
    populateLineupInputs('blue', blueTeamMeta.formation, true);
    document.getElementById('lineup-modal').classList.remove('hidden');
}

function closeLineupModal() { document.getElementById('lineup-modal').classList.add('hidden'); }

function populateLineupInputs(team, formation, keepExisting = false) {
    const containerEl = document.getElementById(team + '-players-list');
    const template = formationTemplates[formation] || formationTemplates['4-3-3'];
    const existingPlayers = pieces.filter(p => p.type === team);
    containerEl.innerHTML = '';
    template.forEach((slot, idx) => {
        const current = keepExisting && existingPlayers[idx] ? existingPlayers[idx] : null;
        const numVal = current ? current.number : slot.num;
        const labelVal = current ? current.label : slot.label;
        const row = document.createElement('div');
        row.className = 'flex items-center gap-1.5';
        row.innerHTML = '<span class="text-[10px] font-en text-slate-500 w-5 text-center">' + (idx + 1) + '</span>' +
            '<input type="text" data-team="' + team + '" data-idx="' + idx + '" data-field="num" value="' + numVal + '" maxlength="4" class="w-14 bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs text-center font-en font-bold text-white focus:outline-none focus:border-blue-500" placeholder="رقم">' +
            '<input type="text" data-team="' + team + '" data-idx="' + idx + '" data-field="label" value="' + labelVal + '" maxlength="18" class="flex-1 bg-slate-950 border border-slate-700 rounded px-2.5 py-1 text-xs text-white focus:outline-none focus:border-blue-500" placeholder="اسم اللاعب أو المركز...">';
        containerEl.appendChild(row);
    });
}

function applyBothTeamsLineups() {
    saveHistory();
    const redName = document.getElementById('input-red-team-name').value.trim() || 'الفريق الأحمر';
    const redForm = document.getElementById('select-red-formation').value;
    const blueName = document.getElementById('input-blue-team-name').value.trim() || 'الفريق الأزرق';
    const blueForm = document.getElementById('select-blue-formation').value;

    redTeamMeta = { name: redName, formation: redForm };
    blueTeamMeta = { name: blueName, formation: blueForm };
    pieces = pieces.filter(p => p.type !== 'red' && p.type !== 'blue');

    formationTemplates[redForm].forEach((slot, idx) => {
        const numInput = document.querySelector('input[data-team="red"][data-idx="' + idx + '"][data-field="num"]');
        const lblInput = document.querySelector('input[data-team="red"][data-idx="' + idx + '"][data-field="label"]');
        const posX = pitchMode === 'half' ? Math.min(0.48, slot.nx * 0.95) : slot.nx;
        pieces.push({ id: 'red_' + idx, type: 'red', nx: posX, ny: slot.ny, number: numInput ? numInput.value.trim() : slot.num, label: lblInput ? lblInput.value.trim() : slot.label });
    });

    formationTemplates[blueForm].forEach((slot, idx) => {
        const numInput = document.querySelector('input[data-team="blue"][data-idx="' + idx + '"][data-field="num"]');
        const lblInput = document.querySelector('input[data-team="blue"][data-idx="' + idx + '"][data-field="label"]');
        const posX = pitchMode === 'half' ? Math.max(0.52, 1 - slot.nx * 0.95) : (1 - slot.nx);
        pieces.push({ id: 'blue_' + idx, type:
