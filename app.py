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
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Inter:wght@500;600;700;800&display=swap" rel="stylesheet">
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
        .fmt-btn.active {
            background-color: #2563eb;
            color: #ffffff;
            border-color: #60a5fa;
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
                    ProTactics <span class="text-xs font-normal text-emerald-400 bg-emerald-950/80 border border-emerald-800/60 px-2 py-0.5 rounded-full mr-1">Studio</span>
                </h1>
                <p class="text-[11px] text-slate-400 hidden sm:block">لوحة التحليل والرسم التكتيكي الاحترافية</p>
            </div>
        </div>

        <div class="flex flex-wrap items-center gap-2">
            <!-- زر إدارة تشكيلة وأسماء وألوان وشعارات الفريقين -->
            <button onclick="openLineupModal()" class="flex items-center gap-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white border border-blue-400/40 text-xs px-3 py-1.5 rounded-lg shadow-md shadow-blue-950/50 transition font-bold">
                <i class="fa-solid fa-shield-halved"></i>
                <span>الفريقين (الأسماء، الألوان، الشعارات)</span>
            </button>

            <!-- زر إظهار/إخفاء شريط تنسيق النصوص -->
            <button onclick="toggleTextFormatBar()" id="btn-text-fmt" class="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs px-3 py-1.5 rounded-lg transition font-semibold">
                <i class="fa-solid fa-bold text-yellow-400"></i>
                <span>تنسيق النصوص</span>
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
                <span>5-Zones</span>
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

    <!-- شريط تنسيق النصوص (Text Formatting Toolbar) -->
    <div id="text-format-bar" class="hidden bg-slate-900 border-b border-slate-800 px-4 py-1.5 flex flex-wrap items-center justify-center gap-3 z-10 shadow-md">
        <span class="text-xs font-bold text-blue-400 flex items-center gap-1">
            <i class="fa-solid fa-pen-nib"></i> تنسيق النص الافتراضي:
        </span>
        <div class="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
            <button onclick="toggleDefaultBold()" id="fmt-bold-btn" class="fmt-btn active px-2.5 py-1 rounded text-xs font-en font-bold border border-transparent transition" title="خط عريض Bold">
                B
            </button>
            <button onclick="toggleDefaultItalic()" id="fmt-italic-btn" class="fmt-btn px-2.5 py-1 rounded text-xs font-en italic border border-transparent text-slate-300 transition" title="خط مائل Italic">
                I
            </button>
            <button onclick="toggleDefaultBg()" id="fmt-bg-btn" class="fmt-btn active px-2.5 py-1 rounded text-xs border border-transparent transition" title="خلفية داكنة للنص">
                <i class="fa-solid fa-square"></i> خلفية
            </button>
        </div>
        <div class="flex items-center gap-1.5 bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800">
            <span class="text-[11px] text-slate-400">حجم الخط:</span>
            <select id="default-font-size" onchange="defaultTextStyle.size = parseInt(this.value)" class="bg-transparent text-xs font-en font-bold text-white focus:outline-none cursor-pointer">
                <option value="12" class="bg-slate-900">صغير (12px)</option>
                <option value="15" selected class="bg-slate-900">متوسط (15px)</option>
                <option value="19" class="bg-slate-900">كبير (19px)</option>
                <option value="24" class="bg-slate-900">عنوان (24px)</option>
            </select>
        </div>
        <span class="text-[11px] text-slate-400 hidden md:inline">💡 انقر مرتين (Double Click) على أي نص في الملعب لتعديله</span>
    </div>

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
                <div class="hidden md:block text-[11px] font-bold text-slate-400 px-1">لون الرسم والنص</div>
                <div class="flex items-center justify-around gap-1.5 bg-slate-900/90 p-1.5 rounded-lg border border-slate-800">
                    <button onclick="setColor('#facc15')" data-color="#facc15" class="color-btn w-6 h-6 rounded-full bg-yellow-400 ring-2 ring-white scale-110 transition"></button>
                    <button onclick="setColor('#ffffff')" data-color="#ffffff" class="color-btn w-6 h-6 rounded-full bg-white opacity-80 hover:opacity-100 transition"></button>
                    <button onclick="setColor('#ef4444')" data-color="#ef4444" class="color-btn w-6 h-6 rounded-full bg-red-500 opacity-80 hover:opacity-100 transition"></button>
                    <button onclick="setColor('#38bdf8')" data-color="#38bdf8" class="color-btn w-6 h-6 rounded-full bg-sky-400 opacity-80 hover:opacity-100 transition"></button>
                    <button onclick="setColor('#22c55e')" data-color="#22c55e" class="color-btn w-6 h-6 rounded-full bg-green-500 opacity-80 hover:opacity-100 transition"></button>
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
                    <button onclick="addPiece('team1')" class="flex items-center justify-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 py-1.5 px-2 rounded-lg text-xs font-semibold transition">
                        <span id="sidebar-team1-dot" class="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
                        <span>+ لاعب (1)</span>
                    </button>
                    <button onclick="addPiece('team2')" class="flex items-center justify-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 py-1.5 px-2 rounded-lg text-xs font-semibold transition">
                        <span id="sidebar-team2-dot" class="w-3 h-3 rounded-full bg-sky-500 inline-block"></span>
                        <span>+ لاعب (2)</span>
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
                <span id="tool-hint-text">اسحب اللاعبين لتحريكهم. انقر مرتين (Double Click) على أي لاعب أو نص لتعديله وتنسيقه.</span>
            </div>
        </aside>

        <!-- Canvas Area -->
        <main id="canvas-container" class="flex-1 relative bg-[#080c14] flex flex-col items-center justify-center p-2 sm:p-3 overflow-hidden">
            <!-- شريط عرض أسماء الفريقين وشعاراتهم وخططهم أعلى الملعب -->
            <div class="w-full max-w-4xl flex items-center justify-between bg-slate-900/95 border border-slate-800 rounded-xl px-4 py-1.5 mb-2 shadow-md">
                <div class="flex items-center gap-2.5">
                    <img id="banner-team1-logo" src="" alt="" class="hidden w-7 h-7 object-contain rounded bg-slate-800/80 p-0.5 border border-slate-700">
                    <span id="banner-team1-dot" class="w-3.5 h-3.5 rounded-full bg-red-500 inline-block border border-white/50"></span>
                    <span id="display-team1-name" class="text-xs sm:text-sm font-bold text-white">الفريق الأول</span>
                    <span id="display-team1-form" class="text-[11px] font-en font-semibold bg-slate-800 text-slate-200 border border-slate-700 px-2 py-0.5 rounded">5-4-1</span>
                </div>
                <span class="text-xs font-en font-extrabold text-slate-500 tracking-wider">VS</span>
                <div class="flex items-center gap-2.5">
                    <span id="display-team2-form" class="text-[11px] font-en font-semibold bg-slate-800 text-slate-200 border border-slate-700 px-2 py-0.5 rounded">4-3-3</span>
                    <span id="display-team2-name" class="text-xs sm:text-sm font-bold text-white">الفريق الثاني</span>
                    <span id="banner-team2-dot" class="w-3.5 h-3.5 rounded-full bg-sky-500 inline-block border border-white/50"></span>
                    <img id="banner-team2-logo" src="" alt="" class="hidden w-7 h-7 object-contain rounded bg-slate-800/80 p-0.5 border border-slate-700">
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

    <!-- Modal: Lineup, Colors & Logos Manager -->
    <div id="lineup-modal" class="hidden fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center z-50 p-3 sm:p-4">
        <div class="bg-[#111827] border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[92vh] flex flex-col shadow-2xl">
            <div class="flex items-center justify-between border-b border-slate-800 px-5 py-3.5 shrink-0">
                <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-shield-halved text-blue-400"></i>
                    <span>إعداد الفريقين (الأسماء، ألوان القمصان، الشعارات، التشكيلة)</span>
                </h3>
                <button onclick="closeLineupModal()" class="text-slate-400 hover:text-white"><i class="fa-solid fa-xmark text-xl"></i></button>
            </div>

            <div class="p-4 sm:p-5 overflow-y-auto grid grid-cols-1 md:grid-cols-2 gap-5">
                <!-- الفريق الأول -->
                <div class="bg-slate-900/80 border border-slate-700/80 rounded-xl p-3.5">
                    <div class="flex items-center justify-between mb-3 pb-2 border-b border-slate-800">
                        <span class="font-bold text-sm text-white">الفريق الأول (يسار الملعب)</span>
                        <label class="cursor-pointer bg-slate-800 hover:bg-slate-700 text-xs text-blue-300 border border-slate-700 px-2.5 py-1 rounded-lg flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-image"></i>
                            <span>رفع شعار النادي</span>
                            <input type="file" accept="image/*" onchange="handleLogoUpload('team1', this)" class="hidden">
                        </label>
                    </div>

                    <!-- معاينة الشعار واختيار اللون -->
                    <div class="flex items-center gap-3 mb-3 bg-slate-950/80 p-2.5 rounded-lg border border-slate-800">
                        <div class="w-11 h-11 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center overflow-hidden shrink-0">
                            <img id="preview-team1-logo" src="" class="hidden w-full h-full object-contain p-1">
                            <i id="placeholder-team1-logo" class="fa-solid fa-shield text-slate-600 text-lg"></i>
                        </div>
                        <div class="flex-1">
                            <label class="block text-[11px] text-slate-400 mb-1">لون قمصان الفريق:</label>
                            <div class="flex items-center gap-1.5 flex-wrap">
                                <input type="color" id="input-team1-color" value="#dc2626" class="w-7 h-7 rounded cursor-pointer bg-transparent border-0">
                                <button type="button" onclick="setTeamColorInput('team1', '#dc2626')" class="w-5 h-5 rounded-full bg-red-600 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team1', '#ffffff')" class="w-5 h-5 rounded-full bg-white border border-slate-400"></button>
                                <button type="button" onclick="setTeamColorInput('team1', '#facc15')" class="w-5 h-5 rounded-full bg-yellow-400 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team1', '#16a34a')" class="w-5 h-5 rounded-full bg-green-600 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team1', '#111827')" class="w-5 h-5 rounded-full bg-gray-900 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team1', '#7c3aed')" class="w-5 h-5 rounded-full bg-violet-600 border border-white/40"></button>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-2 mb-3">
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">اسم النادي:</label>
                            <input type="text" id="input-team1-name" value="الفريق الأول" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">الخطة التكتيكية:</label>
                            <select id="select-team1-formation" onchange="populateLineupInputs('team1', this.value)" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2 py-1.5 text-xs font-en text-white focus:outline-none focus:border-blue-500">
                                <option value="5-4-1">5-4-1</option>
                                <option value="4-3-3">4-3-3</option>
                                <option value="3-5-2">3-5-2</option>
                                <option value="4-2-3-1">4-2-3-1</option>
                                <option value="4-4-2">4-4-2</option>
                            </select>
                        </div>
                    </div>
                    <div id="team1-players-list" class="space-y-1.5 max-h-56 overflow-y-auto pr-1"></div>
                </div>

                <!-- الفريق الثاني -->
                <div class="bg-slate-900/80 border border-slate-700/80 rounded-xl p-3.5">
                    <div class="flex items-center justify-between mb-3 pb-2 border-b border-slate-800">
                        <span class="font-bold text-sm text-white">الفريق الثاني (يمين الملعب)</span>
                        <label class="cursor-pointer bg-slate-800 hover:bg-slate-700 text-xs text-blue-300 border border-slate-700 px-2.5 py-1 rounded-lg flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-image"></i>
                            <span>رفع شعار النادي</span>
                            <input type="file" accept="image/*" onchange="handleLogoUpload('team2', this)" class="hidden">
                        </label>
                    </div>

                    <!-- معاينة الشعار واختيار اللون -->
                    <div class="flex items-center gap-3 mb-3 bg-slate-950/80 p-2.5 rounded-lg border border-slate-800">
                        <div class="w-11 h-11 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center overflow-hidden shrink-0">
                            <img id="preview-team2-logo" src="" class="hidden w-full h-full object-contain p-1">
                            <i id="placeholder-team2-logo" class="fa-solid fa-shield text-slate-600 text-lg"></i>
                        </div>
                        <div class="flex-1">
                            <label class="block text-[11px] text-slate-400 mb-1">لون قمصان الفريق:</label>
                            <div class="flex items-center gap-1.5 flex-wrap">
                                <input type="color" id="input-team2-color" value="#0284c7" class="w-7 h-7 rounded cursor-pointer bg-transparent border-0">
                                <button type="button" onclick="setTeamColorInput('team2', '#0284c7')" class="w-5 h-5 rounded-full bg-sky-600 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team2', '#ffffff')" class="w-5 h-5 rounded-full bg-white border border-slate-400"></button>
                                <button type="button" onclick="setTeamColorInput('team2', '#facc15')" class="w-5 h-5 rounded-full bg-yellow-400 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team2', '#ea580c')" class="w-5 h-5 rounded-full bg-orange-600 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team2', '#111827')" class="w-5 h-5 rounded-full bg-gray-900 border border-white/40"></button>
                                <button type="button" onclick="setTeamColorInput('team2', '#dc2626')" class="w-5 h-5 rounded-full bg-red-600 border border-white/40"></button>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-2 mb-3">
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">اسم النادي:</label>
                            <input type="text" id="input-team2-name" value="الفريق الثاني" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block text-[11px] text-slate-400 mb-1">الخطة التكتيكية:</label>
                            <select id="select-team2-formation" onchange="populateLineupInputs('team2', this.value)" class="w-full bg-slate-950 border border-slate-700 rounded-lg px-2 py-1.5 text-xs font-en text-white focus:outline-none focus:border-blue-500">
                                <option value="4-3-3">4-3-3</option>
                                <option value="4-2-3-1">4-2-3-1</option>
                                <option value="5-4-1">5-4-1</option>
                                <option value="3-5-2">3-5-2</option>
                                <option value="4-4-2">4-4-2</option>
                            </select>
                        </div>
                    </div>
                    <div id="team2-players-list" class="space-y-1.5 max-h-56 overflow-y-auto pr-1"></div>
                </div>
            </div>

            <div class="flex items-center justify-end gap-2 px-5 py-3 border-t border-slate-800 shrink-0 bg-slate-900/50 rounded-b-2xl">
                <button onclick="closeLineupModal()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-4 py-2 rounded-lg transition">إلغاء</button>
                <button onclick="applyBothTeamsLineups()" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-5 py-2 rounded-lg shadow-lg shadow-emerald-950/50 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-check"></i>
                    <span>تطبيق التغييرات على الملعب</span>
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
                    <label class="block text-xs font-semibold text-slate-400 mb-1">الرقم أو الرمز داخل الدائرة:</label>
                    <input type="text" id="edit-number" maxlength="4" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white font-en font-bold focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">اسم اللاعب أو المركز أسفل الدائرة:</label>
                    <input type="text" id="edit-label" maxlength="18" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-400 mb-1">لون مخصص لهذا اللاعب فقط:</label>
                    <input type="color" id="edit-piece-color" class="w-full h-8 rounded cursor-pointer bg-slate-900 border border-slate-700">
                </div>
            </div>
            <div class="flex items-center justify-between gap-2 mt-5 pt-3 border-t border-slate-800">
                <button onclick="deleteSelectedPiece()" class="bg-red-950/70 hover:bg-red-900 text-red-300 border border-red-800/70 text-xs font-semibold px-3 py-2 rounded-lg transition">حذف</button>
                <div class="flex items-center gap-2">
                    <button onclick="closeEditModal()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-3 py-2 rounded-lg">إلغاء</button>
                    <button onclick="saveEditModal()" class="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-lg">حفظ</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal: Add / Edit Rich Text Annotation -->
    <div id="text-modal" class="hidden fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-[#111827] border border-slate-700 rounded-2xl w-full max-w-md p-5 shadow-2xl">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                <h3 class="text-base font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-font text-yellow-400"></i>
                    <span id="text-modal-title">إضافة وتنسيق نص تكتيكي</span>
                </h3>
                <button onclick="closeTextModal()" class="text-slate-400 hover:text-white"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>

            <input type="text" id="annotation-input" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 mb-3" placeholder="اكتب النص التكتيكي هنا...">

            <!-- أدوات التنسيق داخل نافذة النص -->
            <div class="flex flex-wrap items-center justify-between gap-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800 mb-4">
                <div class="flex items-center gap-1.5">
                    <button type="button" id="modal-btn-bold" onclick="toggleModalTextFlag('bold')" class="fmt-btn active px-3 py-1.5 rounded-lg text-xs font-en font-extrabold border border-slate-700 transition">B</button>
                    <button type="button" id="modal-btn-italic" onclick="toggleModalTextFlag('italic')" class="fmt-btn px-3 py-1.5 rounded-lg text-xs font-en italic border border-slate-700 text-slate-300 transition">I</button>
                    <button type="button" id="modal-btn-bg" onclick="toggleModalTextFlag('hasBg')" class="fmt-btn active px-2.5 py-1.5 rounded-lg text-xs border border-slate-700 transition">خلفية</button>
                </div>
                <div class="flex items-center gap-2">
                    <select id="modal-text-size" class="bg-slate-900 border border-slate-700 rounded-lg px-2 py-1 text-xs font-en text-white">
                        <option value="12">12px</option>
                        <option value="15" selected>15px</option>
                        <option value="19">19px</option>
                        <option value="24">24px</option>
                    </select>
                    <input type="color" id="modal-text-color" value="#facc15" class="w-7 h-7 rounded cursor-pointer bg-transparent border-0">
                </div>
            </div>

            <div class="flex items-center justify-between gap-2">
                <button id="btn-delete-text" onclick="deleteEditingText()" class="hidden bg-red-950/70 hover:bg-red-900 text-red-300 border border-red-800/70 text-xs font-semibold px-3 py-2 rounded-lg">حذف النص</button>
                <div class="flex items-center gap-2 mr-auto">
                    <button onclick="closeTextModal()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-3 py-2 rounded-lg">إلغاء</button>
                    <button onclick="confirmTextAnnotation()" class="bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold px-4 py-2 rounded-lg">حفظ النص</button>
                </div>
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

        // إعدادات التنسيق الافتراضية للنصوص
        let defaultTextStyle = {
            bold: true,
            italic: false,
            size: 15,
            hasBg: true
        };

        // بيانات الفريقين (الاسم، الخطة، اللون، الشعار)
        let team1Meta = { name: 'الفريق الأول', formation: '5-4-1', color: '#dc2626', logoSrc: '', logoImg: null };
        let team2Meta = { name: 'الفريق الثاني', formation: '4-3-3', color: '#0284c7', logoSrc: '', logoImg: null };
        let tempLogos = { team1: '', team2: '' };

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
        let editingTextIndex = null;
        let modalTextFlags = { bold: true, italic: false, hasBg: true };

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
            select: 'اسحب اللاعبين لتحريكهم بحرية. انقر مرتين (Double Click) على أي لاعب أو نص لتعديله وتنسيقه.',
            arrow: 'اضغط واسحب على الملعب لرسم سهم حركة مستقيم.',
            curved: 'اضغط واسحب لرسم سهم حركة مقوس (Curved Run) للضغط القوسي وغلق زوايا التمرير.',
            pass: 'اضغط واسحب لرسم خط تمرير متقطع بين اللاعبين.',
            polygon: 'انقر في عدة نقاط لتحديد زوايا منطقة، ثم اضغط "إغلاق وتظليل".',
            ruler: 'اضغط واسحب بين خطين أو لاعبين لقياس المسافة بالمتر (105×68م).',
            connect: 'اضغط واسحب من لاعب إلى آخر لربطهم بخط تكتيكي.',
            text: 'انقر في أي مكان على الملعب لإضافة نص وتنسيقه (Bold / Italic / الحجم).'
        };

        // حساب تباين اللون لاختيار نص أبيض أو أسود تلقائياً داخل دائرة اللاعب
        function getContrastTextColor(hex) {
            if (!hex || hex.length < 7) return '#ffffff';
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
            return (yiq >= 145) ? '#0f172a' : '#ffffff';
        }

        function initDefaultPieces() {
            pieces = [];
            formationTemplates['5-4-1'].forEach((p, idx) => {
                pieces.push({ id: 'team1_' + idx, type: 'team1', nx: p.nx, ny: p.ny, number: p.num, label: p.label, color: team1Meta.color });
            });
            formationTemplates['4-3-3'].forEach((p, idx) => {
                pieces.push({ id: 'team2_' + idx, type: 'team2', nx: 1 - p.nx, ny: p.ny, number: p.num, label: p.label, color: team2Meta.color });
            });
            pieces.push({ id: 'ball_1', type: 'ball', nx: 0.50, ny: 0.50, number: '', label: '' });
            updateTeamBanner();
        }

        function updateTeamBanner() {
            document.getElementById('display-team1-name').textContent = team1Meta.name;
            document.getElementById('display-team1-form').textContent = team1Meta.formation;
            document.getElementById('banner-team1-dot').style.backgroundColor = team1Meta.color;
            document.getElementById('sidebar-team1-dot').style.backgroundColor = team1Meta.color;

            const logo1El = document.getElementById('banner-team1-logo');
            if (team1Meta.logoSrc) {
                logo1El.src = team1Meta.logoSrc;
                logo1El.classList.remove('hidden');
            } else {
                logo1El.classList.add('hidden');
            }

            document.getElementById('display-team2-name').textContent = team2Meta.name;
            document.getElementById('display-team2-form').textContent = team2Meta.formation;
            document.getElementById('banner-team2-dot').style.backgroundColor = team2Meta.color;
            document.getElementById('sidebar-team2-dot').style.backgroundColor = team2Meta.color;

            const logo2El = document.getElementById('banner-team2-logo');
            if (team2Meta.logoSrc) {
                logo2El.src = team2Meta.logoSrc;
                logo2El.classList.remove('hidden');
            } else {
                logo2El.classList.add('hidden');
            }
        }

        // تنسيق النصوص (Toolbar Functions)
        function toggleTextFormatBar() {
            const bar = document.getElementById('text-format-bar');
            const btn = document.getElementById('btn-text-fmt');
            bar.classList.toggle('hidden');
            if (!bar.classList.contains('hidden')) {
                btn.classList.add('border-blue-500', 'bg-slate-800', 'text-white');
            } else {
                btn.classList.remove('border-blue-500', 'bg-slate-800', 'text-white');
            }
            resizeCanvas();
        }

        function toggleDefaultBold() {
            defaultTextStyle.bold = !defaultTextStyle.bold;
            document.getElementById('fmt-bold-btn').classList.toggle('active', defaultTextStyle.bold);
        }

        function toggleDefaultItalic() {
            defaultTextStyle.italic = !defaultTextStyle.italic;
            document.getElementById('fmt-italic-btn').classList.toggle('active', defaultTextStyle.italic);
        }

        function toggleDefaultBg() {
            defaultTextStyle.hasBg = !defaultTextStyle.hasBg;
            document.getElementById('fmt-bg-btn').classList.toggle('active', defaultTextStyle.hasBg);
        }

        // إدارة نافذة الفريقين والألوان والشعارات
        function openLineupModal() {
            document.getElementById('input-team1-name').value = team1Meta.name;
            document.getElementById('select-team1-formation').value = team1Meta.formation;
            document.getElementById('input-team1-color').value = team1Meta.color;
            tempLogos.team1 = team1Meta.logoSrc;
            updateLogoPreview('team1', team1Meta.logoSrc);

            document.getElementById('input-team2-name').value = team2Meta.name;
            document.getElementById('select-team2-formation').value = team2Meta.formation;
            document.getElementById('input-team2-color').value = team2Meta.color;
            tempLogos.team2 = team2Meta.logoSrc;
            updateLogoPreview('team2', team2Meta.logoSrc);

            populateLineupInputs('team1', team1Meta.formation, true);
            populateLineupInputs('team2', team2Meta.formation, true);
            document.getElementById('lineup-modal').classList.remove('hidden');
        }

        function closeLineupModal() {
            document.getElementById('lineup-modal').classList.add('hidden');
        }

        function setTeamColorInput(team, hex) {
            document.getElementById(`input-${team}-color`).value = hex;
        }

        function handleLogoUpload(team, input) {
            const file = input.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                tempLogos[team] = e.target.result;
                updateLogoPreview(team, e.target.result);
            };
            reader.readAsDataURL(file);
        }

        function updateLogoPreview(team, src) {
            const img = document.getElementById(`preview-${team}-logo`);
            const icon = document.getElementById(`placeholder-${team}-logo`);
            if (src) {
                img.src = src;
                img.classList.remove('hidden');
                icon.classList.add('hidden');
            } else {
                img.classList.add('hidden');
                icon.classList.remove('hidden');
            }
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
                        class="flex-1 bg-slate-950 border border-slate-700 rounded px-2.5 py-1 text-xs text-white focus:outline-none focus:border-blue-500" placeholder="اسم اللاعب...">
                `;
                containerEl.appendChild(row);
            });
        }

        function applyBothTeamsLineups() {
            saveHistory();

            const t1Name = document.getElementById('input-team1-name').value.trim() || 'الفريق الأول';
            const t1Form = document.getElementById('select-team1-formation').value;
            const t1Color = document.getElementById('input-team1-color').value;

            const t2Name = document.getElementById('input-team2-name').value.trim() || 'الفريق الثاني';
            const t2Form = document.getElementById('select-team2-formation').value;
            const t2Color = document.getElementById('input-team2-color').value;

            team1Meta = { name: t1Name, formation: t1Form, color: t1Color, logoSrc: tempLogos.team1, logoImg: null };
            team2Meta = { name: t2Name, formation: t2Form, color: t2Color, logoSrc: tempLogos.team2, logoImg: null };

            if (team1Meta.logoSrc) {
                const img1 = new Image();
                img1.src = team1Meta.logoSrc;
                team1Meta.logoImg = img1;
            }
            if (team2Meta.logoSrc) {
                const img2 = new Image();
                img2.src = team2Meta.logoSrc;
                team2Meta.logoImg = img2;
            }

            pieces = pieces.filter(p => p.type !== 'team1' && p.type !== 'team2');

            formationTemplates[t1Form].forEach((slot, idx) => {
                const numInput = document.querySelector(`input[data-team="team1"][data-idx="${idx}"][data-field="num"]`);
                const lblInput = document.querySelector(`input[data-team="team1"][data-idx="${idx}"][data-field="label"]`);
                const posX = pitchMode === 'half' ? Math.min(0.48, slot.nx * 0.95) : slot.nx;
                pieces.push({
                    id: 'team1_' + idx,
                    type: 'team1',
                    nx: posX,
                    ny: slot.ny,
                    number: numInput ? numInput.value.trim() : slot.num,
                    label: lblInput ? lblInput.value.trim() : slot.label,
                    color: t1Color
                });
            });

            formationTemplates[t2Form].forEach((slot, idx) => {
                const numInput = document.querySelector(`input[data-team="team2"][data-idx="${idx}"][data-field="num"]`);
                const lblInput = document.querySelector(`input[data-team="team2"][data-idx="${idx}"][data-field="label"]`);
                const posX = pitchMode === 'half' ? Math.max(0.52, 1 - slot.nx * 0.95) : (1 - slot.nx);
                pieces.push({
                    id: 'team2_' + idx,
                    type: 'team2',
                    nx: posX,
                    ny: slot.ny,
                    number: numInput ? numInput.value.trim() : slot.num,
                    label: lblInput ? lblInput.value.trim() : slot.label,
                    color: t2Color
                });
            });

            updateTeamBanner();
            closeLineupModal();
            render();
            showToast('تم تحديث الفريقين والألوان والشعارات');
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
                ctx.arc(x + w - spotDist, y + h / 2,
