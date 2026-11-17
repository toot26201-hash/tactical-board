import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة لتعمل بملء العرض وبتصميم داكن احترافي
st.set_page_config(
    page_title="ProTactics - لوحة التحليل والرسم التكتيكي",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إخفاء الهوامش الافتراضية لـ Streamlit لإعطاء مساحة كاملة للوحة التكتيكية
st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100% !important;
        }
        header[data-testid="stHeader"] {
            display: none;
        }
        footer {
            display: none;
        }
        iframe {
            border-radius: 12px;
            border: 1px solid #1e293b;
        }
    </style>
""", unsafe_allow_html=True)

# كود HTML/JS الكامل للوحة الرسم التكتيكي التفاعلية
tactical_board_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ProTactics - لوحة التحليل والرسم التكتيكي</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Cairo', 'Inter', sans-serif;
            background-color: #0b0f19;
            color: #e2e8f0;
            overflow: hidden;
            user-select: none;
            -webkit-user-select: none;
        }
        .font-en { font-family: 'Inter', sans-serif; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        .tool-btn.active {
            background-color: #2563eb;
            color: #ffffff;
            border-color: #60a5fa;
            box-shadow: 0 0 12px rgba(37, 99, 235, 0.45);
        }
        canvas { touch-action: none; display: block; }
    </style>
</head>
<body class="h-screen flex flex-col bg-[#0b0f19] text-slate-200">

    <!-- Header / Top Bar -->
    <header class="bg-[#111827] border-b border-slate-800 px-3 py-2 flex flex-wrap items-center justify-between gap-2 z-20 shadow-lg">
        <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center shadow-md shadow-emerald-900/40">
                <i class="fa-solid fa-chess-board text-white text-lg"></i>
            </div>
            <div>
                <h1 class="text-base md:text-lg font-bold tracking-tight text-white leading-tight">
                    ProTactics <span class="text-xs font-normal text-emerald-400 bg-emerald-950/80 border border-emerald-800/60 px-2 py-0.5 rounded-full mr-1">Pro Edition</span>
                </h1>
                <p class="text-[11px] text-slate-400 hidden sm:block">لوحة التحليل والرسم التكتيكي الاحترافية</p>
            </div>
        </div>

        <div class="flex flex-wrap items-center gap-2">
            <!-- زر إدارة تشكيلة وأسماء الفريقين -->
            <button onclick="openLineupModal()" class="flex items-center gap-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white border border-blue-400/40 text-xs px-3 py-1.5 rounded-lg shadow-md shadow-blue-950/50 transition font-bold">
                <i class="fa-solid fa-users-gear"></i>
                <span>تشكيلة وأسماء الفريقين</span>
            </button>

            <div class="flex items-center bg-slate-900 p-1 rounded-lg border border-slate-800">
                <button onclick="setPitchMode('full')" id="btn-pitch-full" class="pitch-mode-btn active bg-slate-700 text-white text-xs px-2.5 py-1.5 rounded-md font-semibold transition">
                    ملعب كامل <span class="font-en text-[10px] opacity-75">(Full)</span>
                </button>
                <button onclick="setPitchMode('half')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 hover:text-white text-xs px-2.5 py-1.5 rounded-md font-semibold transition">
                    نصف ملعب <span class="font-en text-[10px] opacity-75">(Half)</span>
                </button>
            </div>

            <button onclick="toggleZones()" id="btn-toggle-zones" class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs px-3 py-1.5 rounded-lg transition font-semibold">
                <i class="fa-solid fa-table-columns text-amber-400"></i>
                <span>5-Zones & Half-spaces</span>
            </button>

            <button onclick="togglePitchTheme()" id="btn-pitch-theme" class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs px-3 py-1.5 rounded-lg transition font-semibold">
                <i class="fa-solid fa-palette text-emerald-400"></i>
                <span id="theme-label">عشب داكن</span>
            </button>
        </div>

        <div class="flex items-center gap-1.5">
            <button onclick="undoAction()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs px-2.5 py-1.5 rounded-lg transition flex items-center gap-1">
                <i class="fa-solid fa-rotate-left"></i>
                <span class="hidden lg:inline">تراجع</span>
            </button>
            <button onclick="clearDrawings()" class="bg-slate-800 hover:bg-amber-950/60 text-amber-300 border border-slate-700 hover:border-amber-700 text-xs px-2.5 py-1.5 rounded-lg transition flex items-center gap-1">
                <i class="fa-solid fa-eraser"></i>
                <span class="hidden lg:inline">مسح الرسم</span>
            </button>
            <button onclick="resetBoard()" class="bg-slate-800 hover:bg-red-950/60 text-red-400 border border-slate-700 hover:border-red-800 text-xs px-2.5 py-1.5 rounded-lg transition flex items-center gap-1">
                <i class="fa-solid fa-trash-can"></i>
                <span class="hidden lg:inline">إعادة ضبط</span>
            </button>
            <button onclick="exportPNG()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-3 py-1.5 rounded-lg shadow-md shadow-emerald-900/40 transition flex items-center gap-1.5">
                <i class="fa-solid fa-camera"></i>
                <span>تصدير PNG</span>
            </button>
        </div>
    </header>

    <!-- Main Workspace -->
    <div class="flex-1 flex flex-col md:flex-row overflow-hidden relative">
        <!-- Sidebar -->
        <aside class="bg-[#111827] border-b md:border-b-0 md:border-l border-slate-800 p-2 flex md:flex-col items-center justify-between md:justify-start gap-2 overflow-x-auto md:overflow-y-auto md:w-56 shrink-0 z-10">
            <div class="w-full hidden md:block text-[11px] font-bold text-slate-400 uppercase tracking-wider px-1 mb-0.5">
                أدوات التحليل والرسم
            </div>

            <div class="flex md:grid md:grid-cols-2 gap-1.5 w-auto md:w-full shrink-0">
                <button onclick="setTool('select')" id="tool-select" class="tool-btn active flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-arrow-pointer text-sm mb-1"></i>
                    <span class="text-[11px] font-semibold">تحريك</span>
                    <span class="text-[9px] font-en opacity-70">Select</span>
                </button>
                <button onclick="setTool('arrow')" id="tool-arrow" class="tool-btn flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-arrow-up-long text-sm mb-1 rotate-45"></i>
                    <span class="text-[11px] font-semibold">سهم حركة</span>
                    <span class="text-[9px] font-en opacity-70">Run</span>
                </button>
                <button onclick="setTool('curved')" id="tool-curved" class="tool-btn flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-share text-sm mb-1"></i>
                    <span class="text-[11px] font-semibold">ضغط قوسي</span>
                    <span class="text-[9px] font-en opacity-70">Curved</span>
                </button>
                <button onclick="setTool('pass')" id="tool-pass" class="tool-btn flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-ellipsis text-sm mb-1"></i>
                    <span class="text-[11px] font-semibold">تمرير</span>
                    <span class="text-[9px] font-en opacity-70">Pass</span>
                </button>
                <button onclick="setTool('polygon')" id="tool-polygon" class="tool-btn flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-draw-polygon text-sm mb-1"></i>
                    <span class="text-[11px] font-semibold">تظليل مساحة</span>
                    <span class="text-[9px] font-en opacity-70">Zone</span>
                </button>
                <button onclick="setTool('ruler')" id="tool-ruler" class="tool-btn flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-ruler-horizontal text-sm mb-1"></i>
                    <span class="text-[11px] font-semibold">قياس متر</span>
                    <span class="text-[9px] font-en opacity-70">Distance</span>
                </button>
                <button onclick="setTool('connect')" id="tool-connect" class="tool-btn flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-circle-nodes text-sm mb-1"></i>
                    <span class="text-[11px] font-semibold">ربط خطوط</span>
                    <span class="text-[9px] font-en opacity-70">Connect</span>
                </button>
                <button onclick="setTool('text')" id="tool-text" class="tool-btn flex flex-col items-center justify-center p-2 rounded-lg border border-slate-700/80 bg-slate-800/60 hover:bg-slate-800 text-slate-300 transition min-w-[68px]">
                    <i class="fa-solid fa-font text-sm mb-1"></i>
                    <span class="text-[11px] font-semibold">نص شرح</span>
                    <span class="text-[9px] font-en opacity-70">Text</span>
                </button>
            </div>

            <div class="hidden md:block w-full border-t border-slate-800 my-1"></div>

            <!-- Colors & Stroke -->
            <div class="flex md:flex-col items-center md:items-stretch gap-2 shrink-0">
                <div class="hidden md:block text-[11px] font-bold text-slate-400 px-1">لون الرسم وسمك الخط</div>
                <div class="flex items-center justify-around gap-1.5 bg-slate-900/90 p-1.5 rounded-lg border border-slate-800">
                    <button onclick="setColor('#facc15')" data-color="#facc15" class="color-btn w-6 h-6 rounded-full bg-yellow-400 ring-2 ring-white scale-110 transition"></button>
                    <button onclick="setColor('#ffffff')" data-color="#ffffff" class="color-btn w-6 h-6 rounded-full bg-white opacity-80 hover:opacity-100 transition"></button>
                    <button onclick="setColor('#ef4444')" data-color="#ef4444" class="color-btn w-6 h-6 rounded-full bg-red-500 opacity-80 hover:opacity-100 transition"></button>
                    <button onclick="setColor('#38bdf8')" data-color="#38bdf8" class="color-btn w-6 h-6 rounded-full bg-sky-400 opacity-80 hover:opacity-100 transition"></button>
                    <button onclick="setColor('#f97316')" data-color="#f97316" class="color-btn w-6 h-6 rounded-full bg-orange-500 opacity-80 hover:opacity-100 transition"></button>
                </div>
                <div class="hidden md:flex items-center justify-between gap-2 bg-slate-900/90 px-2.5 py-1.5 rounded-lg border border-slate-800">
                    <span class="text-[11px] text-slate-400">السمك:</span>
                    <input type="range" id="stroke-width" min="2" max="7" value="3" oninput="currentStrokeWidth = parseInt(this.value)" class="w-24 accent-blue-500 cursor-pointer">
                </div>
            </div>

            <div class="hidden md:block w-full border-t border-slate-800 my-1"></div>

            <!-- Add Elements -->
            <div class="hidden md:flex flex-col gap-1.5 w-full">
                <div class="text-[11px] font-bold text-slate-400 px-1">إضافة عناصر للملعب</div>
                <div class="grid grid-cols-2 gap-1.5">
                    <button onclick="addPiece('red')" class="flex items-center justify-center gap-1.5 bg-red-950/50 hover:bg-red-900/60 text-red-300 border border-red-800/60 py-1.5 px-2 rounded-lg text-xs font-semibold transition">
                        <span class="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
                        <span>+ لاعب أحمر</span>
                    </button>
                    <button onclick="addPiece('blue')" class="flex items-center justify-center gap-1.5 bg-sky-950/50 hover:bg-sky-900/60 text-sky-300 border border-sky-800/60 py-1.5 px-2 rounded-lg text-xs font-semibold transition">
                        <span class="w-3 h-3 rounded-full bg-sky-500 inline-block"></span>
                        <span>+ لاعب أزرق</span>
                    </button>
                    <button onclick="addPiece('ball')" class="flex items-center justify-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 py-1.5 px-2 rounded-lg text-xs font-semibold transition">
                        <i class="fa-solid fa-futbol text-white"></i>
                        <span>+ كرة</span>
                    </button>
                    <button onclick="addPiece('cone')" class="flex items-center justify-center gap-1.5 bg-amber-950/40 hover:bg-amber-900/50 text-amber-300 border border-amber-800/60 py-1.5 px-2 rounded-lg text-xs font-semibold transition">
                        <i class="fa-solid fa-triangle-exclamation text-orange-400"></i>
                        <span>+ قمع</span>
                    </button>
                </div>
            </div>

            <div id="tool-hint-box" class="hidden md:block mt-auto w-full bg-slate-900/90 border border-slate-800 rounded-lg p-2.5 text-[11px] text-slate-400 leading-relaxed">
                <div class="font-bold text-blue-400 mb-0.5"><i class="fa-solid fa-circle-info ml-1"></i> تلميح الاستخدام:</div>
                <span id="tool-hint-text">اسحب اللاعبين لتحريكهم. انقر مرتين (Double Click) على أي لاعب لتعديل رقمه أو اسمه.</span>
            </div>
        </aside>

        <!-- Canvas Area -->
        <main id="canvas-container" class="flex-1 relative bg-[#080c14] flex flex-col items-center justify-center p-2 sm:p-3 overflow-hidden">
            <!-- شريط عرض أسماء الفريقين وخططهما أعلى الملعب -->
            <div class="w-full max-w-4xl flex items-center justify-between bg-slate-900/90 border border-slate-800 rounded-lg px-4 py-1.5 mb-2 shadow-md">
                <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full bg-red-500 inline-block shadow shadow-red-500/50"></span>
                    <span id="display-red-name" class="text-xs sm:text-sm font-bold text-white">الفريق الأحمر</span>
                    <span id="display-red-form" class="text-[11px] font-en font-semibold bg-red-950/80 text-red-300 border border-red-800/60 px-2 py-0.5 rounded">5-4-1</span>
                </div>
                <span class="text-xs font-en font-bold text-slate-500">VS</span>
                <div class="flex items-center gap-2">
                    <span id="display-blue-form" class="text-[11px] font-en font-semibold bg-sky-950/80 text-sky-300 border border-sky-800/60 px-2 py-0.5 rounded">4-3-3</span>
                    <span id="display-blue-name" class="text-xs sm:text-sm font-bold text-white">الفريق الأزرق</span>
                    <span class="w-3 h-3 rounded-full bg-sky-500 inline-block shadow shadow-sky-500/50"></span>
                </div>
            </div>

            <canvas id="tactical-canvas" class="rounded-xl shadow-2xl border border-slate-800"></canvas>

            <div id="polygon-controls" class="hidden absolute bottom-6 left-1/2 -translate-x-1/2 bg-slate-900/95 border border-yellow-500/60 px-4 py-2 rounded-full shadow-2xl flex items-center gap-3 z-20">
                <span class="text-xs text-yellow-300 font-semibold"><i class="fa-solid fa-draw-polygon ml-1"></i> انقر لإضافة نقاط المساحة</span>
                <button onclick="finishPolygon()" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-3 py-1 rounded-full transition">إغلاق وتظليل</button>
                <button onclick="cancelPolygon()" class="bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs px-2.5 py-1 rounded-full transition">إلغاء</button>
            </div>

            <div id="toast-msg" class="pointer-events-none opacity-0 transition-opacity duration-300 absolute top-14 left-1/2 -translate-x-1/2 bg-slate-900/95 border border-slate-700 text-white text-xs font-semibold px-4 py-2 rounded-full shadow-xl z-30">
                تم الحفظ
            </div>
        </main>
    </div>

    <!-- Modal: Lineup & Teams Manager (إدارة تشكيلة وأسماء الفريقين) -->
    <div id="lineup-modal" class="hidden fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center z-50 p-3 sm:p-4">
        <div class="bg-[#111827] border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[92vh] flex flex-col shadow-2xl">
            <div class="flex items-center justify-between border-b border-slate-800 px-5 py-3.5 shrink-0">
                <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-users-gear text-blue-400"></i>
                    <span>إعداد تشكيلة وأسماء لاعبي الفريقين</span>
                </h3>
                <button onclick="closeLineupModal()" class="text-slate-400 hover:text-white"><i class="fa-solid fa-xmark text-xl"></i></button>
            </div>

            <div class="p-4 sm:p-5 overflow-y-auto grid grid-cols-1 md:grid-cols-2 gap-5">
                <!-- الفريق الأحمر -->
                <div class="bg-slate-900/80 border border-red-900/50 rounded-xl p-3.5">
                    <div class="flex items-center gap-2 mb-3 pb-2 border-b border-slate-800">
                        <span class="w-3.5 h-3.5 rounded-full bg-red-500"></span>
                        <span class="font-bold text-sm text-red-400">الفريق الأول (الأحمر - يسار)</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2 mb-3">
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">اسم الفريق:</label>
                            <input type="text" id="input-red-team-name" value="الفريق الأحمر" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-red-500">
                        </div>
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">الخطة التكتيكية:</label>
                            <select id="select-red-formation" onchange="populateLineupInputs('red', this.value)" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2 py-1.5 text-xs font-en text-white focus:outline-none focus:border-red-500">
                                <option value="5-4-1">5-4-1</option>
                                <option value="4-3-3">4-3-3</option>
                                <option value="3-5-2">3-5-2</option>
                                <option value="4-2-3-1">4-2-3-1</option>
                                <option value="4-4-2">4-4-2</option>
                            </select>
                        </div>
                    </div>
                    <div class="text-[11px] font-semibold text-slate-400 mb-1.5 flex justify-between px-1">
                        <span>المركز / الرقم</span>
                        <span>اسم اللاعب (يظهر أسفل الدائرة)</span>
                    </div>
                    <div id="red-players-list" class="space-y-1.5 max-h-64 overflow-y-auto pr-1"></div>
                </div>

                <!-- الفريق الأزرق -->
                <div class="bg-slate-900/80 border border-sky-900/50 rounded-xl p-3.5">
                    <div class="flex items-center gap-2 mb-3 pb-2 border-b border-slate-800">
                        <span class="w-3.5 h-3.5 rounded-full bg-sky-500"></span>
                        <span class="font-bold text-sm text-sky-400">الفريق الثاني (الأزرق - يمين)</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2 mb-3">
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">اسم الفريق:</label>
                            <input type="text" id="input-blue-team-name" value="الفريق الأزرق" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-sky-500">
                        </div>
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">الخطة التكتيكية:</label>
                            <select id="select-blue-formation" onchange="populateLineupInputs('blue', this.value)" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2 py-1.5 text-xs font-en text-white focus:outline-none focus:border-sky-500">
                                <option value="4-3-3">4-3-3</option>
                                <option value="4-2-3-1">4-2-3-1</option>
                                <option value="5-4-1">5-4-1</option>
                                <option value="3-5-2">3-5-2</option>
                                <option value="4-4-2">4-4-2</option>
                            </select>
                        </div>
                    </div>
                    <div class="text-[11px] font-semibold text-slate-400 mb-1.5 flex justify-between px-1">
                        <span>المركز / الرقم</span>
                        <span>اسم اللاعب (يظهر أسفل الدائرة)</span>
                    </div>
                    <div id="blue-players-list" class="space-y-1.5 max-h-64 overflow-y-auto pr-1"></div>
                </div>
            </div>

            <div class="flex items-center justify-end gap-2 px-5 py-3 border-t border-slate-800 shrink-0 bg-slate-900/50 rounded-b-2xl">
                <button onclick="closeLineupModal()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-4 py-2 rounded-lg transition">إلغاء</button>
                <button onclick="applyBothTeamsLineups()" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-5 py-2 rounded-lg shadow-lg shadow-emerald-950/50 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-check"></i>
                    <span>تطبيق التشكيلة والأسماء على الملعب</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Modal: Edit Single Player -->
    <div id="edit-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-[#111827] border border-slate-700 rounded-2xl w-full max-w-sm p-5 shadow-2xl">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-user-pen text-blue-400"></i>
                    <span>تعديل بيانات اللاعب</span>
                </h3>
                <button onclick="closeEditModal()" class="text-slate-400 hover:text-white"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <div class="space-y-3">
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">الرقم أو الرمز داخل الدائرة (مثل 4 أو CB):</label>
                    <input type="text" id="edit-number" maxlength="4" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white font-en font-bold focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">اسم اللاعب أو المركز أسفل الدائرة:</label>
                    <input type="text" id="edit-label" maxlength="18" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <span class="block text-[11px] text-slate-500 mb-1.5">اختصارات سريعة للمراكز:</span>
                    <div class="flex flex-wrap gap-1.5 font-en">
                        <button type="button" onclick="quickFillRole('GK', 'حارس')" class="text-[11px] bg-slate-800 hover:bg-slate-700 px-2 py-1 rounded text-slate-300">GK</button>
                        <button type="button" onclick="quickFillRole('CB', 'قلب دفاع')" class="text-[11px] bg-slate-800 hover:bg-slate-700 px-2 py-1 rounded text-slate-300">CB</button>
                        <button type="button" onclick="quickFillRole('WB', 'جناح خلفي')" class="text-[11px] bg-slate-800 hover:bg-slate-700 px-2 py-1 rounded text-slate-300">WB</button>
                        <button type="button" onclick="quickFillRole('DM', 'ارتكاز')" class="text-[11px] bg-slate-800 hover:bg-slate-700 px-2 py-1 rounded text-slate-300">DM</button>
                        <button type="button" onclick="quickFillRole('CM', 'وسط')" class="text-[11px] bg-slate-800 hover:bg-slate-700 px-2 py-1 rounded text-slate-300">CM</button>
                        <button type="button" onclick="quickFillRole('IF', 'مساحة نصفية')" class="text-[11px] bg-slate-800 hover:bg-slate-700 px-2 py-1 rounded text-slate-300">IF</button>
                        <button type="button" onclick="quickFillRole('FWD', 'مهاجم')" class="text-[11px] bg-slate-800 hover:bg-slate-700 px-2 py-1 rounded text-slate-300">FWD</button>
                    </div>
                </div>
            </div>
            <div class="flex items-center justify-between gap-2 mt-5 pt-3 border-t border-slate-800">
                <button onclick="deleteSelectedPiece()" class="bg-red-950/70 hover:bg-red-900 text-red-300 border border-red-800/70 text-xs font-semibold px-3 py-2 rounded-lg transition">حذف العنصر</button>
                <div class="flex items-center gap-2">
                    <button onclick="closeEditModal()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-3 py-2 rounded-lg">إلغاء</button>
                    <button onclick="saveEditModal()" class="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-lg">حفظ التعديل</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal: Add Text -->
    <div id="text-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-[#111827] border border-slate-700 rounded-2xl w-full max-w-sm p-5 shadow-2xl">
            <h3 class="text-base font-bold text-white mb-3 flex items-center gap-2">
                <i class="fa-solid fa-font text-yellow-400"></i>
                <span>إضافة ملاحظة تكتيكية على الملعب</span>
            </h3>
            <input type="text" id="annotation-input" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 mb-4" placeholder="اكتب النص التوضيحي هنا...">
            <div class="flex justify-end gap-2">
                <button onclick="closeTextModal()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-3 py-2 rounded-lg">إلغاء</button>
                <button onclick="confirmTextAnnotation()" class="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-lg">إضافة للملعب</button>
            </div>
        </div>
    </div>

    <script>
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
            const redTemplate = formationTemplates['5-4-1'];
            redTemplate.forEach((p, idx) => {
                pieces.push({ id: 'red_' + idx, type: 'red', nx: p.nx, ny: p.ny, number: p.num, label: p.label });
            });

            const blueTemplate = formationTemplates['4-3-3'];
            blueTemplate.forEach((p, idx) => {
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

        // إدارة نافذة تشكيلة وأسماء الفريقين
        function openLineupModal() {
            document.getElementById('input-red-team-name').value = redTeamMeta.name;
            document.getElementById('select-red-formation').value = redTeamMeta.formation;
            document.getElementById('input-blue-team-name').value = blueTeamMeta.name;
            document.getElementById('select-blue-formation').value = blueTeamMeta.formation;

            populateLineupInputs('red', redTeamMeta.formation, true);
            populateLineupInputs('blue', blueTeamMeta.formation, true);
            document.getElementById('lineup-modal').classList.remove('hidden');
        }

        function closeLineupModal() {
            document.getElementById('lineup-modal').classList.add('hidden');
        }

        function populateLineupInputs(team, formation, keepExisting = false) {
            const containerEl = document.getElementById(`${team}-players-list`);
            const template = formationTemplates[formation] || formationTemplates['4-3-3'];
            const existingPlayers = pieces.filter(p => p.type === team);

            containerEl.innerHTML = '';
            template.forEach((slot, idx) => {
                const current = keepExisting && existingPlayers[idx] ? existingPlayers[idx] : null;
                const numVal = current ? current.number : slot.num;
                const labelVal = current ? current.label : slot.label;

                const row = document.createElement('div');
                row.className = 'flex items-center gap-1.5';
                row.innerHTML = `
                    <span class="text-[10px] font-en text-slate-500 w-5 text-center">${idx + 1}</span>
                    <input type="text" data-team="${team}" data-idx="${idx}" data-field="num" value="${numVal}" maxlength="4"
                        class="w-14 bg-slate-950 border border-slate-700 rounded px-2 py-1 text-xs text-center font-en font-bold text-white focus:outline-none focus:border-blue-500" placeholder="رقم">
                    <input type="text" data-team="${team}" data-idx="${idx}" data-field="label" value="${labelVal}" maxlength="18"
                        class="flex-1 bg-slate-950 border border-slate-700 rounded px-2.5 py-1 text-xs text-white focus:outline-none focus:border-blue-500" placeholder="اسم اللاعب أو المركز...">
                `;
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

            // الاحتفاظ بالكرات والأقماع فقط وإعادة بناء لاعبي الفريقين
            pieces = pieces.filter(p => p.type !== 'red' && p.type !== 'blue');

            const redTemplate = formationTemplates[redForm];
            redTemplate.forEach((slot, idx) => {
                const numInput = document.querySelector(`input[data-team="red"][data-idx="${idx}"][data-field="num"]`);
                const lblInput = document.querySelector(`input[data-team="red"][data-idx="${idx}"][data-field="label"]`);
                const posX = pitchMode === 'half' ? Math.min(0.48, slot.nx * 0.95) : slot.nx;
                pieces.push({
                    id: 'red_' + idx,
                    type: 'red',
                    nx: posX,
                    ny: slot.ny,
                    number: numInput ? numInput.value.trim() : slot.num,
                    label: lblInput ? lblInput.value.trim() : slot.label
                });
            });

            const blueTemplate = formationTemplates[blueForm];
            blueTemplate.forEach((slot, idx) => {
                const numInput = document.querySelector(`input[data-team="blue"][data-idx="${idx}"][data-field="num"]`);
                const lblInput = document.querySelector(`input[data-team="blue"][data-idx="${idx}"][data-field="label"]`);
                const posX = pitchMode === 'half' ? Math.max(0.52, 1 - slot.nx * 0.95) : (1 - slot.nx);
                pieces.push({
                    id: 'blue_' + idx,
                    type: 'blue',
                    nx: posX,
                    ny: slot.ny,
                    number: numInput ? numInput.value.trim() : slot.num,
                    label: lblInput ? lblInput.value.trim() : slot.label
                });
            });

            updateTeamBanner();
            closeLineupModal();
            render();
            showToast('تم تحديث تشكيلة وأسماء الفريقين بنجاح');
        }

        function resizeCanvas() {
            const rect = container.getBoundingClientRect();
            const padX = window.innerWidth < 640 ? 12 : 24;
            const padY = window.innerWidth < 640 ? 44 : 52;
            const availW = Math.max(200, rect.width - padX * 2);
            const availH = Math.max(150, rect.height - padY);
            const targetRatio = pitchMode === 'full' ? (105 / 68) : (68 / 58);

            let finalW = availW;
            let finalH = availW / targetRatio;
            if (finalH > availH) {
                finalH = availH;
                finalW = availH * targetRatio;
            }
            finalW = Math.max(100, finalW);
            finalH = Math.max(100, finalH);

            const dpr = window.devicePixelRatio || 1;
            canvas.width = finalW * dpr;
            canvas.height = finalH * dpr;
            canvas.style.width = `${finalW}px`;
            canvas.style.height = `${finalH}px`;
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

            const margin = Math.max(10, Math.min(finalW, finalH) * 0.025);
            pitchRect = {
                x: margin,
                y: margin,
                w: Math.max(50, finalW - margin * 2),
                h: Math.max(50, finalH - margin * 2),
                canvasW: finalW,
                canvasH: finalH
            };
            render();
        }

        function normToCanvas(nx, ny) {
            return { x: pitchRect.x + nx * pitchRect.w, y: pitchRect.y + ny * pitchRect.h };
        }

        function canvasToNorm(cx, cy) {
            return {
                nx: Math.max(0, Math.min(1, (cx - pitchRect.x) / pitchRect.w)),
                ny: Math.max(0, Math.min(1, (cy - pitchRect.y) / pitchRect.h))
            };
        }

        function calculateMeters(p1, p2) {
            const lengthMeters = pitchMode === 'full' ? 105 : 52.5;
            const widthMeters = 68;
            const dx = (p2.nx - p1.nx) * lengthMeters;
            const dy = (p2.ny - p1.ny) * widthMeters;
            return Math.sqrt(dx * dx + dy * dy).toFixed(1);
        }

        function drawPitch() {
            const { x, y, w, h, canvasW, canvasH } = pitchRect;
            if (w <= 0 || h <= 0) return;

            ctx.fillStyle = pitchTheme === 'green' ? '#0d2618' : '#0f172a';
            ctx.fillRect(0, 0, canvasW, canvasH);

            if (pitchTheme === 'green') {
                ctx.fillStyle = '#133824';
                ctx.fillRect(x, y, w, h);
                const stripes = pitchMode === 'full' ? 14 : 8;
                const stripeW = w / stripes;
                for (let i = 0; i < stripes; i++) {
                    if (i % 2 === 0) {
                        ctx.fillStyle = 'rgba(255, 255, 255, 0.025)';
                        ctx.fillRect(x + i * stripeW, y, stripeW, h);
                    }
                }
            } else {
                ctx.fillStyle = '#151e32';
                ctx.fillRect(x, y, w, h);
            }

            if (showZones) drawTacticalZones(x, y, w, h);

            ctx.strokeStyle = pitchTheme === 'green' ? 'rgba(255, 255, 255, 0.65)' : 'rgba(148, 163, 184, 0.55)';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, w, h);

            if (pitchMode === 'full') {
                ctx.beginPath();
                ctx.moveTo(x + w / 2, y);
                ctx.lineTo(x + w / 2, y + h);
                ctx.stroke();

                const centerR = Math.max(1, (9.15 / 105) * w);
                ctx.beginPath();
                ctx.arc(x + w / 2, y + h / 2, centerR, 0, Math.PI * 2);
                ctx.stroke();

                ctx.fillStyle = ctx.strokeStyle;
                ctx.beginPath();
                ctx.arc(x + w / 2, y + h / 2, 3, 0, Math.PI * 2);
                ctx.fill();

                const penW = (16.5 / 105) * w;
                const penH = (40.32 / 68) * h;
                const penY = y + (h - penH) / 2;
                ctx.strokeRect(x, penY, penW, penH);
                ctx.strokeRect(x + w - penW, penY, penW, penH);

                const goalW = (5.5 / 105) * w;
                const goalH = (18.32 / 68) * h;
                const goalY = y + (h - goalH) / 2;
                ctx.strokeRect(x, goalY, goalW, goalH);
                ctx.strokeRect(x + w - goalW, goalY, goalW, goalH);

                const spotDist = (11 / 105) * w;
                ctx.beginPath();
                ctx.arc(x + spotDist, y + h / 2, 2.5, 0, Math.PI * 2);
                ctx.arc(x + w - spotDist, y + h / 2, 2.5, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(x + spotDist, y + h / 2, centerR, -0.92, 0.92);
                ctx.stroke();
                ctx.beginPath();
                ctx.arc(x + w - spotDist, y + h / 2, centerR, Math.PI - 0.92, Math.PI + 0.92);
                ctx.stroke();

                const netDepth = 6;
                const netH = (7.32 / 68) * h;
                ctx.strokeRect(x - netDepth, y + (h - netH) / 2, netDepth, netH);
                ctx.strokeRect(x + w, y + (h - netH) / 2, netDepth, netH);
            } else {
                const halfLen = 52.5;
                const penW = (16.5 / halfLen) * w;
                const penH = (40.32 / 68) * h;
                const penY = y + (h - penH) / 2;
                ctx.strokeRect(x, penY, penW, penH);

                const goalW = (5.5 / halfLen) * w;
                const goalH = (18.32 / 68) * h;
                const goalY = y + (h - goalH) / 2;
                ctx.strokeRect(x, goalY, goalW, goalH);

                const spotDist = (11 / halfLen) * w;
                const centerR = Math.max(1, (9.15 / halfLen) * w);
                ctx.fillStyle = ctx.strokeStyle;
                ctx.beginPath();
                ctx.arc(x + spotDist, y + h / 2, 3, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(x + spotDist, y + h / 2, centerR, -0.92, 0.92);
                ctx.stroke();
                ctx.beginPath();
                ctx.arc(x + w, y + h / 2, centerR, Math.PI * 0.5, Math.PI * 1.5);
                ctx.stroke();

                const netDepth = 7;
                const netH = (7.32 / 68) * h;
                ctx.strokeRect(x - netDepth, y + (h - netH) / 2, netDepth, netH);
            }
        }

        function drawTacticalZones(x, y, w, h) {
            const penH = (40.32 / 68) * h;
            const goalH = (18.32 / 68) * h;
            const topWideH = (h - penH) / 2;
            const halfSpaceH = (penH - goalH) / 2;

            const y1 = y + topWideH;
            const y2 = y1 + halfSpaceH;
            const y3 = y2 + goalH;
            const y4 = y3 + halfSpaceH;

            ctx.fillStyle = 'rgba(250, 204, 21, 0.08)';
            ctx.fillRect(x, y1, w, halfSpaceH);
            ctx.fillRect(x, y3, w, halfSpaceH);

            ctx.save();
            ctx.strokeStyle = 'rgba(250, 204, 21, 0.42)';
            ctx.setLineDash([6, 6]);
            ctx.lineWidth = 1.2;
            [y1, y2, y3, y4].forEach(lineY => {
                ctx.beginPath();
                ctx.moveTo(x, lineY);
                ctx.lineTo(x + w, lineY);
                ctx.stroke();
            });
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.35)';
            [x + w / 3, x + (2 * w) / 3].forEach(lineX => {
                ctx.beginPath();
                ctx.moveTo(lineX, y);
                ctx.lineTo(lineX, y + h);
                ctx.stroke();
            });
            ctx.restore();

            ctx.save();
            ctx.font = '600 10px Inter, sans-serif';
            ctx.fillStyle = 'rgba(250, 204, 21, 0.75)';
            ctx.textAlign = 'right';
            ctx.fillText('Wide Channel', x + w - 8, y + topWideH / 2 + 3);
            ctx.fillText('Half-Space', x + w - 8, y1 + halfSpaceH / 2 + 3);
            ctx.fillText('Central Zone', x + w - 8, y2 + goalH / 2 + 3);
            ctx.fillText('Half-Space', x + w - 8, y3 + halfSpaceH / 2 + 3);
            ctx.fillText('Wide Channel', x + w - 8, y4 + topWideH / 2 + 3);
            ctx.restore();
        }

        function drawDrawings() {
            drawings.forEach(item => renderDrawingItem(item));
            if (currentDraft) renderDrawingItem(currentDraft, true);
            if (polygonPoints.length > 0) {
                ctx.save();
                ctx.strokeStyle = currentColor;
                ctx.fillStyle = hexToRgba(currentColor, 0.22);
                ctx.lineWidth = currentStrokeWidth;
                ctx.beginPath();
                polygonPoints.forEach((pt, idx) => {
                    const c = normToCanvas(pt.nx, pt.ny);
                    if (idx === 0) ctx.moveTo(c.x, c.y);
                    else ctx.lineTo(c.x, c.y);
                });
                ctx.stroke();
                polygonPoints.forEach(pt => {
                    const c = normToCanvas(pt.nx, pt.ny);
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath();
                    ctx.arc(c.x, c.y, 4.5, 0, Math.PI * 2);
                    ctx.fill();
                });
                ctx.restore();
            }
        }

        function renderDrawingItem(item) {
            ctx.save();
            ctx.strokeStyle = item.color;
            ctx.fillStyle = item.color;
            ctx.lineWidth = item.width || 3;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';

            if (item.type === 'arrow') {
                const p1 = normToCanvas(item.points[0].nx, item.points[0].ny);
                const p2 = normToCanvas(item.points[1].nx, item.points[1].ny);
                drawArrowLine(p1.x, p1.y, p2.x, p2.y, item.width, false);
            } else if (item.type === 'pass') {
                const p1 = normToCanvas(item.points[0].nx, item.points[0].ny);
                const p2 = normToCanvas(item.points[1].nx, item.points[1].ny);
                drawArrowLine(p1.x, p1.y, p2.x, p2.y, item.width, true);
            } else if (item.type === 'curved') {
                const p1 = normToCanvas(item.points[0].nx, item.points[0].ny);
                const p2 = normToCanvas(item.points[1].nx, item.points[1].ny);
                drawCurvedArrow(p1.x, p1.y, p2.x, p2.y, item.width);
            } else if (item.type === 'connect') {
                const p1 = normToCanvas(item.points[0].nx, item.points[0].ny);
                const p2 = normToCanvas(item.points[1].nx, item.points[1].ny);
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            } else if (item.type === 'polygon') {
                ctx.beginPath();
                item.points.forEach((pt, idx) => {
                    const c = normToCanvas(pt.nx, pt.ny);
                    if (idx === 0) ctx.moveTo(c.x, c.y);
                    else ctx.lineTo(c.x, c.y);
                });
                ctx.closePath();
                ctx.fillStyle = hexToRgba(item.color, 0.24);
                ctx.fill();
                ctx.stroke();
            } else if (item.type === 'ruler') {
                const p1 = normToCanvas(item.points[0].nx, item.points[0].ny);
                const p2 = normToCanvas(item.points[1].nx, item.points[1].ny);
                const meters = calculateMeters(item.points[0], item.points[1]);
                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
                [p1, p2].forEach(pt => {
                    ctx.beginPath();
                    ctx.arc(pt.x, pt.y, 4, 0, Math.PI * 2);
                    ctx.fill();
                });
                const midX = (p1.x + p2.x) / 2;
                const midY = (p1.y + p2.y) / 2;
                const label = `${meters} m`;
                ctx.font = 'bold 12px Inter, Cairo, sans-serif';
                const textW = ctx.measureText(label).width + 14;
                ctx.fillStyle = '#0f172a';
                ctx.strokeStyle = item.color;
                ctx.lineWidth = 1.5;
                roundRect(ctx, midX - textW / 2, midY - 12, textW, 24, 6, true, true);
                ctx.fillStyle = item.color;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(label, midX, midY);
            } else if (item.type === 'text') {
                const p = normToCanvas(item.points[0].nx, item.points[0].ny);
                ctx.font = 'bold 13px Cairo, Inter, sans-serif';
                const textW = ctx.measureText(item.text).width + 18;
                ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
                ctx.strokeStyle = item.color;
                ctx.lineWidth = 1.5;
                roundRect(ctx, p.x - textW / 2, p.y - 14, textW, 28, 7, true, true);
                ctx.fillStyle = item.color;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(item.text, p.x, p.y);
            }
            ctx.restore();
        }

        function drawArrowLine(x1, y1, x2, y2, width, dashed) {
            const headLen = 11 + width * 1.5;
            const angle = Math.atan2(y2 - y1, x2 - x1);
            ctx.save();
            if (dashed) ctx.setLineDash([8, 6]);
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2 - Math.cos(angle) * (headLen * 0.6), y2 - Math.sin(angle) * (headLen * 0.6));
            ctx.stroke();
            ctx.restore();

            ctx.beginPath();
            ctx.moveTo(x2, y2);
            ctx.lineTo(x2 - headLen * Math.cos(angle - Math.PI / 6), y2 - headLen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(x2 - headLen * Math.cos(angle + Math.PI / 6), y2 - headLen * Math.sin(angle + Math.PI / 6));
            ctx.closePath();
            ctx.fill();
        }

        function drawCurvedArrow(x1, y1, x2, y2, width) {
            const dx = x2 - x1;
            const dy = y2 - y1;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 5) return;
            const midX = (x1 + x2) / 2;
            const midY = (y1 + y2) / 2;
            const cpX = midX + (-dy / dist) * (dist * 0.28);
            const cpY = midY + (dx / dist) * (dist * 0.28);

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.quadraticCurveTo(cpX, cpY, x2, y2);
            ctx.stroke();

            const angle = Math.atan2(y2 - cpY, x2 - cpX);
            const headLen = 11 + width * 1.5;
            ctx.beginPath();
            ctx.moveTo(x2, y2);
            ctx.lineTo(x2 - headLen * Math.cos(angle - Math.PI / 6), y2 - headLen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(x2 - headLen * Math.cos(angle + Math.PI / 6), y2 - headLen * Math.sin(angle + Math.PI / 6));
            ctx.closePath();
            ctx.fill();
        }

        function drawPieces() {
            const radius = Math.max(13, Math.min(18, pitchRect.w * 0.021));
            pieces.forEach(p => {
                const pos = normToCanvas(p.nx, p.ny);
                ctx.save();
                if (p.type === 'red' || p.type === 'blue') {
                    ctx.shadowColor = 'rgba(0, 0, 0, 0.55)';
                    ctx.shadowBlur = 6;
                    ctx.shadowOffsetY = 3;
                    const grad = ctx.createRadialGradient(pos.x - 4, pos.y - 4, 2, pos.x, pos.y, radius);
                    if (p.type === 'red') {
                        grad.addColorStop(0, '#f87171');
                        grad.addColorStop(1, '#b91c1c');
                    } else {
                        grad.addColorStop(0, '#38bdf8');
                        grad.addColorStop(1, '#0369a1');
                    }
                    ctx.fillStyle = grad;
                    ctx.beginPath();
                    ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.shadowColor = 'transparent';
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    ctx.fillStyle = '#ffffff';
                    ctx.font = `bold ${radius * 0.72}px Inter, sans-serif`;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(p.number || '', pos.x, pos.y + 0.5);

                    if (p.label) {
                        ctx.font = 'bold 10px Cairo, Inter, sans-serif';
                        const lblW = ctx.measureText(p.label).width + 8;
                        ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
                        roundRect(ctx, pos.x - lblW / 2, pos.y + radius + 3, lblW, 14, 4, true, false);
                        ctx.fillStyle = '#f8fafc';
                        ctx.fillText(p.label, pos.x, pos.y + radius + 10);
                    }
                } else if (p.type === 'ball') {
                    const ballR = radius * 0.65;
                    ctx.shadowColor = 'rgba(0, 0, 0, 0.6)';
                    ctx.shadowBlur = 4;
                    ctx.fillStyle = '#ffffff';
                    ctx.beginPath();
                    ctx.arc(pos.x, pos.y, ballR, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#0f172a';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();
                    ctx.fillStyle = '#0f172a';
                    ctx.beginPath();
                    ctx.arc(pos.x, pos.y, ballR * 0.38, 0, Math.PI * 2);
                    ctx.fill();
                } else if (p.type === 'cone') {
                    const coneR = radius * 0.65;
                    ctx.fillStyle = '#f97316';
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.moveTo(pos.x, pos.y - coneR);
                    ctx.lineTo(pos.x + coneR, pos.y + coneR * 0.8);
                    ctx.lineTo(pos.x - coneR, pos.y + coneR * 0.8);
                    ctx.closePath();
                    ctx.fill();
                    ctx.stroke();
                }
                ctx.restore();
            });
        }

        function render() {
            drawPitch();
            drawDrawings();
            drawPieces();
        }

        function getPointerPos(e) {
            const rect = canvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return { x: clientX - rect.left, y: clientY - rect.top };
        }

        function findPieceAt(cx, cy) {
            const hitRadius = Math.max(18, pitchRect.w * 0.025);
            for (let i = pieces.length - 1; i >= 0; i--) {
                const pos = normToCanvas(pieces[i].nx, pieces[i].ny);
                if (Math.hypot(cx - pos.x, cy - pos.y) <= hitRadius) return pieces[i];
            }
            return null;
        }

        function handlePointerDown(e) {
            const pos = getPointerPos(e);
            const norm = canvasToNorm(pos.x, pos.y);
            if (currentTool === 'select') {
                const hit = findPieceAt(pos.x, pos.y);
                if (hit) {
                    saveHistory();
                    draggingPiece = hit;
                    const pCanvas = normToCanvas(hit.nx, hit.ny);
                    dragOffset = { x: pos.x - pCanvas.x, y: pos.y - pCanvas.y };
                    pieces = pieces.filter(p => p.id !== hit.id);
                    pieces.push(hit);
                    render();
                }
            } else if (currentTool === 'polygon') {
                polygonPoints.push(norm);
                document.getElementById('polygon-controls').classList.remove('hidden');
                render();
            } else if (currentTool === 'text') {
                pendingTextPos = norm;
                document.getElementById('annotation-input').value = '';
                document.getElementById('text-modal').classList.remove('hidden');
                setTimeout(() => document.getElementById('annotation-input').focus(), 50);
            } else {
                isDrawing = true;
                currentDraft = { type: currentTool, points: [norm, norm], color: currentColor, width: currentStrokeWidth };
            }
        }

        function handlePointerMove(e) {
            if (draggingPiece) {
                e.preventDefault();
                const pos = getPointerPos(e);
                const norm = canvasToNorm(pos.x - dragOffset.x, pos.y - dragOffset.y);
                draggingPiece.nx = norm.nx;
                draggingPiece.ny = norm.ny;
                render();
            } else if (isDrawing && currentDraft) {
                e.preventDefault();
                const pos = getPointerPos(e);
                currentDraft.points[1] = canvasToNorm(pos.x, pos.y);
                render();
            }
        }

        function handlePointerUp() {
            if (draggingPiece) {
                draggingPiece = null;
                render();
            } else if (isDrawing && currentDraft) {
                isDrawing = false;
                const p1 = currentDraft.points[0];
                const p2 = currentDraft.points[1];
                if (Math.hypot(p2.nx - p1.nx, p2.ny - p1.ny) > 0.015) {
                    saveHistory();
                    drawings.push(currentDraft);
                }
                currentDraft = null;
                render();
            }
        }

        function handleDoubleClick(e) {
            const pos = getPointerPos(e);
            if (currentTool === 'polygon' && polygonPoints.length >= 3) {
                finishPolygon();
                return;
            }
            const hit = findPieceAt(pos.x, pos.y);
            if (hit && (hit.type === 'red' || hit.type === 'blue')) openEditModal(hit);
        }

        canvas.addEventListener('mousedown', handlePointerDown);
        canvas.addEventListener('mousemove', handlePointerMove);
        window.addEventListener('mouseup', handlePointerUp);
        canvas.addEventListener('dblclick', handleDoubleClick);
        canvas.addEventListener('touchstart', handlePointerDown, { passive: false });
        canvas.addEventListener('touchmove', handlePointerMove, { passive: false });
        window.addEventListener('touchend', handlePointerUp);

        function finishPolygon() {
            if (polygonPoints.length >= 3) {
                saveHistory();
                drawings.push({ type: 'polygon', points: [...polygonPoints], color: currentColor, width: currentStrokeWidth });
            }
            cancelPolygon();
        }

        function cancelPolygon() {
            polygonPoints = [];
            document.getElementById('polygon-controls').classList.add('hidden');
            render();
        }

        function closeTextModal() {
            document.getElementById('text-modal').classList.add('hidden');
            pendingTextPos = null;
        }

        function confirmTextAnnotation() {
            const val = document.getElementById('annotation-input').value.trim();
            if (val && pendingTextPos) {
                saveHistory();
                drawings.push({ type: 'text', points: [pendingTextPos], color: currentColor, text: val });
                render();
            }
            closeTextModal();
        }

        document.getElementById('annotation-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') confirmTextAnnotation();
        });

        function openEditModal(piece) {
            editingPieceId = piece.id;
            document.getElementById('edit-number').value = piece.number || '';
            document.getElementById('edit-label').value = piece.label || '';
            document.getElementById('edit-modal').classList.remove('hidden');
        }

        function closeEditModal() {
            document.getElementById('edit-modal').classList.add('hidden');
            editingPieceId = null;
        }

        function quickFillRole(num, label) {
            document.getElementById('edit-number').value = num;
            document.getElementById('edit-label').value = label;
        }

        function saveEditModal() {
            const piece = pieces.find(p => p.id === editingPieceId);
            if (piece) {
                saveHistory();
                piece.number = document.getElementById('edit-number').value.trim();
                piece.label = document.getElementById('edit-label').value.trim();
                render();
            }
            closeEditModal();
        }

        function deleteSelectedPiece() {
            if (editingPieceId) {
                saveHistory();
                pieces = pieces.filter(p => p.id !== editingPieceId);
                render();
                showToast('تم حذف العنصر');
            }
            closeEditModal();
        }

        function addPiece(type) {
            saveHistory();
            const count = pieces.filter(p => p.type === type).length + 1;
            pieces.push({
                id: `${type}_${Date.now()}`,
                type: type,
                nx: 0.5 + (Math.random() - 0.5) * 0.08,
                ny: 0.5 + (Math.random() - 0.5) * 0.08,
                number: (type === 'red' || type === 'blue') ? String(count) : '',
                label: ''
            });
            setTool('select');
            render();
            showToast('تمت إضافة العنصر');
        }

        function setTool(tool) {
            if (currentTool === 'polygon' && tool !== 'polygon') cancelPolygon();
            currentTool = tool;
            document.querySelectorAll('.tool-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById(`tool-${tool}`);
            if (activeBtn) activeBtn.classList.add('active');
            document.getElementById('tool-hint-text').textContent = toolHints[tool] || '';
            canvas.style.cursor = tool === 'select' ? 'grab' : 'crosshair';
        }

        function setColor(hex) {
            currentColor = hex;
            document.querySelectorAll('.color-btn').forEach(btn => {
                if (btn.dataset.color === hex) {
                    btn.classList.add('ring-2', 'ring-white', 'scale-110');
                    btn.classList.remove('opacity-80');
                } else {
                    btn.classList.remove('ring-2', 'ring-white', 'scale-110');
                    btn.classList.add('opacity-80');
                }
            });
        }

        function setPitchMode(mode) {
            pitchMode = mode;
            document.querySelectorAll('.pitch-mode-btn').forEach(btn => {
                btn.classList.remove('active', 'bg-slate-700', 'text-white');
                btn.classList.add('text-slate-400');
            });
            const activeBtn = document.getElementById(`btn-pitch-${mode}`);
            activeBtn.classList.add('active', 'bg-slate-700', 'text-white');
            activeBtn.classList.remove('text-slate-400');
            resizeCanvas();
        }

        function toggleZones() {
            showZones = !showZones;
            const btn = document.getElementById('btn-toggle-zones');
            if (showZones) btn.classList.add('border-amber-500', 'bg-amber-950/40', 'text-amber-200');
            else btn.classList.remove('border-amber-500', 'bg-amber-950/40', 'text-amber-200');
            render();
        }

        function togglePitchTheme() {
            pitchTheme = pitchTheme === 'green' ? 'dark' : 'green';
            document.getElementById('theme-label').textContent = pitchTheme === 'green' ? 'عشب داكن' : 'داكن تكتيكي';
            render();
        }

        function saveHistory() {
            historyStack.push({
                pieces: JSON.parse(JSON.stringify(pieces)),
                drawings: JSON.parse(JSON.stringify(drawings)),
                redTeamMeta: { ...redTeamMeta },
                blueTeamMeta: { ...blueTeamMeta }
            });
            if (historyStack.length > 30) historyStack.shift();
        }

        function undoAction() {
            if (historyStack.length === 0) return showToast('لا يوجد إجراءات للتراجع');
            const prev = historyStack.pop();
            pieces = prev.pieces;
            drawings = prev.drawings;
            if (prev.redTeamMeta) redTeamMeta = prev.redTeamMeta;
            if (prev.blueTeamMeta) blueTeamMeta = prev.blueTeamMeta;
            updateTeamBanner();
            render();
            showToast('تم التراجع');
        }

        function clearDrawings() {
            if (drawings.length === 0) return;
            saveHistory();
            drawings = [];
            cancelPolygon();
            render();
            showToast('تم مسح الرسومات');
        }

        function resetBoard() {
            saveHistory();
            drawings = [];
            cancelPolygon();
            redTeamMeta = { name: 'الفريق الأحمر', formation: '5-4-1' };
            blueTeamMeta = { name: 'الفريق الأزرق', formation: '4-3-3' };
            initDefaultPieces();
            render();
            showToast('تمت إعادة ضبط الملعب');
        }

        function exportPNG() {
            render();
            ctx.save();
            ctx.font = 'bold 12px Cairo, Inter, sans-serif';
            ctx.fillStyle = 'rgba(255, 255, 255, 0.75)';
            ctx.textAlign = 'left';
            ctx.fillText(`${redTeamMeta.name} (${redTeamMeta.formation}) vs ${blueTeamMeta.name} (${blueTeamMeta.formation})`, pitchRect.x + 10, pitchRect.y + pitchRect.h - 10);
            ctx.restore();

            const link = document.createElement('a');
            link.download = `tactical-board-${Date.now()}.png`;
            link.href = canvas.toDataURL('image/png', 1.0);
            link.click();
            render();
            showToast('تم تحميل الصورة بنجاح');
        }

        function hexToRgba(hex, alpha) {
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        }

        function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
            ctx.beginPath();
            ctx.moveTo(x + radius, y);
            ctx.lineTo(x + width - radius, y);
            ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
            ctx.lineTo(x + width, y + height - radius);
            ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
            ctx.lineTo(x + radius, y + height);
            ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
            ctx.lineTo(x, y + radius);
            ctx.quadraticCurveTo(x, y, x + radius, y);
            ctx.closePath();
            if (fill) ctx.fill();
            if (stroke) ctx.stroke();
        }

        let toastTimer = null;
        function showToast(msg) {
            const el = document.getElementById('toast-msg');
            el.textContent = msg;
            el.classList.remove('opacity-0');
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => el.classList.add('opacity-0'), 2200);
        }

        window.addEventListener('resize', resizeCanvas);
        window.onload = function () {
            initDefaultPieces();
            resizeCanvas();
        };
    </script>
</body>
</html>
"""

# عرض اللوحة التكتيكية داخل Streamlit بارتفاع مناسب لشاشة العرض الكاملة
components.html(tactical_board_html, height=800, scrolling=False)
