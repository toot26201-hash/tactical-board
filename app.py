<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ProTactics 3D PRO | TootScouting</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Inter:wght@500;600;700;800;900&display=swap" rel="stylesheet" />
  <style>
    html, body { width: 100%; height: 100vh; margin: 0; padding: 0; font-family: "Cairo", "Inter", sans-serif; background: #070b14; color: #e2e8f0; overflow: hidden; user-select: none; }
    .font-en { font-family: "Inter", sans-serif; }
    .tool-btn { transition: all 0.15s ease; }
    .tool-btn.active { background: #2563eb; color: #ffffff; border-color: #60a5fa; }
    .frame-btn.active { background: #10b981; color: #052e16; border-color: #34d399; font-weight: 800; }
    .stroke-btn.active { background: #facc15; color: #0f172a; font-weight: 800; }
    .pitch-grid-bg {
      background-image: radial-gradient(rgba(212, 175, 55, 0.12) 1px, transparent 1px),
                        linear-gradient(to bottom, rgba(7, 11, 20, 0.85), rgba(7, 11, 20, 0.98));
      background-size: 28px 28px, 100% 100%;
    }
    .gold-glow { box-shadow: 0 0 35px rgba(212, 175, 55, 0.18); }
  </style>
</head>
<body class="flex flex-col h-screen overflow-hidden">

<!-- ================= 1. صفحة الهبوط (Landing Page) ================= -->
<div id="landing-page" class="fixed inset-0 z-[110] w-full h-full bg-[#070b14] pitch-grid-bg overflow-y-auto overflow-x-hidden select-text">
  <!-- شريط التنقل العلوي -->
  <nav class="sticky top-0 z-20 bg-[#070b14]/90 backdrop-blur-md border-b border-slate-800/80 px-4 md:px-10 py-3 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-yellow-600 flex items-center justify-center text-slate-950 font-black text-lg shadow-lg">
        <i class="fa-solid fa-futbol"></i>
      </div>
      <div>
        <div class="font-en font-black text-base md:text-lg tracking-wide text-white leading-none">
          Toot<span class="text-amber-400">Scouting</span>
        </div>
        <div class="text-[11px] text-slate-400 font-semibold mt-0.5">ProTactics 3D PRO</div>
      </div>
    </div>

    <div class="flex items-center gap-2 md:gap-3">
      <a href="#features" class="hidden md:inline-block text-xs font-bold text-slate-300 hover:text-amber-400 px-3 py-1.5 transition">المميزات</a>
      <a href="#pricing" class="hidden md:inline-block text-xs font-bold text-slate-300 hover:text-amber-400 px-3 py-1.5 transition">الباقات</a>
      <button onclick="openAuthFromLanding('login')" class="text-xs font-bold text-slate-200 hover:text-white border border-slate-700 hover:border-slate-500 px-3.5 py-2 rounded-xl transition">
        تسجيل الدخول
      </button>
      <button onclick="openAuthFromLanding('signup')" class="text-xs font-extrabold bg-gradient-to-r from-amber-400 to-yellow-500 hover:from-amber-300 hover:to-yellow-400 text-slate-950 px-4 py-2 rounded-xl shadow-lg transition">
        ابدأ مجاناً 🚀
      </button>
    </div>
  </nav>

  <!-- القسم الرئيسي (Hero Section) -->
  <section class="max-w-6xl mx-auto px-4 md:px-8 pt-12 pb-14 text-center space-y-6">
    <div class="inline-flex items-center gap-2 bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-bold px-4 py-1.5 rounded-full">
      <i class="fa-solid fa-wand-magic-sparkles"></i> المنصة العربية الأولى لمحللي الأداء والمدربين المحترفين
    </div>

    <h1 class="text-3xl md:text-5xl font-black text-white leading-tight max-w-4xl mx-auto">
      حوّل أفكارك التكتيكية إلى <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-yellow-400 to-amber-500">تحريك 3D احترافي</span> في ثوانٍ
    </h1>

    <p class="text-sm md:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
      صمّم الجمل التكتيكية، الكرات الثابتة، سيناريوهات الضغط، وحركات اللاعبين بإطارات متسلسلة (Keyframes)، واحفظ خططك على السحابة أو صدّرها كفيديو جاهز للمحاضرات الفنية والتحليل.
    </p>

    <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
      <button onclick="openAuthFromLanding('signup')" class="bg-gradient-to-r from-amber-400 to-yellow-500 hover:from-amber-300 hover:to-yellow-400 text-slate-950 font-black text-sm px-7 py-3.5 rounded-2xl shadow-xl gold-glow transition flex items-center gap-2">
        <span>افتح السبورة التكتيكية الآن</span>
        <i class="fa-solid fa-arrow-left"></i>
      </button>
      <button onclick="openAuthFromLanding('login')" class="bg-slate-900 hover:bg-slate-800 text-white border border-slate-700 font-bold text-sm px-6 py-3.5 rounded-2xl transition">
        لدي حساب بالفعل
      </button>
    </div>

    <!-- معاينة بصرية مصغرة لواجهة التحليل -->
    <div class="max-w-4xl mx-auto mt-10 bg-slate-900/90 border border-slate-800 rounded-2xl p-3 shadow-2xl gold-glow">
      <div class="bg-[#133824] border-2 border-white/40 rounded-xl p-6 relative overflow-hidden">
        <div class="flex items-center justify-between text-[11px] font-en text-amber-300 font-bold mb-4">
          <span>● LIVE TACTICAL ENGINE 3D</span>
          <span>TootScouting • ProTactics PRO</span>
        </div>
        <div class="grid grid-cols-3 gap-4 items-center py-6">
          <div class="flex flex-col items-center gap-2">
            <div class="w-10 h-10 rounded-full bg-red-600 border-2 border-white flex items-center justify-center font-en font-black text-white shadow-lg">6</div>
            <span class="text-[11px] bg-slate-950/80 px-2 py-0.5 rounded text-white font-bold">Pivot • ارتكاز</span>
          </div>
          <div class="flex flex-col items-center gap-1 text-amber-300">
            <i class="fa-solid fa-share text-2xl animate-pulse"></i>
            <span class="text-[11px] font-en font-bold bg-slate-950/80 px-2.5 py-0.5 rounded">18.4 m • Line Breaking Pass</span>
          </div>
          <div class="flex flex-col items-center gap-2">
            <div class="w-10 h-10 rounded-full bg-red-600 border-2 border-amber-400 ring-4 ring-amber-400/30 flex items-center justify-center font-en font-black text-white shadow-lg">10</div>
            <span class="text-[11px] bg-slate-950/80 px-2 py-0.5 rounded text-amber-300 font-bold">Half-Space • بين الخطوط</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- قسم المميزات (Features) -->
  <section id="features" class="max-w-6xl mx-auto px-4 md:px-8 py-12 border-t border-slate-800/80">
    <div class="text-center mb-10">
      <h2 class="text-2xl md:text-3xl font-black text-white">كل أدوات محلل الأداء في مكان واحد</h2>
      <p class="text-xs md:text-sm text-slate-400 mt-1.5">مصممة خصيصاً لتلبية احتياجات المحللين والمدربين في الأندية والأكاديميات</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <div class="bg-slate-900/80 border border-slate-800 hover:border-amber-500/40 rounded-2xl p-5 space-y-2.5 transition">
        <div class="w-10 h-10 rounded-xl bg-amber-500/15 text-amber-400 flex items-center justify-center text-lg"><i class="fa-solid fa-cube"></i></div>
        <h3 class="text-base font-extrabold text-white">عرض 2D و 3D تفاعلي</h3>
        <p class="text-xs text-slate-400 leading-relaxed">انتقل بضغطة واحدة بين الرؤية العلوية الكلاسيكية والمنظور الثلاثي الأبعاد 3D بـ 5 ثيمات ملاعب عالمية منها ثيم Opta و Midnight الذهبي.</p>
      </div>

      <div class="bg-slate-900/80 border border-slate-800 hover:border-amber-500/40 rounded-2xl p-5 space-y-2.5 transition">
        <div class="w-10 h-10 rounded-xl bg-emerald-500/15 text-emerald-400 flex items-center justify-center text-lg"><i class="fa-solid fa-film"></i></div>
        <h3 class="text-base font-extrabold text-white">تحريك الإطارات وتصدير الفيديو</h3>
        <p class="text-xs text-slate-400 leading-relaxed">أنشئ سيناريو متكامل من عدة إطارات (Keyframes) مع تتبع مسارات الحركة تلقائياً وتصدير المحاضرة كملف فيديو جاهز للعرض.</p>
      </div>

      <div class="bg-slate-900/80 border border-slate-800 hover:border-amber-500/40 rounded-2xl p-5 space-y-2.5 transition">
        <div class="w-10 h-10 rounded-xl bg-sky-500/15 text-sky-400 flex items-center justify-center text-lg"><i class="fa-solid fa-ruler-combined"></i></div>
        <h3 class="text-base font-extrabold text-white">قياسات تكتيكية حية</h3>
        <p class="text-xs text-slate-400 leading-relaxed">احسب أطوال وعرض خطوط الفريق (Compactness)، المسافات بالأمتار بين اللاعبين، خط التسلل المتحرك، ومخاريط الرؤية والظل الدفاعي.</p>
      </div>
    </div>
  </section>

  <!-- قسم الباقات (Pricing) -->
  <section id="pricing" class="max-w-4xl mx-auto px-4 md:px-8 py-12 border-t border-slate-800/80">
    <div class="text-center mb-8">
      <h2 class="text-2xl md:text-3xl font-black text-white">اختر الباقة المناسبة لعملك</h2>
      <p class="text-xs md:text-sm text-slate-400 mt-1">ابدأ مجاناً أو فعّل باقة المحترفين للحصول على كامل الصلاحيات</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between space-y-5">
        <div class="space-y-3">
          <div class="text-xs font-bold text-slate-400">للتجربة والاستخدام الأساسي</div>
          <div class="text-2xl font-black text-white">الباقة المجانية (Free)</div>
          <ul class="space-y-2 text-xs text-slate-300 pt-2">
            <li>✔ جميع أدوات الرسم والتشكيلات ووضع 3D</li>
            <li>✔ مكتبة الكرات الثابتة الجاهزة</li>
            <li>✔ حفظ خطة واحدة على السحابة</li>
            <li>✔ تصدير صور عالية الجودة PNG</li>
            <li class="text-slate-500">✖ تصدير الفيديو غير متاح</li>
          </ul>
        </div>
        <button onclick="openAuthFromLanding('signup')" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs py-3 rounded-xl transition">
          إنشاء حساب مجاني
        </button>
      </div>

      <div class="bg-gradient-to-b from-amber-950/30 to-slate-900 border-2 border-amber-500/70 rounded-2xl p-6 flex flex-col justify-between space-y-5 relative gold-glow">
        <span class="absolute -top-3 left-5 bg-amber-400 text-slate-950 text-[10px] font-black px-3 py-0.5 rounded-full">الأكثر طلباً للمحللين</span>
        <div class="space-y-3">
          <div class="text-xs font-bold text-amber-400">للمحللين والمدربين المحترفين</div>
          <div class="text-2xl font-black text-white">باقة المحترفين (PRO)</div>
          <ul class="space-y-2 text-xs text-slate-200 pt-2">
            <li>✔ <b>حفظ سحابي غير محدود</b> لجميع خططك</li>
            <li>✔ <b>تصدير فيديو كامل</b> للتحريك التكتيكي</li>
            <li>✔ تخصيص شعارات وأطقم الفرق بالكامل</li>
            <li>✔ أولوية الدعم الفني والتحديثات المستمرة</li>
          </ul>
        </div>
        <button onclick="requestProViaWhatsApp()" class="w-full bg-gradient-to-r from-amber-400 to-yellow-500 hover:from-amber-300 hover:to-yellow-400 text-slate-950 font-black text-xs py-3 rounded-xl shadow-lg transition flex items-center justify-center gap-2">
          <i class="fa-brands fa-whatsapp text-base"></i> اشترك في باقة PRO الآن
        </button>
      </div>
    </div>
  </section>

  <!-- تذييل الصفحة (Footer) -->
  <footer class="border-t border-slate-800/80 py-6 px-4 text-center text-xs text-slate-500">
    جميع الحقوق محفوظة © <span class="text-amber-400 font-en font-bold">TootScouting</span> — تطوير وتصميم لمحللي الأداء في كرة القدم
  </footer>
</div>

<!-- ================= 2. شاشة تسجيل الدخول وإنشاء الحساب ================= -->
<div id="auth-overlay" class="hidden fixed inset-0 z-[100] bg-[#070b14]/95 backdrop-blur-md flex items-center justify-center p-4">
  <div class="bg-[#111827] border border-slate-800 rounded-2xl w-full max-w-sm p-6 shadow-2xl space-y-4 relative">
    <button onclick="backToLanding()" class="text-[11px] text-slate-400 hover:text-amber-400 flex items-center gap-1 transition">
      <i class="fa-solid fa-arrow-right"></i> العودة للصفحة الرئيسية
    </button>

    <div class="text-center space-y-1">
      <div class="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xl mb-1">
        <i class="fa-solid fa-futbol"></i>
      </div>
      <h2 class="text-lg font-extrabold text-white tracking-wide">ProTactics <span class="text-amber-400">3D PRO</span></h2>
      <p class="text-[11px] text-slate-400 font-semibold">TootScouting • منصة تحليل الأداء والتخطيط التكتيكي</p>
    </div>

    <div class="grid grid-cols-2 gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs font-bold">
      <button type="button" id="tab-login" onclick="switchAuthMode('login')" class="bg-amber-500 text-slate-950 py-1.5 rounded-lg transition">تسجيل الدخول</button>
      <button type="button" id="tab-signup" onclick="switchAuthMode('signup')" class="text-slate-400 hover:text-white py-1.5 rounded-lg transition">حساب جديد</button>
    </div>

    <form id="auth-form" onsubmit="handleSupabaseAuth(event)" class="space-y-3">
      <div id="name-field" class="hidden">
        <label class="block text-[11px] text-slate-300 mb-1">الاسم الكامل (أو اسم المحلل / النادي)</label>
        <input type="text" id="auth-name" placeholder="مثال: كابتن محمود سالم" class="w-full bg-slate-950 border border-slate-700 focus:border-amber-400 rounded-xl px-3 py-2 text-xs text-white outline-none">
      </div>
      <div>
        <label class="block text-[11px] text-slate-300 mb-1">البريد الإلكتروني</label>
        <input type="email" id="auth-email" required placeholder="analyst@tootscouting.com" class="w-full bg-slate-950 border border-slate-700 focus:border-amber-400 rounded-xl px-3 py-2 text-xs text-white outline-none font-en text-left" dir="ltr">
      </div>
      <div>
        <label class="block text-[11px] text-slate-300 mb-1">كلمة المرور</label>
        <input type="password" id="auth-pass" required minlength="6" placeholder="••••••••" class="w-full bg-slate-950 border border-slate-700 focus:border-amber-400 rounded-xl px-3 py-2 text-xs text-white outline-none font-en text-left" dir="ltr">
      </div>
      <div id="auth-msg" class="hidden text-[11px] text-rose-400 bg-rose-950/60 border border-rose-800 rounded-lg px-2.5 py-1.5 text-center"></div>
      <button type="submit" id="auth-submit-btn" class="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-extrabold text-xs py-2.5 rounded-xl shadow-lg transition">
        دخول إلى غرفة التحليل 🔓
      </button>
    </form>

    <div class="pt-2 border-t border-slate-800/80 text-center text-[10px] text-slate-500">
      حماية الجلسة الواحدة مفعّلة • مدعوم بواسطة <span class="text-amber-400 font-en font-bold">TootScouting</span>
    </div>
  </div>
</div>

<!-- ================= 3. شريط التحكم العلوي للسبورة ================= -->
<header class="bg-[#0f172a] border-b border-slate-800 px-3 py-1.5 flex flex-wrap items-center justify-between gap-2 shrink-0 z-20">
  <div class="flex items-center gap-2">
    <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-amber-400 to-yellow-600 flex items-center justify-center text-slate-950 font-bold text-xs shadow">
      <i class="fa-solid fa-futbol"></i>
    </div>
    <div>
      <h1 class="text-xs font-extrabold tracking-wide text-white leading-none">
        ProTactics <span class="text-amber-400">3D PRO</span>
      </h1>
      <span class="text-[9px] text-slate-400 font-en font-semibold">TootScouting</span>
    </div>
    <span id="user-badge" class="hidden text-[10px] bg-slate-800 border border-slate-700 text-slate-200 px-2 py-0.5 rounded-full font-semibold"></span>
    <button onclick="openUpgradeModal()" id="btn-upgrade-nav" class="bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-extrabold text-[11px] px-2.5 py-1 rounded-lg shadow transition">⭐ ترقية لـ PRO</button>
  </div>

  <div class="flex flex-wrap items-center gap-1.5">
    <select id="setpiece-select" onchange="loadSetPiece(this.value)" class="bg-amber-950/80 border border-amber-600 text-amber-300 text-[11px] font-bold px-2 py-1 rounded-lg">
      <option value="">⚡ مكتبة التكتيكات...</option>
      <option value="corner_att">ركنية هجومية</option>
      <option value="fk_direct">ضربة حرة</option>
      <option value="gk_buildup">بناء اللعب</option>
      <option value="high_press">ضغط عالي</option>
      <option value="counter_att">هجمة مرتدة</option>
      <option value="rondo_drill">تمرين Rondo</option>
    </select>

    <button onclick="openLineupModal()" class="bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg">التشكيلات</button>
    <button onclick="toggle3D()" id="btn-toggle-3d" class="tool-btn bg-slate-800 border border-slate-700 text-amber-300 text-[11px] font-bold px-2.5 py-1 rounded-lg">3D</button>

    <select id="pitch-theme-select" onchange="setPitchTheme(this.value)" class="bg-slate-800 border border-slate-700 text-slate-200 text-[11px] px-2 py-1 rounded-lg">
      <option value="green">أخضر</option>
      <option value="classic">كلاسيك</option>
      <option value="navy">كحلي</option>
      <option value="midnight">ذهبي داكن</option>
      <option value="opta">Opta أبيض</option>
    </select>

    <div class="flex bg-slate-900 p-0.5 rounded-lg border border-slate-800 text-[11px]">
      <button onclick="setPitchMode('full')" id="btn-pitch-full" class="pitch-mode-btn bg-slate-700 text-white px-2 py-0.5 rounded">كامل</button>
      <button onclick="setPitchMode('half')" id="btn-pitch-half" class="pitch-mode-btn text-slate-400 px-2 py-0.5 rounded">نصف</button>
    </div>

    <button onclick="toggleZones()" id="btn-toggle-zones" class="tool-btn bg-slate-800 border border-slate-700 text-slate-300 text-[11px] px-2 py-1 rounded-lg">الممرات</button>
    <button onclick="toggleOffside()" id="btn-toggle-offside" class="tool-btn bg-slate-800 border border-slate-700 text-rose-300 text-[11px] px-2 py-1 rounded-lg">تسلل</button>
    <button onclick="toggleCompactness()" id="btn-toggle-compact" class="tool-btn bg-slate-800 border border-slate-700 text-emerald-300 text-[11px] px-2 py-1 rounded-lg">الخطوط</button>
    <button onclick="toggleTrails()" id="btn-toggle-trails" class="tool-btn active bg-slate-800 border border-slate-700 text-sky-300 text-[11px] px-2 py-1 rounded-lg">المسارات</button>
    <button onclick="toggleNotesPanel()" id="btn-toggle-notes" class="tool-btn bg-slate-800 border border-slate-700 text-slate-300 text-[11px] px-2 py-1 rounded-lg">ملاحظات</button>
  </div>

  <div class="flex items-center gap-1">
    <button onclick="undoAction()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] px-2 py-1 rounded-lg"><i class="fa-solid fa-rotate-left"></i></button>
    <button onclick="clearDrawings()" class="bg-slate-800 hover:bg-slate-700 text-amber-300 text-[11px] px-2 py-1 rounded-lg">مسح</button>
    <button onclick="resetBoard()" class="bg-slate-800 hover:bg-slate-700 text-red-400 text-[11px] px-2 py-1 rounded-lg">إعادة</button>
    <button onclick="openCloudModal()" class="bg-amber-600 hover:bg-amber-500 text-slate-950 font-extrabold text-[11px] px-2.5 py-1 rounded-lg flex items-center gap-1"><i class="fa-solid fa-cloud"></i> خططي</button>
    <button onclick="exportJSON()" class="bg-slate-800 hover:bg-slate-700 text-cyan-300 text-[11px] px-2 py-1 rounded-lg">JSON</button>
    <label class="bg-slate-800 hover:bg-slate-700 text-cyan-300 text-[11px] px-2 py-1 rounded-lg cursor-pointer">فتح<input type="file" accept=".json" onchange="importJSON(event)" class="hidden"></label>
    <button onclick="exportVideo()" id="btn-export-video" class="bg-purple-600 hover:bg-purple-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg">فيديو</button>
    <button onclick="exportPNG()" class="bg-emerald-600 hover:bg-emerald-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg">PNG</button>
    <button onclick="logoutSession()" title="تسجيل الخروج" class="bg-rose-950 hover:bg-rose-900 border border-rose-800 text-rose-300 text-[11px] px-2 py-1 rounded-lg"><i class="fa-solid fa-right-from-bracket"></i></button>
  </div>
</header>

<div class="flex flex-1 overflow-hidden">
  <!-- الشريط الجانبي للأدوات -->
  <aside class="bg-[#111827] border-l border-slate-800 p-2 flex flex-col gap-1.5 w-52 shrink-0 overflow-y-auto">
    <div class="text-[10px] font-bold text-slate-400">أدوات الرسم والربط</div>
