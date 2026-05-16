"""Inline HTML dashboard for the SOCKS5 auth relay web UI."""

_WEB_INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>SOCKS5 relay · live traffic</title>
<script>
  // Apply saved theme before first paint to avoid flash.
  (function(){try{var t=localStorage.getItem("s5theme")||"dark";
    var p=localStorage.getItem("s5palette")||"aurora";
    document.documentElement.setAttribute("data-theme",t);
    document.documentElement.setAttribute("data-accent",p);}catch(e){}})();
</script>
<style>
:root{
  --bg:#07090d; --panel:#131822; --panel2:#1a2030; --border:#262d3d;
  --border-soft:rgba(255,255,255,.06);
  --text:#e6edf3; --muted:#8b949e; --dim:#6e7681;
  --up:#ff9650; --down:#5ac8fa; --accent:#d2a0ff;
  --good:#96dc82; --warn:#f0c864; --bad:#f07878;
  --bg-glow-a:rgba(90,200,250,.14); --bg-glow-b:rgba(255,150,80,.10); --bg-glow-c:rgba(210,160,255,.10);
  --orb-a-solid:#5ac8fa; --orb-b-solid:#d2a0ff; --orb-c-solid:#ff9650;
  --title-grad-start:#ffffff; --title-grad-end:#b8c7d9;
  --sh-sm:0 1px 2px rgba(0,0,0,.4);
  --sh-md:0 8px 24px -6px rgba(0,0,0,.55),0 2px 8px rgba(0,0,0,.35);
  --sh-lg:0 24px 60px -12px rgba(0,0,0,.6),0 8px 20px -4px rgba(0,0,0,.4);
  --sh-inset:inset 0 1px 0 rgba(255,255,255,.05),inset 0 0 0 1px rgba(255,255,255,.02);
  --glow-accent:0 0 24px rgba(210,160,255,.25);
  --glow-down:0 0 24px rgba(90,200,250,.28);
  --glow-good:0 0 24px rgba(150,220,130,.28);
  --glow-bad:0 0 24px rgba(240,120,120,.28);
  --font:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Consolas,monospace;
}
html[data-theme="light"]{
  --bg:#f4f6fb; --panel:#ffffff; --panel2:#f7f9fd; --border:#dfe4ef;
  --border-soft:rgba(0,0,0,.05);
  --text:#141a26; --muted:#5a6478; --dim:#8592a8;
  --up:#e07030; --down:#1e8ac8; --accent:#7a4ec0;
  --good:#3da85a; --warn:#c08a1a; --bad:#c5453e;
  --bg-glow-a:rgba(90,200,250,.10); --bg-glow-b:rgba(255,150,80,.07); --bg-glow-c:rgba(210,160,255,.08);
  --orb-a-solid:#6ccbf6; --orb-b-solid:#b994f1; --orb-c-solid:#ffac6d;
  --title-grad-start:#141a26; --title-grad-end:#4a5468;
  --sh-sm:0 1px 2px rgba(20,26,38,.06);
  --sh-md:0 8px 24px -8px rgba(20,26,38,.14),0 2px 6px rgba(20,26,38,.05);
  --sh-lg:0 20px 50px -14px rgba(20,26,38,.18),0 6px 14px -4px rgba(20,26,38,.08);
  --sh-inset:inset 0 1px 0 rgba(255,255,255,.8),inset 0 0 0 1px rgba(0,0,0,.02);
  --glow-accent:0 0 18px rgba(122,78,192,.12);
  --glow-down:0 0 18px rgba(30,138,200,.15);
  --glow-good:0 0 18px rgba(61,168,90,.18);
  --glow-bad:0 0 18px rgba(197,69,62,.18);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:var(--font);
  font-feature-settings:"cv11","ss01","ss03","cv02";-webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility}
body{min-height:100vh;position:relative;overflow-x:hidden;background:
  radial-gradient(1400px 700px at 8% -12%,var(--bg-glow-a),transparent 55%),
  radial-gradient(1100px 600px at 110% 8%,var(--bg-glow-b),transparent 55%),
  radial-gradient(900px 600px at 50% 120%,var(--bg-glow-c),transparent 60%),
  var(--bg);
  padding:24px}
html[data-theme="light"] body{background:
  radial-gradient(1400px 700px at 8% -12%,var(--bg-glow-a),transparent 55%),
  radial-gradient(1100px 600px at 110% 8%,var(--bg-glow-b),transparent 55%),
  radial-gradient(900px 600px at 50% 120%,var(--bg-glow-c),transparent 60%),
  var(--bg)}
html[data-theme="light"] .orbs{opacity:.25;filter:blur(100px)}
html[data-accent="ocean"]{
  --up:#55d6ff; --down:#38bdf8; --accent:#7dd3fc; --good:#4ade80; --warn:#facc15; --bad:#fb7185;
  --bg-glow-a:rgba(56,189,248,.18); --bg-glow-b:rgba(125,211,252,.12); --bg-glow-c:rgba(34,211,238,.10);
  --orb-a-solid:#38bdf8; --orb-b-solid:#7dd3fc; --orb-c-solid:#22d3ee;
  --title-grad-start:#ecfeff; --title-grad-end:#bae6fd;
  --glow-accent:0 0 22px rgba(125,211,252,.28); --glow-down:0 0 24px rgba(56,189,248,.28);
}
html[data-theme="light"][data-accent="ocean"]{
  --title-grad-start:#082f49; --title-grad-end:#0369a1;
  --bg-glow-a:rgba(56,189,248,.12); --bg-glow-b:rgba(125,211,252,.10); --bg-glow-c:rgba(34,211,238,.08);
}
html[data-accent="emerald"]{
  --up:#fbbf24; --down:#34d399; --accent:#10b981; --good:#22c55e; --warn:#f59e0b; --bad:#f87171;
  --bg-glow-a:rgba(52,211,153,.18); --bg-glow-b:rgba(251,191,36,.10); --bg-glow-c:rgba(16,185,129,.12);
  --orb-a-solid:#34d399; --orb-b-solid:#10b981; --orb-c-solid:#fbbf24;
  --title-grad-start:#ecfdf5; --title-grad-end:#a7f3d0;
  --glow-accent:0 0 22px rgba(16,185,129,.24); --glow-down:0 0 24px rgba(52,211,153,.26);
}
html[data-theme="light"][data-accent="emerald"]{
  --title-grad-start:#052e16; --title-grad-end:#047857;
  --bg-glow-a:rgba(52,211,153,.10); --bg-glow-b:rgba(251,191,36,.08); --bg-glow-c:rgba(16,185,129,.08);
}
html[data-accent="sunset"]{
  --up:#fb923c; --down:#f472b6; --accent:#a78bfa; --good:#86efac; --warn:#fbbf24; --bad:#fb7185;
  --bg-glow-a:rgba(251,146,60,.18); --bg-glow-b:rgba(244,114,182,.12); --bg-glow-c:rgba(167,139,250,.12);
  --orb-a-solid:#fb923c; --orb-b-solid:#f472b6; --orb-c-solid:#a78bfa;
  --title-grad-start:#fff7ed; --title-grad-end:#fbcfe8;
  --glow-accent:0 0 22px rgba(167,139,250,.26); --glow-down:0 0 24px rgba(244,114,182,.24);
}
html[data-theme="light"][data-accent="sunset"]{
  --title-grad-start:#431407; --title-grad-end:#9d174d;
  --bg-glow-a:rgba(251,146,60,.10); --bg-glow-b:rgba(244,114,182,.08); --bg-glow-c:rgba(167,139,250,.08);
}
html[data-accent="rose"]{
  --up:#fb7185; --down:#2dd4bf; --accent:#f472b6; --good:#4ade80; --warn:#facc15; --bad:#ef4444;
  --bg-glow-a:rgba(244,114,182,.16); --bg-glow-b:rgba(45,212,191,.12); --bg-glow-c:rgba(251,113,133,.12);
  --orb-a-solid:#f472b6; --orb-b-solid:#2dd4bf; --orb-c-solid:#fb7185;
  --title-grad-start:#fff1f2; --title-grad-end:#fbcfe8;
  --glow-accent:0 0 22px rgba(244,114,182,.26); --glow-down:0 0 24px rgba(45,212,191,.24);
}
html[data-theme="light"][data-accent="rose"]{
  --title-grad-start:#4a044e; --title-grad-end:#be185d;
  --bg-glow-a:rgba(244,114,182,.10); --bg-glow-b:rgba(45,212,191,.08); --bg-glow-c:rgba(251,113,133,.08);
}
/* ---- light-theme overrides for hard-coded dark surfaces ----------- */
html[data-theme="light"] .title h1{background:linear-gradient(135deg,var(--title-grad-start),var(--title-grad-end));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
html[data-theme="light"] input[type="number"],
html[data-theme="light"] input[type="text"],
html[data-theme="light"] input[type="password"]{
  background:#ffffff;border-color:var(--border);color:var(--text);
  box-shadow:inset 0 1px 2px rgba(20,26,38,.06);-moz-appearance:textfield}
html[data-theme="light"] input[type="number"]::-webkit-inner-spin-button,
html[data-theme="light"] input[type="number"]::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
html[data-theme="light"] input[type="number"]:focus,
html[data-theme="light"] input[type="text"]:focus,
html[data-theme="light"] input[type="password"]:focus{
  border-color:var(--down);box-shadow:inset 0 1px 2px rgba(20,26,38,.06),0 0 0 3px rgba(30,138,200,.18)}
html[data-theme="light"] .btn{
  background:linear-gradient(180deg,#ffffff,#f0f3f9);color:var(--text);
  border-color:var(--border);box-shadow:var(--sh-sm),var(--sh-inset)}
html[data-theme="light"] .btn:hover{color:var(--down);border-color:var(--down);
  box-shadow:var(--sh-md),0 0 12px rgba(30,138,200,.12)}
html[data-theme="light"] .btn.primary{
  background:linear-gradient(180deg,#2a95d0,#1877b0);color:#fff;
  border-color:rgba(30,138,200,.55);box-shadow:var(--sh-md),0 0 12px rgba(30,138,200,.18)}
html[data-theme="light"] .btn.primary:hover{color:#fff}
html[data-theme="light"] .btn.danger{
  background:linear-gradient(180deg,#fff1f0,#ffe2e0);color:var(--bad);
  border-color:rgba(197,69,62,.3)}
html[data-theme="light"] .btn.danger:hover{
  background:linear-gradient(180deg,#ffe2e0,#ffcbc7);color:var(--bad);
  border-color:var(--bad);box-shadow:var(--sh-md),var(--glow-bad)}
html[data-theme="light"] .btn.ghost{background:transparent;border-color:var(--border)}
html[data-theme="light"] .toggle{
  background:#e4e8f0;border-color:#cdd3df;
  box-shadow:inset 0 1px 2px rgba(20,26,38,.1)}
html[data-theme="light"] .toggle::after{background:#ffffff;
  box-shadow:0 1px 3px rgba(20,26,38,.2),0 0 0 1px rgba(20,26,38,.04)}
html[data-theme="light"] .toggle.on{background:linear-gradient(90deg,#c6e3f3,#8bc9e6);
  border-color:var(--down);box-shadow:inset 0 1px 2px rgba(20,26,38,.08),var(--glow-down)}
html[data-theme="light"] .toggle.ok{background:linear-gradient(90deg,#d1ecd6,#a6dcb1);
  border-color:var(--good);box-shadow:inset 0 1px 2px rgba(20,26,38,.08),var(--glow-good)}
html[data-theme="light"] .toggle.danger{background:linear-gradient(90deg,#f6d1cf,#eca8a3);
  border-color:var(--bad);box-shadow:inset 0 1px 2px rgba(20,26,38,.08),var(--glow-bad)}
html[data-theme="light"] .preset{background:#ffffff}
html[data-theme="light"] .preset:hover{border-color:#b5bdcd}
html[data-theme="light"] .preset.on{
  background:linear-gradient(180deg,rgba(122,78,192,.08),rgba(122,78,192,.02));
  border-color:rgba(122,78,192,.45)}
html[data-theme="light"] .preset .name .ic{
  background:linear-gradient(180deg,#eef1f7,#e2e7f0);color:var(--muted)}
html[data-theme="light"] .preset.on .name .ic{
  background:linear-gradient(180deg,rgba(122,78,192,.18),rgba(122,78,192,.06));color:var(--accent)}
html[data-theme="light"] .preset .cnt{background:rgba(20,26,38,.05)}
html[data-theme="light"] .limit-progress{background:#e4e8f0;border-color:#cdd3df;
  box-shadow:inset 0 1px 2px rgba(20,26,38,.1)}
html[data-theme="light"] .pill{background:#ffffff;color:var(--muted)}
html[data-theme="light"] ::-webkit-scrollbar-thumb{background:#cdd3df;border-color:var(--bg)}
html[data-theme="light"] ::-webkit-scrollbar-thumb:hover{background:#a9b1c2}
html[data-theme="light"] ::selection{background:rgba(122,78,192,.25);color:#141a26}
html[data-theme="light"] canvas{background:#ffffff !important;border-color:var(--border)}
html[data-theme="light"] .bar{background:#e4e8f0}
html[data-theme="light"] .ev{background:#ffffff;color:var(--muted)}
html[data-theme="light"] .ev b{color:var(--text)}
html[data-theme="light"] .dot.off{background:#b5bdcd}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);
  background-size:44px 44px;
  mask-image:radial-gradient(ellipse at 50% 30%,#000 30%,transparent 75%);
  -webkit-mask-image:radial-gradient(ellipse at 50% 30%,#000 30%,transparent 75%)}
.orbs{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;filter:blur(80px);opacity:.55}
.orb{position:absolute;width:420px;height:420px;border-radius:50%;mix-blend-mode:screen}
.orb.a{background:radial-gradient(circle,var(--orb-a-solid) 0%,transparent 70%);top:-120px;left:-80px;animation:float1 18s ease-in-out infinite}
.orb.b{background:radial-gradient(circle,var(--orb-b-solid) 0%,transparent 70%);bottom:-150px;right:-100px;animation:float2 22s ease-in-out infinite}
.orb.c{background:radial-gradient(circle,var(--orb-c-solid) 0%,transparent 70%);top:40%;left:60%;width:320px;height:320px;animation:float3 26s ease-in-out infinite}
@keyframes float1{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(80px,60px) scale(1.1)}}
@keyframes float2{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-100px,-70px) scale(1.15)}}
@keyframes float3{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-60px,80px) scale(.9)}}
.wrap{position:relative;z-index:1}
.wrap{max-width:1200px;margin:0 auto}
header{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.title{display:flex;align-items:center;gap:14px}
.title .logo{position:relative;width:42px;height:42px;border-radius:12px;
  background:linear-gradient(135deg,rgba(90,200,250,.28),rgba(210,160,255,.28));
  display:grid;place-items:center;border:1px solid rgba(210,160,255,.35);color:#fff;
  box-shadow:var(--glow-accent),var(--sh-inset),var(--sh-md)}
.title .logo::after{content:"";position:absolute;inset:-2px;border-radius:14px;padding:2px;
  background:conic-gradient(from 0deg,rgba(90,200,250,.6),rgba(210,160,255,.6),rgba(255,150,80,.6),rgba(90,200,250,.6));
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;opacity:.4;animation:spin 8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.title h1{margin:0;font-size:18px;letter-spacing:.3px;background:linear-gradient(135deg,var(--title-grad-start),var(--title-grad-end));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.header-actions{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-left:auto}
.theme-tools{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end}
.theme-swatches{display:flex;align-items:center;gap:6px;flex-wrap:wrap;padding:6px 8px;border-radius:999px;
  border:1px solid var(--border);background:linear-gradient(180deg,rgba(255,255,255,.03),transparent),var(--panel);
  box-shadow:var(--sh-sm),var(--sh-inset);backdrop-filter:blur(8px)}
.theme-swatch{position:relative;width:18px;height:18px;border-radius:999px;border:1px solid rgba(255,255,255,.16);cursor:pointer;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 2px 8px rgba(0,0,0,.28);transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}
.theme-swatch:hover{transform:translateY(-1px) scale(1.06)}
.theme-swatch.active{border-color:var(--text);box-shadow:0 0 0 2px rgba(255,255,255,.06),0 0 0 4px rgba(90,200,250,.18),0 4px 14px rgba(0,0,0,.28)}
.theme-swatch::after{content:"";position:absolute;inset:3px;border-radius:999px;background:rgba(255,255,255,.18);opacity:0;transition:opacity .18s ease}
.theme-swatch.active::after{opacity:1}
.theme-swatch.aurora{background:linear-gradient(135deg,#5ac8fa,#d2a0ff,#ff9650)}
.theme-swatch.ocean{background:linear-gradient(135deg,#38bdf8,#7dd3fc,#22d3ee)}
.theme-swatch.emerald{background:linear-gradient(135deg,#34d399,#10b981,#fbbf24)}
.theme-swatch.sunset{background:linear-gradient(135deg,#fb923c,#f472b6,#a78bfa)}
.theme-swatch.rose{background:linear-gradient(135deg,#f472b6,#2dd4bf,#fb7185)}
.theme-mode-label{font-size:11px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}
.title .sub{color:var(--muted);font-size:12px;margin-top:2px}
.pill{display:inline-flex;align-items:center;gap:8px;font-size:12px;padding:7px 12px;
  border:1px solid var(--border);border-radius:999px;color:var(--muted);
  background:linear-gradient(180deg,rgba(255,255,255,.03),transparent),var(--panel);
  box-shadow:var(--sh-sm),var(--sh-inset);backdrop-filter:blur(8px)}
.pill .dot{width:8px;height:8px;border-radius:50%;background:var(--good);box-shadow:0 0 10px var(--good),0 0 20px rgba(150,220,130,.4);animation:pulse 2s ease-in-out infinite}
.pill.bad .dot{background:var(--bad);box-shadow:0 0 10px var(--bad),0 0 20px rgba(240,120,120,.4)}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.6;transform:scale(.9)}}

.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:18px}
.card{position:relative;background:linear-gradient(180deg,var(--panel),var(--panel2));
  border:1px solid var(--border);border-radius:16px;padding:18px;
  box-shadow:var(--sh-md),var(--sh-inset);
  backdrop-filter:blur(10px) saturate(140%);
  -webkit-backdrop-filter:blur(10px) saturate(140%);
  transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease}
.card::before{content:"";position:absolute;inset:0;border-radius:16px;pointer-events:none;
  background:radial-gradient(600px 200px at var(--mx,50%) var(--my,0%),rgba(255,255,255,.06),transparent 45%);
  opacity:0;transition:opacity .3s}
.card:hover{transform:translateY(-2px);box-shadow:var(--sh-lg),var(--sh-inset);border-color:#303848}
.card:hover::before{opacity:1}
.card > *{position:relative}
.card h2{margin:0 0 14px;font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);
  display:flex;align-items:center;gap:8px}
.card h2::before{content:"";width:3px;height:12px;border-radius:2px;
  background:linear-gradient(180deg,var(--accent),var(--down));box-shadow:0 0 8px rgba(210,160,255,.5)}
.stat{display:flex;flex-direction:column;gap:6px}
.stat .v{font-family:var(--mono);font-size:24px;font-weight:700;color:var(--text);letter-spacing:-.02em;
  text-shadow:0 2px 16px rgba(0,0,0,.4)}
.stat .v.up{color:var(--up);text-shadow:0 0 24px rgba(255,150,80,.35)}
.stat .v.down{color:var(--down);text-shadow:0 0 24px rgba(90,200,250,.35)}
.stat .v.acc{color:var(--accent);text-shadow:0 0 24px rgba(210,160,255,.35)}
.stat .l{font-size:11px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}
.stat .s{font-family:var(--mono);font-size:12px;color:var(--dim)}
.row{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.up{color:var(--up)} .down{color:var(--down)} .acc{color:var(--accent)}
.good{color:var(--good)} .warn{color:var(--warn)} .bad{color:var(--bad)} .muted{color:var(--muted)}

.span-3{grid-column:span 3} .span-4{grid-column:span 4} .span-6{grid-column:span 6}
.span-8{grid-column:span 8} .span-12{grid-column:span 12}
@media(max-width:900px){.span-3,.span-4,.span-6,.span-8{grid-column:span 12}}

canvas{width:100%;height:220px;display:block;border-radius:10px;background:
  repeating-linear-gradient(0deg,rgba(255,255,255,.02) 0 1px,transparent 1px 40px),
  repeating-linear-gradient(90deg,rgba(255,255,255,.02) 0 1px,transparent 1px 40px),
  radial-gradient(600px 200px at 50% 100%,rgba(90,200,250,.06),transparent 70%),
  #070a10;border:1px solid var(--border);
  box-shadow:inset 0 2px 10px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,255,255,.02)}

table{width:100%;border-collapse:separate;border-spacing:0;font-size:13px}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--border-soft)}
th{font-size:10px;color:var(--muted);letter-spacing:.12em;text-transform:uppercase;font-weight:600;
  background:rgba(255,255,255,.02);position:sticky;top:0;backdrop-filter:blur(6px)}
th:first-child{border-top-left-radius:10px} th:last-child{border-top-right-radius:10px}
tbody tr{transition:background .2s}
tbody tr:hover{background:linear-gradient(90deg,rgba(210,160,255,.05),rgba(90,200,250,.03),transparent)}
tr:last-child td{border-bottom:none}
td.mono{font-family:var(--mono)}
.bar{position:relative;height:6px;background:#070a10;border-radius:4px;overflow:hidden;min-width:80px;
  box-shadow:inset 0 1px 2px rgba(0,0,0,.6)}
.bar > i{position:absolute;inset:0;background:linear-gradient(90deg,var(--accent),var(--down));
  transform-origin:left;transform:scaleX(0);transition:transform .5s cubic-bezier(.4,0,.2,1);
  box-shadow:0 0 10px rgba(210,160,255,.4)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;vertical-align:middle;margin-right:6px}
.dot.on{background:var(--accent);box-shadow:0 0 10px var(--accent),0 0 20px rgba(210,160,255,.4)}
.dot.off{background:#333a44}

.events{display:flex;gap:8px;flex-wrap:wrap}
.ev{padding:7px 12px;border-radius:10px;border:1px solid var(--border);
  background:linear-gradient(180deg,rgba(255,255,255,.02),transparent),#0a0e15;
  font-family:var(--mono);font-size:12px;color:var(--muted);
  box-shadow:var(--sh-sm),var(--sh-inset);transition:transform .15s}
.ev:hover{transform:translateY(-1px)}
.ev b{color:var(--text);margin-right:4px;font-weight:700}
.ev.err b{color:var(--bad);text-shadow:0 0 12px rgba(240,120,120,.5)}
.ev.auth b{color:var(--warn);text-shadow:0 0 12px rgba(240,200,100,.5)}
.ev.ref b{color:var(--accent);text-shadow:0 0 12px rgba(210,160,255,.5)}

footer{margin-top:24px;padding:16px;color:var(--dim);font-size:11px;text-align:center;font-family:var(--mono);
  border-top:1px solid var(--border-soft)}
.legend{display:inline-flex;align-items:center;gap:6px;margin-left:12px;font-size:11px;color:var(--muted)}
.legend .sw{width:10px;height:10px;border-radius:3px;box-shadow:0 0 8px currentColor}
.sw.up{background:var(--up);color:var(--up)} .sw.down{background:var(--down);color:var(--down)}
svg{display:block}
::selection{background:rgba(210,160,255,.3);color:#fff}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:10px;border:2px solid var(--bg)}
::-webkit-scrollbar-thumb:hover{background:#3a4458}

/* ---- controls panel ------------------------------------------------- */
.ctrl{display:flex;flex-direction:column;gap:12px}
.ctrl-row{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.ctrl-row .lbl{font-size:13px}
.ctrl-row .lbl small{display:block;color:var(--muted);font-size:11px;margin-top:2px}
.toggle{--sz:22px;position:relative;width:44px;height:var(--sz);flex:0 0 44px;
  background:#070a10;border:1px solid var(--border);border-radius:999px;cursor:pointer;
  transition:background .25s,border-color .25s,box-shadow .25s;
  box-shadow:inset 0 1px 3px rgba(0,0,0,.6)}
.toggle::after{content:"";position:absolute;top:2px;left:2px;width:calc(var(--sz) - 6px);
  height:calc(var(--sz) - 6px);background:var(--muted);border-radius:50%;transition:all .25s cubic-bezier(.4,0,.2,1);
  box-shadow:0 2px 6px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.2)}
.toggle.on{background:linear-gradient(90deg,#1e3a55,#2a6b88);border-color:var(--down);box-shadow:inset 0 1px 3px rgba(0,0,0,.6),var(--glow-down)}
.toggle.on::after{left:calc(100% - var(--sz) + 4px);background:var(--down);box-shadow:0 0 12px var(--down),0 2px 4px rgba(0,0,0,.4)}
.toggle.ok{background:linear-gradient(90deg,#1e4a2a,#2a7a4e);border-color:var(--good);box-shadow:inset 0 1px 3px rgba(0,0,0,.6),var(--glow-good)}
.toggle.ok::after{left:calc(100% - var(--sz) + 4px);background:var(--good);box-shadow:0 0 12px var(--good),0 2px 4px rgba(0,0,0,.4)}
.toggle.danger{background:linear-gradient(90deg,#5a1e1e,#882a2a);border-color:var(--bad);box-shadow:inset 0 1px 3px rgba(0,0,0,.6),var(--glow-bad)}
.toggle.danger::after{left:calc(100% - var(--sz) + 4px);background:var(--bad);box-shadow:0 0 12px var(--bad),0 2px 4px rgba(0,0,0,.4)}

.presets{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.preset{display:flex;align-items:center;justify-content:space-between;gap:8px;
  padding:11px 13px;border:1px solid var(--border);border-radius:12px;
  background:linear-gradient(180deg,rgba(255,255,255,.02),transparent),#0a0e15;
  box-shadow:var(--sh-sm),var(--sh-inset);cursor:pointer;
  transition:all .2s;position:relative;overflow:hidden}
.preset:hover{transform:translateY(-1px);border-color:#3a4458;box-shadow:var(--sh-md),var(--sh-inset)}
.preset.on{border-color:rgba(210,160,255,.5);background:linear-gradient(180deg,rgba(210,160,255,.12),rgba(210,160,255,.04));
  box-shadow:var(--glow-accent),var(--sh-inset)}
.preset.on::after{content:"";position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--accent),transparent)}
.preset .name{font-size:13px;font-weight:500;display:flex;align-items:center;gap:8px}
.preset .name .ic{width:24px;height:24px;border-radius:7px;display:grid;place-items:center;
  font-size:12px;background:linear-gradient(180deg,#1f2634,#161b27);color:var(--muted);
  box-shadow:var(--sh-inset),0 1px 2px rgba(0,0,0,.4)}
.preset.on .name .ic{color:var(--accent);background:linear-gradient(180deg,rgba(210,160,255,.18),rgba(210,160,255,.06));
  box-shadow:var(--sh-inset),0 0 12px rgba(210,160,255,.25)}
.preset .cnt{font-family:var(--mono);font-size:11px;color:var(--muted);padding:2px 8px;
  background:rgba(255,255,255,.04);border-radius:999px;border:1px solid var(--border-soft)}

.inline-form{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
input[type="number"],input[type="text"],input[type="password"]{background:#070a10;border:1px solid var(--border);border-radius:10px;
  color:var(--text);padding:9px 12px;font-family:var(--mono);font-size:13px;
  outline:none;transition:all .2s;box-shadow:inset 0 1px 3px rgba(0,0,0,.5);
  -moz-appearance:textfield}
input[type="number"]::-webkit-inner-spin-button, 
input[type="number"]::-webkit-outer-spin-button {-webkit-appearance:none;margin:0}
input[type="number"]{width:110px}
input[type="number"]:focus,input[type="text"]:focus,input[type="password"]:focus{border-color:var(--down);box-shadow:inset 0 1px 3px rgba(0,0,0,.5),0 0 0 3px rgba(90,200,250,.15)}
.btn{display:inline-flex;align-items:center;gap:6px;padding:9px 14px;border-radius:10px;
  border:1px solid var(--border);
  background:linear-gradient(180deg,#1a2030,#10151e);color:var(--text);font-size:12px;font-weight:500;cursor:pointer;
  font-family:var(--font);transition:all .2s;
  box-shadow:var(--sh-sm),var(--sh-inset)}
.btn:hover{transform:translateY(-1px);border-color:var(--down);color:var(--down);box-shadow:var(--sh-md),var(--sh-inset),0 0 16px rgba(90,200,250,.15)}
.btn:active{transform:translateY(0)}
.btn.primary{background:linear-gradient(180deg,#3a6b9a,#245a82);border-color:rgba(90,200,250,.5);color:#fff;
  box-shadow:var(--sh-md),var(--sh-inset),var(--glow-down)}
.btn.primary:hover{filter:brightness(1.15);color:#fff}
.btn.danger{border-color:rgba(240,120,120,.35);color:var(--bad);
  background:linear-gradient(180deg,#2a151a,#1a0d11)}
.btn.danger:hover{background:linear-gradient(180deg,#4a2028,#2a1318);border-color:var(--bad);color:var(--bad);box-shadow:var(--sh-md),var(--glow-bad)}
.btn.ghost{background:transparent;border-color:var(--border-soft)}
.btn:disabled{opacity:.4;cursor:not-allowed;transform:none !important;box-shadow:var(--sh-sm) !important}

.limit-progress{height:8px;background:#070a10;border-radius:6px;overflow:hidden;margin-top:6px;border:1px solid var(--border);
  box-shadow:inset 0 1px 3px rgba(0,0,0,.6)}
.limit-progress > i{display:block;height:100%;background:linear-gradient(90deg,var(--good),var(--warn),var(--bad));
  width:0%;transition:width .4s ease;box-shadow:0 0 12px currentColor;
  background-size:200% 100%;animation:shimmer 2.5s linear infinite}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
.bypass-badge{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:999px;
  font-size:10px;font-family:var(--mono);background:linear-gradient(180deg,rgba(210,160,255,.18),rgba(210,160,255,.06));color:var(--accent);
  border:1px solid rgba(210,160,255,.35);box-shadow:0 0 12px rgba(210,160,255,.2),var(--sh-inset)}
.paused-banner{display:none;background:linear-gradient(90deg,rgba(240,200,100,.18),rgba(240,200,100,.04));
  border:1px solid rgba(240,200,100,.45);color:var(--warn);padding:12px 16px;border-radius:12px;
  margin-bottom:18px;font-size:13px;box-shadow:var(--sh-md),0 0 24px rgba(240,200,100,.1)}
.paused-banner.show{display:block;animation:fadein .3s ease}

/* ---- config generator console blocks ------------------------------ */
.cfg-block{margin-top:14px;border:1px solid var(--border);border-radius:12px;
  background:linear-gradient(180deg,rgba(255,255,255,.02),transparent),var(--panel2);
  box-shadow:var(--sh-sm),var(--sh-inset);overflow:hidden}
.cfg-head{display:flex;align-items:center;justify-content:space-between;
  padding:10px 14px;border-bottom:1px solid var(--border);
  background:linear-gradient(180deg,rgba(90,200,250,.06),transparent)}
.cfg-title{font-size:12px;font-weight:600;letter-spacing:.5px;color:var(--down);
  text-transform:uppercase}
.cfg-copy{padding:6px 12px !important;font-size:11px !important}
.cfg-copy.ok{border-color:var(--good) !important;color:var(--good) !important;
  box-shadow:0 0 12px rgba(120,240,180,.25) !important}
pre.console{margin:0;padding:14px 16px;font-family:var(--mono);font-size:12px;
  line-height:1.55;color:#cfe4f5;background:#070a0f;white-space:pre-wrap;word-break:break-all;
  max-height:340px;overflow:auto;text-shadow:0 0 6px rgba(90,200,250,.08)}
pre.console::-webkit-scrollbar{width:10px;height:10px}
pre.console::-webkit-scrollbar-track{background:#050709}
pre.console::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#1b2733,#0d141c);border-radius:8px;border:1px solid var(--border-soft)}

/* ---- tabs ---------------------------------------------------------- */
.tabs{display:flex;gap:4px;margin-bottom:24px;
  background:linear-gradient(180deg,rgba(255,255,255,.02),transparent),var(--panel2);
  padding:6px;border-radius:14px;border:1px solid var(--border);
  box-shadow:var(--sh-md),var(--sh-inset);
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  overflow-x:auto;-webkit-overflow-scrolling:touch}
.tab{flex:1;min-width:max-content;padding:10px 16px;font-size:13px;font-weight:500;color:var(--muted);
  cursor:pointer;border:1px solid transparent;background:transparent;border-radius:10px;
  transition:all .25s cubic-bezier(.4,0,.2,1);font-family:var(--font);display:inline-flex;align-items:center;
  justify-content:center;gap:8px;position:relative}
.tab:hover{color:var(--text);background:rgba(255,255,255,.04)}
.tab.active{color:#fff;
  background:linear-gradient(180deg,rgba(210,160,255,.12),rgba(90,200,250,.08));
  border-color:rgba(210,160,255,.25);
  box-shadow:0 4px 12px rgba(0,0,0,.4),0 0 20px rgba(210,160,255,.15),inset 0 1px 0 rgba(255,255,255,.08)}
.tab.active::after{content:"";position:absolute;bottom:-7px;left:50%;transform:translateX(-50%);
  width:24px;height:2px;border-radius:2px;background:linear-gradient(90deg,var(--accent),var(--down));
  box-shadow:0 0 10px var(--accent)}
.tab .ic{display:flex;opacity:.6;transition:all .25s;color:inherit}
.tab:hover .ic{opacity:.9}
.tab.active .ic{opacity:1;color:var(--accent);filter:drop-shadow(0 0 6px rgba(210,160,255,.6))}
.tab-pane{display:none}
.tab-pane.active{display:block;animation:fadein .3s ease}
@keyframes fadein { from { opacity:0; transform:translateY(4px) } to { opacity:1; transform:translateY(0) } }
.section-label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}

/* ---- UX helpers ---------------------------------------------------- */
.ux-intro{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
.ux-intro .copy{min-width:240px;flex:1}
.ux-intro .title{font-size:14px;font-weight:700;letter-spacing:.01em;color:var(--text);margin:0 0 4px}
.ux-intro .desc{font-size:12px;color:var(--muted);margin:0}
.ux-actions{display:flex;gap:8px;flex-wrap:wrap}
.mini-chip{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;
  border:1px solid var(--border-soft);font-size:11px;color:var(--muted);background:rgba(255,255,255,.03)}
.mini-chip b{font-family:var(--mono);color:var(--text)}
.sys-grid{display:grid;grid-template-columns:repeat(4,minmax(180px,1fr));gap:16px}
.sys-card{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;padding:8px 0}
.sys-ring{--pct:0%;--ring-color:var(--down);width:108px;height:108px;border-radius:50%;position:relative;
  display:grid;place-items:center;background:conic-gradient(var(--ring-color) 0 var(--pct),rgba(255,255,255,.10) var(--pct) 100%);
  box-shadow:var(--sh-sm),inset 0 0 0 1px rgba(255,255,255,.03)}
.sys-ring::before{content:"";position:absolute;inset:9px;border-radius:50%;background:linear-gradient(180deg,var(--panel),var(--panel2));
  box-shadow:inset 0 1px 1px rgba(255,255,255,.05),0 1px 8px rgba(0,0,0,.18)}
.sys-ring .value{position:relative;z-index:1;font-family:var(--mono);font-size:20px;font-weight:700;color:var(--text)}
.sys-card.cpu .sys-ring{--ring-color:var(--down)}
.sys-card.ram .sys-ring{--ring-color:var(--accent)}
.sys-card.swap .sys-ring{--ring-color:var(--warn)}
.sys-card.disk .sys-ring{--ring-color:var(--up)}
.sys-meta{display:flex;flex-direction:column;gap:4px;min-width:120px}
.sys-meta b{font-size:13px;letter-spacing:.02em}
.sys-meta span{font-size:12px;color:var(--muted);font-family:var(--mono)}
@media(max-width:980px){.sys-grid{grid-template-columns:repeat(2,minmax(180px,1fr))}}
@media(max-width:640px){.sys-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="orbs"><div class="orb a"></div><div class="orb b"></div><div class="orb c"></div></div>

<div class="wrap">
  <header>
    <div class="title">
      <div class="logo"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" fill="currentColor" fill-opacity=".2"></polygon></svg></div>
      <div>
        <h1>SOCKS5 relay · live traffic</h1>
        <div class="sub" id="sub">connecting…</div>
      </div>
    </div>
    <div class="header-actions">
      <div class="pill" id="status"><span class="dot"></span><span id="statusText">live</span></div>
      <div class="theme-tools">
        <button class="btn ghost" id="themeBtn" type="button" title="Toggle light / dark theme" style="padding:7px 10px;border-radius:999px">
          <svg id="themeIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          <span class="theme-mode-label" id="themeModeLabel">Dark</span>
        </button>
        <div class="theme-swatches" id="themeSwatches" aria-label="Theme palette selector">
          <button class="theme-swatch aurora" type="button" data-palette="aurora" title="Aurora"></button>
          <button class="theme-swatch ocean" type="button" data-palette="ocean" title="Ocean"></button>
          <button class="theme-swatch emerald" type="button" data-palette="emerald" title="Emerald"></button>
          <button class="theme-swatch sunset" type="button" data-palette="sunset" title="Sunset"></button>
          <button class="theme-swatch rose" type="button" data-palette="rose" title="Rose"></button>
        </div>
      </div>
    </div>
  </header>

  <div class="paused-banner" id="pausedBanner">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;margin-right:6px"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>proxy is paused — new connections are refused until you re-enable it.
  </div>

  <nav class="tabs" role="tablist">
    <button class="tab active" data-tab="overview"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg></span>Overview</button>
    <button class="tab" data-tab="access"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></span>Access &amp; whitelist</button>
    <button class="tab" data-tab="network"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></span>Network &amp; limit</button>
    <button class="tab" data-tab="security"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></span>Security</button>
    <button class="tab" data-tab="hosts"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9"></path><path d="M4 4a16 16 0 0 1 16 16"></path><circle cx="5" cy="19" r="1"></circle></svg></span>Destinations</button>
    <button class="tab" data-tab="clients"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></span>Clients</button>
    <button class="tab" data-tab="configs"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg></span>Configs</button>
  </nav>

  <section class="tab-pane active" id="pane-overview">
    <div class="grid">
      <div class="card span-12">
        <h2>Server resources <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">· live host snapshot</span></h2>
        <div class="sys-grid">
          <div class="sys-card cpu">
            <div class="sys-ring" id="cpuGauge"><span class="value" id="cpuGaugeValue">0%</span></div>
            <div class="sys-meta"><b>CPU</b><span id="cpuMeta">1 core</span></div>
          </div>
          <div class="sys-card ram">
            <div class="sys-ring" id="ramGauge"><span class="value" id="ramGaugeValue">0%</span></div>
            <div class="sys-meta"><b>RAM</b><span id="ramMeta">0 B / 0 B</span></div>
          </div>
          <div class="sys-card swap">
            <div class="sys-ring" id="swapGauge"><span class="value" id="swapGaugeValue">0%</span></div>
            <div class="sys-meta"><b>Swap</b><span id="swapMeta">0 B / 0 B</span></div>
          </div>
          <div class="sys-card disk">
            <div class="sys-ring" id="diskGauge"><span class="value" id="diskGaugeValue">0%</span></div>
            <div class="sys-meta"><b>Storage</b><span id="diskMeta">0 B / 0 B</span></div>
          </div>
        </div>
      </div>

      <div class="card span-12">
        <div class="ux-intro">
          <div class="copy">
            <p class="title">Quick start</p>
            <p class="desc" id="quickGuideText">No traffic yet — start a client connection, then open Destinations or Clients to inspect usage.</p>
          </div>
          <div class="ux-actions">
            <button class="btn" id="goClients">Open clients</button>
            <button class="btn" id="goHosts">Open destinations</button>
            <button class="btn ghost" id="goNetwork">Open network tools</button>
          </div>
        </div>
        <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
          <span class="mini-chip">active tunnels <b id="quickActive">0</b></span>
          <span class="mini-chip">client count <b id="quickClients">0</b></span>
          <span class="mini-chip">last update <b id="quickUpdated">--:--:--</b></span>
        </div>
      </div>

      <div class="card span-3"><h2>Upload</h2>
        <div class="stat"><span class="v up" id="upSpeed">0 B/s</span>
          <span class="s">peak <span id="upPeak">0 B/s</span></span></div></div>
      <div class="card span-3"><h2>Download</h2>
        <div class="stat"><span class="v down" id="downSpeed">0 B/s</span>
          <span class="s">peak <span id="downPeak">0 B/s</span></span></div></div>
      <div class="card span-3"><h2>Active tunnels</h2>
        <div class="stat"><span class="v acc" id="active">0</span>
          <span class="s">peak <span id="peakActive">0</span> · <span id="total">0</span> total · <span id="rate">0.0</span>/s</span></div></div>
      <div class="card span-3"><h2>Uptime</h2>
        <div class="stat"><span class="v" id="uptime">0s</span>
          <span class="s">since start</span></div></div>

      <div class="card span-4">
        <h2>Totals</h2>
        <div class="row"><span class="muted">Live connections</span>
          <span class="v acc" style="font-size:18px" id="tcpConnections">0</span></div>
        <div class="row"><span class="muted">Total</span>
          <span class="v" style="font-size:18px" id="totalBytes">0 B</span></div>
        <div class="row" style="margin-top:8px"><span class="up">↑</span>
          <span class="mono" id="upBytes">0 B</span>
          <span class="muted">avg</span><span class="mono" id="upAvg">0 B/s</span></div>
        <div class="row" style="margin-top:4px"><span class="down">↓</span>
          <span class="mono" id="downBytes">0 B</span>
          <span class="muted">avg</span><span class="mono" id="downAvg">0 B/s</span></div>
        <h2 style="margin-top:16px">Events</h2>
        <div class="events">
          <div class="ev err"><b id="errors">0</b> errors</div>
          <div class="ev auth"><b id="authFail">0</b> auth fail</div>
          <div class="ev ref"><b id="refused">0</b> refused</div>
          <div class="ev"><b id="resets">0</b> resets</div>
        </div>
      </div>

      <div class="card span-8">
        <h2>Throughput
          <span class="legend"><span class="sw up"></span> up</span>
          <span class="legend"><span class="sw down"></span> down</span>
        </h2>
        <canvas id="chart" height="220"></canvas>
      </div>
    </div>
  </section>

  <section class="tab-pane" id="pane-access">
    <div class="grid">
      <div class="card span-6">
        <h2>Proxy &amp; whitelist
          <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">
            · <span class="bypass-badge" id="bypassBadge">bypassed 0</span>
          </span>
        </h2>
        <div class="ctrl">
          <div class="ctrl-row">
            <div class="lbl"><b>Proxy</b><small>Pause / resume all new tunnels</small></div>
            <div class="toggle ok" id="tgProxy"></div>
          </div>
          <div class="ctrl-row">
            <div class="lbl"><b>Whitelist (direct)</b><small>Without strict: matched hosts skip the upstream proxy. With strict: only matched hosts are allowed (still through upstream).</small></div>
            <div class="toggle" id="tgWhitelist"></div>
          </div>
          <div class="ctrl-row">
            <div class="lbl"><b>Strict mode</b><small>Block everything that isn't whitelisted (incl. raw IPs). Allowed hosts go via upstream.</small></div>
            <div class="toggle" id="tgStrict"></div>
          </div>
          <div class="ctrl-row">
            <div class="lbl"><b>Redirect .ir websites</b><small><span style="color:var(--bad);font-weight:600">⚠ Warning:</span> .ir domains connect directly from your real IP, bypassing the upstream proxy. This can leak / expose your real IP address to those sites.</small></div>
            <div class="toggle" id="tgIr"></div>
          </div>
        </div>
      </div>

      <div class="card span-6">
        <h2>Whitelist presets</h2>
        <div class="presets" id="presets">
          <div class="preset" data-name="telegram"><div class="name"><span class="ic"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg></span>Telegram</div>
            <span class="cnt" id="cnt-telegram">0</span></div>
          <div class="preset" data-name="youtube"><div class="name"><span class="ic"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M21.58 7.19c-.23-.86-.9-1.54-1.76-1.77C18.25 5 12 5 12 5s-6.25 0-7.82.42c-.86.23-1.53.91-1.76 1.77C2 8.77 2 12 2 12s0 3.23.42 4.81c.23.86.9 1.54 1.76 1.77C5.75 19 12 19 12 19s6.25 0 7.82-.42c.86-.23 1.53-.91 1.76-1.77C22 15.23 22 12 22 12s0-3.23-.42-4.81zM10 15V9l5 3-5 3z"/></svg></span>YouTube</div>
            <span class="cnt" id="cnt-youtube">0</span></div>
          <div class="preset" data-name="github"><div class="name"><span class="ic"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .3a12 12 0 00-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.4-4-1.4-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.9 1.2 1.9 1.2 1.1 1.9 2.9 1.3 3.6 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 016 0C17.3 4.7 18.3 5 18.3 5c.7 1.7.2 2.9.1 3.2a4.6 4.6 0 011.2 3.2c0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0012 .3"/></svg></span>GitHub</div>
            <span class="cnt" id="cnt-github">0</span></div>
          <div class="preset" data-name="essentials"><div class="name"><span class="ic"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.1 8.3 22 9.3 17 14.1 18.2 21 12 17.8 5.8 21 7 14.1 2 9.3 8.9 8.3 12 2"/></svg></span>Essentials</div>
            <span class="cnt" id="cnt-essentials">0</span></div>
        </div>
        <div class="muted" style="font-size:11px;margin-top:8px">
          Tip: enable the master toggle first, then pick which families to allow.
          Strict mode blocks anything that isn't matched here — matched hosts still go through upstream.
        </div>
      </div>
    </div>
  </section>

  <section class="tab-pane" id="pane-network">
    <div class="grid">
      <div class="card span-6">
        <h2>Listener</h2>
        <div class="muted" style="font-size:12px;margin-bottom:8px">
          Currently listening on <span class="mono" id="listenAddr">…</span>
        </div>
        <div class="section-label">SOCKS port</div>
        <div class="inline-form">
          <input type="number" id="portInput" min="1" max="65535" step="1"/>
          <button class="btn primary" id="portBtn">Apply</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:4px">Rebinds the listener without restart.</div>
        <div class="section-label" style="margin-top:14px">Upstream health</div>
        <div class="inline-form">
          <button class="btn" id="upstreamCheckBtn">Check upstream</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:6px;min-height:16px" id="upstreamCheckStatus">Click to test upstream and detect public IP.</div>
      </div>

      <div class="card span-6">
        <h2>Traffic limit</h2>
        <div class="inline-form">
          <input type="number" id="limitInput" min="0" step="1" placeholder="MB (0=off)"/>
          <button class="btn primary" id="limitBtn">Set</button>
          <button class="btn ghost" id="limitOff">Off</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:6px" id="limitStatus">no limit set</div>
        <div class="limit-progress"><i id="limitBar"></i></div>

        <div class="section-label" style="margin-top:14px">Bandwidth cap</div>
        <div class="inline-form">
          <input type="number" id="bwInput" min="0" step="1" placeholder="KB/s (0=off)"/>
          <button class="btn primary" id="bwBtn">Set</button>
          <button class="btn ghost" id="bwOff">Off</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:4px" id="bwStatus">no bandwidth cap · all tunnels share this limit</div>

        <div class="section-label" style="margin-top:14px">Counters</div>
        <div class="inline-form">
          <button class="btn" id="resetBtn"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>Reset traffic</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:4px">
          Clears totals, peaks, per-host stats.
        </div>
      </div>

      <div class="card span-6">
        <h2>Connection caps</h2>
        <div class="muted" style="font-size:11px;margin-bottom:8px">
          Limit concurrent tunnels. New connects beyond the cap are refused without auth.
        </div>
        <div class="section-label">Global (concurrent tunnels)</div>
        <div class="inline-form">
          <input type="number" id="connTotalInput" min="0" step="1" placeholder="0 = unlimited"/>
          <button class="btn primary" id="connTotalBtn">Set</button>
        </div>
        <div class="section-label" style="margin-top:10px">Per client IP</div>
        <div class="inline-form">
          <input type="number" id="connPerInput" min="0" step="1" placeholder="0 = unlimited"/>
          <button class="btn primary" id="connPerBtn">Set</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:10px" id="connStatus">no caps set</div>
      </div>

      <div class="card span-6">
        <h2>GeoIP lookup</h2>
        <div class="muted" style="font-size:11px;margin-bottom:8px">
          Shows country flag next to each destination in the Destinations tab.
          <b>Leaks visited hostnames to ip-api.com.</b> Off by default.
        </div>
        <div class="ctrl-row">
          <div class="lbl"><b>Enable GeoIP</b><small>Best-effort · results cached · ~45 lookups / min</small></div>
          <div class="toggle" id="tgGeoip"></div>
        </div>
      </div>
    </div>
  </section>

  <section class="tab-pane" id="pane-security">
    <div class="grid">
      <div class="card span-8">
        <h2>SOCKS5 credentials</h2>
        <div class="ctrl-row" style="margin-bottom:12px;padding:10px 12px;
                    background:rgba(240,200,100,.06);border:1px solid rgba(240,200,100,.3);border-radius:10px">
          <div class="lbl">
            <b>Require client authentication</b>
            <small><span style="color:var(--warn);font-weight:600">⚠</span> Turning this OFF lets anyone connect to your relay without a user/pass. Only do this on a trusted LAN.</small>
          </div>
          <div class="toggle ok" id="tgAuth"></div>
        </div>
        <div class="muted" style="font-size:12px;margin-bottom:8px">
          Current user: <span class="mono" id="currentUser">—</span>
          · applying new credentials drops every live tunnel so old clients are forced to re-auth.
        </div>
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:12px;padding:10px 12px;
                    background:rgba(255,255,255,.02);border:1px solid var(--border-soft);border-radius:10px">
          <div style="flex:1;min-width:0">
            <div class="muted" style="font-size:10px;text-transform:uppercase;letter-spacing:.08em;margin-bottom:2px">Live credentials</div>
            <div class="mono" style="font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">
              <span id="credsUser">—</span><span class="muted"> : </span><span id="credsPass">••••••••</span>
            </div>
          </div>
          <button class="btn ghost" id="credsReveal" type="button" title="show/hide current credentials">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            <span id="credsRevealLabel">Show</span>
          </button>
          <button class="btn ghost" id="credsCopy" type="button" title="copy user:pass">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            Copy
          </button>
        </div>
        <div class="inline-form">
          <input type="text" id="userInput" placeholder="username" autocomplete="off" spellcheck="false" style="min-width:180px"/>
          <input type="password" id="passInput" placeholder="new password" autocomplete="new-password" style="min-width:180px"/>
          <button class="btn ghost" id="passReveal" type="button" title="show/hide"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button>
          <button class="btn danger" id="credsBtn"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>Apply &amp; kick clients</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:6px;min-height:16px" id="credsStatus"></div>
      </div>

      <div class="card span-4">
        <h2>Kill switch</h2>
        <div class="muted" style="font-size:12px;margin-bottom:10px">
          Terminates the relay process immediately.
          Every active tunnel drops and the web dashboard goes offline.
        </div>
        <button class="btn danger" id="killBtn"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64A9 9 0 0 1 20.77 15M6.16 6.16a9 9 0 1 0 12.68 12.68"/><line x1="12" y1="2" x2="12" y2="12"/></svg>Kill now</button>
      </div>
    </div>
  </section>

  <section class="tab-pane" id="pane-hosts">
    <div class="card span-12">
      <h2>Top destinations <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">
        · <span id="hostCount">0</span> unique</span></h2>
      <table>
        <thead><tr><th style="width:24px"></th><th>#</th><th>Host</th><th>Share</th>
          <th style="text-align:right">↑ Up</th><th style="text-align:right">↓ Down</th>
          <th style="text-align:right">Conns</th></tr></thead>
        <tbody id="hosts"><tr><td colspan="7" class="muted">no traffic yet</td></tr></tbody>
      </table>
    </div>
  </section>

  <section class="tab-pane" id="pane-clients">
    <div class="card span-12">
      <h2>Connected clients <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">
        · <span id="clientCount">0</span> total</span></h2>
      <table>
        <thead><tr><th style="width:24px"></th><th>#</th><th>IP Address</th>
          <th style="text-align:right">↑ Up</th><th style="text-align:right">↓ Down</th>
          <th style="text-align:right">Active</th><th style="text-align:right">Total</th></tr></thead>
        <tbody id="clients"><tr><td colspan="7" class="muted">no clients yet</td></tr></tbody>
      </table>
    </div>
  </section>

  <section class="tab-pane" id="pane-configs">
    <div class="grid">
      <div class="card span-12">
        <h2>Config generator <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">· V2Ray JSON · Telegram · URI</span></h2>
        <div class="muted" style="font-size:12px;margin-bottom:14px">
          Enter the public IP / hostname that external clients will use to reach this relay,
          plus its port. Username &amp; password are pulled from the running relay automatically —
          the real credentials are embedded in every output.
        </div>
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:12px;margin-bottom:16px">
          <div>
            <label class="muted" style="font-size:11px;display:block;margin-bottom:4px">Public IP / host</label>
            <input type="text" id="cfgHost" placeholder="203.0.113.5 or relay.example.com" />
          </div>
          <div>
            <label class="muted" style="font-size:11px;display:block;margin-bottom:4px">Port</label>
            <input type="number" id="cfgPort" min="1" max="65535" placeholder="2080" />
          </div>
          <div>
            <label class="muted" style="font-size:11px;display:block;margin-bottom:4px">Tag / remark</label>
            <input type="text" id="cfgTag" placeholder="my-relay" />
          </div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px">
          <button class="btn primary" id="cfgBuildBtn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
            Generate
          </button>
          <button class="btn ghost" id="cfgFillMine">Use my local IP</button>
          <span class="muted" id="cfgStatus" style="font-size:11px;align-self:center"></span>
        </div>

        <div class="cfg-block">
          <div class="cfg-head">
            <span class="cfg-title">V2Ray / Xray full config (JSON · runnable as-is)</span>
            <button class="btn ghost cfg-copy" data-target="outV2ray">Copy</button>
          </div>
          <pre class="console" id="outV2ray">Press “Generate” to build configs…</pre>
        </div>

        <div class="cfg-block">
          <div class="cfg-head">
            <span class="cfg-title">Telegram SOCKS5 link</span>
            <button class="btn ghost cfg-copy" data-target="outTelegram">Copy</button>
          </div>
          <pre class="console" id="outTelegram">—</pre>
        </div>

        <div class="cfg-block">
          <div class="cfg-head">
            <span class="cfg-title">SOCKS URI (v2rayN / v2rayNG · socks://base64(user:pass)@host:port#remark)</span>
            <button class="btn ghost cfg-copy" data-target="outUri">Copy</button>
          </div>
          <pre class="console" id="outUri">—</pre>
        </div>

        <div class="cfg-block">
          <div class="cfg-head">
            <span class="cfg-title">Windows CMD (curl test)</span>
            <button class="btn ghost cfg-copy" data-target="outCurl">Copy</button>
          </div>
          <pre class="console" id="outCurl">—</pre>
        </div>
      </div>
    </div>
  </section>

  <footer>refreshing every <span id="tickms">1000</span>ms · data stays on this machine</footer>
</div>

<script>
(() => {
  const $ = id => document.getElementById(id);

  // ---------------- tabs ----------------
  const tabs = document.querySelectorAll(".tab");
  const panes = document.querySelectorAll(".tab-pane");
  const setActiveTab = (name) => {
    tabs.forEach(x => x.classList.toggle("active", x.dataset.tab === name));
    panes.forEach(p => p.classList.toggle("active", p.id === "pane-" + name));
    // Chart canvas can't measure itself while hidden — refit when shown.
    if (name === "overview") requestAnimationFrame(fit);
  };
  tabs.forEach(t => t.addEventListener("click", () => setActiveTab(t.dataset.tab)));
  $("goClients").addEventListener("click", () => setActiveTab("clients"));
  $("goHosts").addEventListener("click", () => setActiveTab("hosts"));
  $("goNetwork").addEventListener("click", () => setActiveTab("network"));

  // ---------------- card spotlight hover ----------------
  document.addEventListener("mousemove", e => {
    const card = e.target.closest && e.target.closest(".card");
    if (!card) return;
    const r = card.getBoundingClientRect();
    card.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100) + "%");
    card.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100) + "%");
  });

  const fmtBytes = n => {
    if (!isFinite(n)) return "0 B";
    const u = ["B","KB","MB","GB","TB"]; let i=0;
    while (n >= 1024 && i < u.length-1) { n/=1024; i++; }
    return n.toFixed(n<10?2:n<100?1:0) + " " + u[i];
  };
  const fmtDur = s => {
    s = Math.floor(s||0);
    const h = Math.floor(s/3600), m = Math.floor((s%3600)/60), x = s%60;
    if (h) return `${h}h${String(m).padStart(2,'0')}m${String(x).padStart(2,'0')}s`;
    if (m) return `${m}m${String(x).padStart(2,'0')}s`;
    return `${x}s`;
  };
  const fmtPct = n => `${Math.max(0, Math.min(100, Number(n) || 0)).toFixed( Number(n) >= 10 || Number(n) === 0 ? 0 : 2)}%`;

  const setGauge = (ringId, valueId, pct) => {
    const ring = $(ringId), value = $(valueId);
    const p = Math.max(0, Math.min(100, Number(pct) || 0));
    if (ring) ring.style.setProperty('--pct', `${p}%`);
    if (value) value.textContent = fmtPct(p);
  };

  const renderSystem = sys => {
    const cpuPct = sys.cpu_percent || 0;
    const ramTotal = sys.ram_total || 0, ramUsed = sys.ram_used || 0;
    const swapTotal = sys.swap_total || 0, swapUsed = sys.swap_used || 0;
    const diskTotal = sys.storage_total || 0, diskUsed = sys.storage_used || 0;

    setGauge('cpuGauge', 'cpuGaugeValue', cpuPct);
    setGauge('ramGauge', 'ramGaugeValue', ramTotal > 0 ? (ramUsed / ramTotal) * 100 : 0);
    setGauge('swapGauge', 'swapGaugeValue', swapTotal > 0 ? (swapUsed / swapTotal) * 100 : 0);
    setGauge('diskGauge', 'diskGaugeValue', diskTotal > 0 ? (diskUsed / diskTotal) * 100 : 0);

    $('cpuMeta').textContent = `${sys.cpu_cores || 1} core${(sys.cpu_cores || 1) > 1 ? 's' : ''}`;
    $('ramMeta').textContent = `${fmtBytes(ramUsed)} / ${fmtBytes(ramTotal)}`;
    $('swapMeta').textContent = `${fmtBytes(swapUsed)} / ${fmtBytes(swapTotal)}`;
    $('diskMeta').textContent = `${fmtBytes(diskUsed)} / ${fmtBytes(diskTotal)}`;
  };

  const cv = $("chart"), cx = cv.getContext("2d");
  let lastSparkUp = [], lastSparkDown = [];
  const fit = () => {
    const r = devicePixelRatio || 1;
    const w = cv.clientWidth, h = cv.clientHeight;
    cv.width = Math.floor(w*r); cv.height = Math.floor(h*r);
    cx.setTransform(r,0,0,r,0,0);
  };
  window.addEventListener("resize", fit); fit();

  const draw = (upArr, dnArr) => {
    const w = cv.clientWidth, h = cv.clientHeight, pad = 6;
    cx.clearRect(0,0,w,h);
    const data = upArr.concat(dnArr);
    const max = Math.max(1, ...data);
    const line = (arr, color) => {
      if (!arr.length) return;
      cx.lineWidth = 1.6; cx.strokeStyle = color;
      cx.lineJoin = "round"; cx.lineCap = "round";
      cx.beginPath();
      const n = arr.length;
      arr.forEach((v,i) => {
        const x = pad + (i/(Math.max(1,n-1))) * (w - pad*2);
        const y = h - pad - (v/max) * (h - pad*2);
        if (i===0) cx.moveTo(x,y); else cx.lineTo(x,y);
      });
      cx.stroke();
      // fill
      const g = cx.createLinearGradient(0,0,0,h);
      g.addColorStop(0, color + "55"); g.addColorStop(1, color + "00");
      cx.lineTo(w-pad, h-pad); cx.lineTo(pad, h-pad); cx.closePath();
      cx.fillStyle = g; cx.fill();
    };
    line(dnArr, getComputedStyle(document.documentElement).getPropertyValue("--down").trim() || "#5ac8fa");
    line(upArr, getComputedStyle(document.documentElement).getPropertyValue("--up").trim()   || "#ff9650");
  };

  const renderHosts = hosts => {
    const tb = $("hosts");
    if (!hosts.length) { tb.innerHTML = '<tr><td colspan="7" class="muted">no traffic yet</td></tr>'; return; }
    const mx = Math.max(1, ...hosts.map(h => h.up + h.down));
    const flagOf = cc => {
      if (!cc || cc.length !== 2) return "";
      const A = 127397; // regional indicator offset
      return String.fromCodePoint(cc.charCodeAt(0)+A) + String.fromCodePoint(cc.charCodeAt(1)+A);
    };
    tb.innerHTML = hosts.map((h,i) => {
      const total = h.up + h.down, ratio = total / mx;
      const flag = flagOf((h.cc || "").toUpperCase());
      const countryTitle = h.country ? ` title="${h.country}"` : "";
      const hostCell = flag
        ? `<span${countryTitle} style="margin-right:6px">${flag}</span><span class="mono">${h.host}</span>`
        : `<span class="mono">${h.host}</span>`;
      return `<tr>
        <td><span class="dot ${h.active>0?'on':'off'}"></span></td>
        <td class="mono muted">${i+1}</td>
        <td>${hostCell}</td>
        <td><div class="bar"><i style="transform:scaleX(${ratio.toFixed(3)})"></i></div></td>
        <td class="mono up" style="text-align:right">${fmtBytes(h.up)}</td>
        <td class="mono down" style="text-align:right">${fmtBytes(h.down)}</td>
        <td class="mono acc" style="text-align:right">${h.active}/${h.total}</td>
      </tr>`;
    }).join("");
  };

  const renderClients = clients => {
    const tb = $("clients");
    if (!clients.length) { tb.innerHTML = '<tr><td colspan="7" class="muted">no clients yet</td></tr>'; return; }
    const mx = Math.max(1, ...clients.map(c => c.bytes_up + c.bytes_down));
    tb.innerHTML = clients.map((c,i) => {
      const total = c.bytes_up + c.bytes_down, ratio = total / mx;
      return `<tr>
        <td><span class="dot ${c.active_tunnels>0?'on':'off'}"></span></td>
        <td class="mono muted">${i+1}</td>
        <td class="mono">${c.ip}</td>
        <td class="mono up" style="text-align:right">${fmtBytes(c.bytes_up)}</td>
        <td class="mono down" style="text-align:right">${fmtBytes(c.bytes_down)}</td>
        <td class="mono acc" style="text-align:right">${c.active_tunnels}</td>
        <td class="mono acc" style="text-align:right">${c.total_tunnels}</td>
      </tr>`;
    }).join("");
  };

  let fails = 0;
  const tick = async () => {
    try {
      const r = await fetch("/api/stats", {cache:"no-store"});
      if (r.status === 401) {
        $("status").classList.add("bad");
        $("statusText").textContent = "auth";
        $("sub").textContent = "authentication required — redirecting to login...";
        window.location.replace('/login');
        return;
      }
      if (r.status === 403) {
        $("status").classList.add("bad");
        $("statusText").textContent = "denied";
        $("sub").textContent = "panel access denied by IP ACL (allowed_panel_ips).";
        return;
      }
      if (!r.ok) throw 0;
      const s = await r.json();
      fails = 0;
      $("status").classList.remove("bad"); $("statusText").textContent = "live";
      $("sub").textContent = `listening on ${s.listen || "?"} · upstream ${s.upstream || "?"}`;

      $("upSpeed").textContent   = fmtBytes(s.up_bps) + "/s";
      $("downSpeed").textContent = fmtBytes(s.down_bps) + "/s";
      $("upPeak").textContent    = fmtBytes(s.peak_up_bps) + "/s";
      $("downPeak").textContent  = fmtBytes(s.peak_down_bps) + "/s";
      $("active").textContent    = s.active;
      $("peakActive").textContent = s.peak_active || 0;
      $("total").textContent     = s.total;
      $("tcpConnections").textContent = s.active || 0;
      $("rate").textContent      = (s.conns_per_sec||0).toFixed(1);
      $("uptime").textContent    = fmtDur(s.uptime);
      $("totalBytes").textContent= fmtBytes(s.bytes_up + s.bytes_down);
      $("upBytes").textContent   = fmtBytes(s.bytes_up);
      $("downBytes").textContent = fmtBytes(s.bytes_down);
      $("upAvg").textContent     = fmtBytes(s.avg_up_bps) + "/s";
      $("downAvg").textContent   = fmtBytes(s.avg_down_bps) + "/s";
      $("errors").textContent    = s.errors;
      $("authFail").textContent  = s.auth_fail;
      $("refused").textContent   = s.refused;
      $("resets").textContent    = s.reset;
      $("hostCount").textContent = s.host_count;
      $("clientCount").textContent = s.client_count || 0;
      $("quickActive").textContent = s.active || 0;
      $("quickClients").textContent = s.client_count || 0;
      $("quickUpdated").textContent = new Date().toLocaleTimeString();
      renderSystem(s.system || {});

      const totalTraffic = (s.bytes_up || 0) + (s.bytes_down || 0);
      if (totalTraffic <= 0 && (s.active || 0) === 0) {
        $("quickGuideText").textContent = "No traffic yet — start a client connection, then open Destinations or Clients to inspect usage.";
      } else if ((s.active || 0) > 0) {
        $("quickGuideText").textContent = "Relay is active now — open Clients for per-IP usage and Destinations for top domains.";
      } else {
        $("quickGuideText").textContent = "Traffic was detected — explore Destinations and Clients tabs for detailed history.";
      }

      lastSparkUp = s.spark_up || [];
      lastSparkDown = s.spark_down || [];
      draw(lastSparkUp, lastSparkDown);
      renderHosts(s.hosts || []);
      renderClients(s.clients || []);
      applyControls(s.controls || {}, s.bytes_up + s.bytes_down);
    } catch(e) {
      if (++fails >= 2) {
        $("status").classList.add("bad");
        $("statusText").textContent = "offline";
        $("sub").textContent = "cannot fetch /api/stats — check server status, ACL, or auth.";
      }
    }
  };

  // ---------------- controls (toggles / forms / kill) ----------------
  let lastCtrl = {};
  let portDirty = false, limitDirty = false, userDirty = false, bwDirty = false;
  let connTotalDirty = false, connPerDirty = false;
  $("portInput").addEventListener("input", () => portDirty = true);
  $("limitInput").addEventListener("input", () => limitDirty = true);
  $("userInput").addEventListener("input", () => userDirty = true);
  $("bwInput").addEventListener("input", () => bwDirty = true);
  $("connTotalInput").addEventListener("input", () => connTotalDirty = true);
  $("connPerInput").addEventListener("input", () => connPerDirty = true);

  // ---------- theme toggle ----------
  const themeModeLabel = $("themeModeLabel");
  const syncThemeSwatches = palette => {
    document.querySelectorAll(".theme-swatch").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.palette === palette);
    });
  };
  const applyTheme = (t, palette) => {
    const nextTheme = t || document.documentElement.getAttribute("data-theme") || "dark";
    const nextPalette = palette || document.documentElement.getAttribute("data-accent") || "aurora";
    document.documentElement.setAttribute("data-theme", nextTheme);
    document.documentElement.setAttribute("data-accent", nextPalette);
    try {
      localStorage.setItem("s5theme", nextTheme);
      localStorage.setItem("s5palette", nextPalette);
    } catch(e) {}
    const icon = $("themeIcon");
    if (themeModeLabel) themeModeLabel.textContent = nextTheme === "light" ? "Light" : "Dark";
    syncThemeSwatches(nextPalette);
    if (!icon) return;
    if (nextTheme === "light") {
      // Sun icon
      icon.innerHTML = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="M4.93 4.93l1.41 1.41"/><path d="M17.66 17.66l1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M4.93 19.07l1.41-1.41"/><path d="M17.66 6.34l1.41-1.41"/>';
    } else {
      icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
    }
    requestAnimationFrame(() => draw(lastSparkUp, lastSparkDown));
  };
  applyTheme(
    document.documentElement.getAttribute("data-theme") || "dark",
    document.documentElement.getAttribute("data-accent") || "aurora",
  );
  $("themeBtn").addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "dark";
    const palette = document.documentElement.getAttribute("data-accent") || "aurora";
    applyTheme(cur === "dark" ? "light" : "dark", palette);
  });
  document.querySelectorAll(".theme-swatch").forEach(btn => {
    btn.addEventListener("click", () => {
      const theme = document.documentElement.getAttribute("data-theme") || "dark";
      applyTheme(theme, btn.dataset.palette || "aurora");
    });
  });

  const post = async (action, params={}) => {
    try {
      const r = await fetch("/api/control", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({action, ...params}),
      });
      const j = await r.json().catch(()=>({}));
      if (!j.ok) console.warn("control failed", action, j);
      tick();
      return j;
    } catch(e) { console.warn("control error", e); return {}; }
  };

  const applyControls = (c, totalBytes) => {
    lastCtrl = c;
    $("listenAddr").textContent = (c.listen_host || "?") + ":" + (c.listen_port || "?");
    $("bypassBadge").textContent = "bypassed " + (c.bypassed || 0)
      + (c.bypassed_active ? " (" + c.bypassed_active + " live)" : "");

    // master proxy toggle — green when ON, gray (off) when paused
    const tgP = $("tgProxy");
    tgP.classList.toggle("ok", !!c.proxy_enabled);
    tgP.classList.remove("danger");
    $("pausedBanner").classList.toggle("show", !c.proxy_enabled);

    // whitelist master
    $("tgWhitelist").classList.toggle("on", !!c.whitelist_enabled);
    // whitelist strict — color red when armed, since it actively blocks
    const tgS = $("tgStrict");
    tgS.classList.toggle("on", !!c.whitelist_strict);
    tgS.classList.toggle("danger", !!c.whitelist_strict);
    // .ir redirect — accent-green, independent of whitelist
    $("tgIr").classList.toggle("ok", !!c.ir_redirect);

    // presets
    const presets = c.presets || {};
    const counts  = c.preset_domains || {};
    const cidrCounts = c.preset_cidrs || {};
    document.querySelectorAll(".preset").forEach(el => {
      const name = el.dataset.name;
      el.classList.toggle("on", !!presets[name]);
      const cnt = $("cnt-" + name);
      if (cnt) {
        const d = (counts[name] || []).length;
        const ip = cidrCounts[name] || 0;
        cnt.textContent = d + "d · " + ip + "ip";
      }
    });

    // port input (don't clobber while user is editing)
    if (!portDirty) $("portInput").value = c.listen_port || "";

    // current username display + input
    const u = c.username || "";
    const pw = c.password || "";
    $("currentUser").textContent = u || "—";
    $("credsUser").textContent = u || "—";
    window.__livePass = pw;
    const revealed = window.__credsRevealed === true;
    $("credsPass").textContent = revealed ? (pw || "—") : (pw ? "•".repeat(Math.min(pw.length, 12)) : "—");
    if (!userDirty) $("userInput").value = u;

    // traffic limit
    const lim = c.traffic_limit_bytes || 0;
    if (!limitDirty) $("limitInput").value = lim ? (lim / (1024*1024)).toFixed(0) : "";
    const bar = $("limitBar"), ls = $("limitStatus");
    if (lim > 0) {
      const pct = Math.min(100, (totalBytes / lim) * 100);
      bar.style.width = pct.toFixed(1) + "%";
      ls.textContent = `${fmtBytes(totalBytes)} / ${fmtBytes(lim)}  (${pct.toFixed(1)}%)`
        + (totalBytes >= lim ? "  · LIMIT REACHED — new connections refused" : "");
      ls.classList.toggle("bad", totalBytes >= lim);
    } else {
      bar.style.width = "0%";
      ls.textContent = "no limit set";
      ls.classList.remove("bad");
    }

    // bandwidth cap
    const bps = c.bandwidth_limit_bps || 0;
    if (!bwDirty) $("bwInput").value = bps ? Math.round(bps / 1024) : "";
    const bwS = $("bwStatus");
    if (bps > 0) {
      const kb = bps / 1024;
      bwS.textContent = `cap: ${kb >= 1024 ? (kb/1024).toFixed(2) + " MB/s" : kb.toFixed(0) + " KB/s"} · shared across all tunnels`;
    } else {
      bwS.textContent = "no bandwidth cap · all tunnels share this limit";
    }

    // connection caps
    const ct = c.max_conn_total || 0;
    const cp = c.max_conn_per_client || 0;
    if (!connTotalDirty) $("connTotalInput").value = ct || "";
    if (!connPerDirty) $("connPerInput").value = cp || "";
    const parts = [];
    if (ct > 0) parts.push(`global: ${ct}`);
    if (cp > 0) parts.push(`per-client: ${cp}`);
    const refused = c.conn_refused || 0;
    $("connStatus").textContent = (parts.length ? parts.join(" · ") : "no caps set")
      + (refused ? `  ·  refused: ${refused}` : "");

    // geoip toggle
    $("tgGeoip").classList.toggle("ok", !!c.geoip_enabled);

    // auth-required toggle — green when auth required (default/safe),
    // red/danger when disabled because it's an insecure state.
    const tgA = $("tgAuth");
    const authOn = c.auth_required !== false;
    tgA.classList.toggle("ok", authOn);
    tgA.classList.toggle("danger", !authOn);
  };

  // wire toggles
  $("tgProxy").addEventListener("click",
    () => post("set_proxy", {enabled: !lastCtrl.proxy_enabled}));
  $("tgWhitelist").addEventListener("click",
    () => post("set_whitelist", {enabled: !lastCtrl.whitelist_enabled}));
  $("tgStrict").addEventListener("click", async () => {
    const turningOn = !lastCtrl.whitelist_strict;
    if (turningOn && !confirm(
      "Enable STRICT whitelist?\n\n" +
      "Every destination that is NOT on the whitelist will be refused.\n" +
      "All active tunnels to non-whitelisted hosts will be dropped immediately.\n\n" +
      "Tip: turn on the main Whitelist toggle + pick presets first."
    )) return;
    post("set_whitelist_strict", {enabled: turningOn});
  });
  $("tgIr").addEventListener("click",
    () => post("set_ir_redirect", {enabled: !lastCtrl.ir_redirect}));
  document.querySelectorAll(".preset").forEach(el => {
    el.addEventListener("click", () => {
      const name = el.dataset.name;
      const current = !!(lastCtrl.presets && lastCtrl.presets[name]);
      post("set_preset", {name, enabled: !current});
    });
  });

  // port change
  $("portBtn").addEventListener("click", async () => {
    const port = parseInt($("portInput").value, 10);
    if (!port || port < 1 || port > 65535) { alert("Port must be 1-65535"); return; }
    const j = await post("change_port", {port});
    portDirty = false;
    if (j && j.ok === false) alert("Port change failed: " + (j.error || "unknown"));
  });

  // upstream check
  $("upstreamCheckBtn").addEventListener("click", async () => {
    const btn = $("upstreamCheckBtn");
    const st = $("upstreamCheckStatus");
    btn.disabled = true;
    st.style.color = "var(--muted)";
    st.textContent = "Checking upstream via IP API…";
    try {
      const j = await post("check_upstream");
      if (j && j.ok) {
        const ip = j.public_ip || "unknown";
        const api = j.api || "api";
        const ms = (typeof j.latency_ms === "number") ? `${j.latency_ms}ms` : "";
        st.style.color = "var(--good)";
        st.textContent = `UP · Public IP: ${ip} · ${api}${ms ? ` · ${ms}` : ""}`;
      } else {
        st.style.color = "var(--bad)";
        st.textContent = `DOWN · ${((j && j.error) || "upstream check failed")}`;
      }
    } catch (e) {
      st.style.color = "var(--bad)";
      st.textContent = "DOWN · request failed";
    } finally {
      btn.disabled = false;
    }
  });

  // traffic limit
  $("limitBtn").addEventListener("click", async () => {
    const mb = parseFloat($("limitInput").value);
    if (isNaN(mb) || mb < 0) { alert("Enter a non-negative MB value"); return; }
    await post("set_limit", {mb});
    limitDirty = false;
  });
  $("limitOff").addEventListener("click", async () => {
    $("limitInput").value = "";
    await post("set_limit", {bytes: 0});
    limitDirty = false;
  });

  // bandwidth cap
  $("bwBtn").addEventListener("click", async () => {
    const kbps = parseFloat($("bwInput").value);
    if (isNaN(kbps) || kbps < 0) { alert("Enter a non-negative KB/s value"); return; }
    await post("set_bandwidth", {kbps});
    bwDirty = false;
  });
  $("bwOff").addEventListener("click", async () => {
    $("bwInput").value = "";
    await post("set_bandwidth", {kbps: 0});
    bwDirty = false;
  });

  // connection caps
  $("connTotalBtn").addEventListener("click", async () => {
    const v = parseInt($("connTotalInput").value, 10);
    if (isNaN(v) || v < 0) { alert("Enter a non-negative integer"); return; }
    await post("set_conn_cap", {total: v});
    connTotalDirty = false;
  });
  $("connPerBtn").addEventListener("click", async () => {
    const v = parseInt($("connPerInput").value, 10);
    if (isNaN(v) || v < 0) { alert("Enter a non-negative integer"); return; }
    await post("set_conn_cap", {per_client: v});
    connPerDirty = false;
  });

  // geoip toggle
  $("tgGeoip").addEventListener("click", () => {
    post("set_geoip", {enabled: !lastCtrl.geoip_enabled});
  });

  // auth-required toggle — confirm before disabling, since it's risky.
  $("tgAuth").addEventListener("click", () => {
    const turningOff = lastCtrl.auth_required !== false;
    if (turningOff && !confirm(
      "Disable SOCKS5 client authentication?\n\n" +
      "Any client that can reach this port will be able to use the proxy " +
      "WITHOUT a username or password.\n\n" +
      "Only do this on a trusted network."
    )) return;
    post("set_auth_required", {enabled: !turningOff});
  });

  // reset counters
  $("resetBtn").addEventListener("click", async () => {
    if (confirm("Reset all traffic counters (up/down totals, peaks, per-host)?")) {
      await post("reset_traffic");
    }
  });

  // kill switch
  $("killBtn").addEventListener("click", async () => {
    if (!confirm("⚠ This will TERMINATE the relay process immediately.\nAll active tunnels will drop. Continue?")) return;
    await post("kill");
    $("status").classList.add("bad");
    $("statusText").textContent = "terminated";
  });

  // live credential rotation
  $("passReveal").addEventListener("click", () => {
    const p = $("passInput");
    p.type = (p.type === "password") ? "text" : "password";
  });
  $("credsReveal").addEventListener("click", () => {
    window.__credsRevealed = !window.__credsRevealed;
    $("credsRevealLabel").textContent = window.__credsRevealed ? "Hide" : "Show";
    const pw = window.__livePass || "";
    $("credsPass").textContent = window.__credsRevealed
      ? (pw || "—")
      : (pw ? "•".repeat(Math.min(pw.length, 12)) : "—");
  });
  $("credsCopy").addEventListener("click", async () => {
    const u = $("credsUser").textContent.trim();
    const pw = window.__livePass || "";
    if (!u || !pw) return;
    try {
      await navigator.clipboard.writeText(u + ":" + pw);
      const btn = $("credsCopy");
      const prev = btn.innerHTML;
      btn.innerHTML = "✓ copied";
      setTimeout(() => { btn.innerHTML = prev; }, 1200);
    } catch (e) {}
  });
  $("credsBtn").addEventListener("click", async () => {
    const st = $("credsStatus");
    const username = $("userInput").value.trim();
    const password = $("passInput").value;
    if (!username || !password) {
      st.textContent = "✖ fill both username and password";
      st.style.color = "var(--bad)";
      return;
    }
    if (username.length > 255 || password.length > 255) {
      st.textContent = "✖ max 255 chars per field";
      st.style.color = "var(--bad)";
      return;
    }
    st.textContent = "… applying …";
    st.style.color = "var(--muted)";
    let j = null;
    try {
      j = await post("set_credentials", {username, password});
    } catch (e) {
      console.error("set_credentials failed", e);
    }
    console.log("set_credentials response:", j);
    if (j && j.ok) {
      $("passInput").value = "";
      $("passInput").type = "password";
      userDirty = false;
      st.textContent = "✓ credentials updated — user=" + (j.username || username) + " — dropped " + (j.dropped || 0) + " tunnel(s)";
      st.style.color = "var(--good)";
      setTimeout(() => {
        if (st.textContent.startsWith("✓")) { st.textContent = ""; st.style.color = ""; }
      }, 8000);
    } else {
      st.textContent = "✖ " + ((j && j.error) || "update failed — check console/network tab");
      st.style.color = "var(--bad)";
    }
  });

  // ---------------- config generator ----------------
  const cfgBuild = () => {
    const host = ($("cfgHost").value || "").trim();
    const port = parseInt($("cfgPort").value, 10);
    const tag  = ($("cfgTag").value || "socks-relay").trim() || "socks-relay";
    const st   = $("cfgStatus");
    const user = (lastCtrl && lastCtrl.username) || "";
    const pass = (lastCtrl && lastCtrl.password) || "";
    if (!host || !port || port < 1 || port > 65535) {
      st.textContent = "✖ enter a valid host and port";
      st.style.color = "var(--bad)";
      return;
    }
    if (!user || !pass) {
      st.textContent = "✖ server credentials not loaded yet";
      st.style.color = "var(--bad)";
      return;
    }
    st.style.color = "var(--good)";
    st.textContent = "✓ generated — credentials pulled from live relay";

    const pwShown = pass;

    // 1) V2Ray / Xray full config (standalone, runnable)
    //    - inbounds: local socks (10808) + http (10809) so apps can connect
    //    - outbound: this SOCKS relay
    //    - routing: direct for private/LAN, blackhole for ads/private blocked dst
    const v2 = {
      log: { loglevel: "warning" },
      inbounds: [
        {
          tag: "socks-in",
          port: 10808,
          listen: "127.0.0.1",
          protocol: "socks",
          settings: { auth: "noauth", udp: true, ip: "127.0.0.1" },
          sniffing: { enabled: true, destOverride: ["http", "tls"] }
        },
        {
          tag: "http-in",
          port: 10809,
          listen: "127.0.0.1",
          protocol: "http",
          sniffing: { enabled: true, destOverride: ["http", "tls"] }
        }
      ],
      outbounds: [
        {
          tag: tag,
          protocol: "socks",
          settings: {
            servers: [{
              address: host,
              port: port,
              users: [{ user: user, pass: pwShown, level: 0 }]
            }]
          },
          streamSettings: { network: "tcp" },
          mux: { enabled: false }
        },
        { tag: "direct",  protocol: "freedom",   settings: {} },
        { tag: "block",   protocol: "blackhole", settings: {} }
      ],
      routing: {
        domainStrategy: "IPIfNonMatch",
        rules: [
          { type: "field", ip: ["geoip:private"], outboundTag: "direct" },
          { type: "field", protocol: ["bittorrent"], outboundTag: "block" }
        ]
      }
    };
    $("outV2ray").textContent = JSON.stringify(v2, null, 2);

    // 2) Telegram SOCKS5 link
    //    https://t.me/socks?server=...&port=...&user=...&pass=...
    //    also tg://socks?... scheme (opens Telegram directly)
    const tgParams = new URLSearchParams({
      server: host, port: String(port), user: user, pass: pwShown
    }).toString();
    $("outTelegram").textContent =
      "https://t.me/socks?" + tgParams + "\n" +
      "tg://socks?" + tgParams;

    // 3) SOCKS URI — v2rayN / v2rayNG style: socks://base64(user:pass)@host:port#remark
    //    NOTE: classic socks5://user:pass@host:port works for curl/Xray but
    //    v2rayN/NG only import the base64 form, so we emit that as the canonical URI.
    const enc = encodeURIComponent;
    // Use the modern, URL-safe-ish base64 of the raw "user:pass" string.
    // btoa() handles ASCII; for multi-byte chars, encode UTF-8 first.
    const utf8 = new TextEncoder().encode(user + ":" + pwShown);
    let bin = "";
    for (let i = 0; i < utf8.length; i++) bin += String.fromCharCode(utf8[i]);
    const b64 = btoa(bin); // standard base64 with padding
    const remark = enc(tag);
    $("outUri").textContent =
      `socks://${b64}@${host}:${port}#${remark}\n` +
      `socks5://${enc(user)}:${enc(pwShown)}@${host}:${port}`;

    // 4) Windows CMD curl test
    //    For URI-style flags we URL-encode user/pass so chars like '@' don't
    //    confuse the parser. --proxy-user takes the raw values.
    $("outCurl").textContent =
      `curl -x socks5h://${enc(user)}:${enc(pwShown)}@${host}:${port} https://ifconfig.me\n` +
      `curl --proxy-user ${user}:${pwShown} --socks5-hostname ${host}:${port} https://api.ipify.org`;
  };

  $("cfgBuildBtn").addEventListener("click", cfgBuild);
  $("cfgHost").addEventListener("keydown", e => { if (e.key === "Enter") cfgBuild(); });
  $("cfgPort").addEventListener("keydown", e => { if (e.key === "Enter") cfgBuild(); });
  $("cfgTag").addEventListener("keydown",  e => { if (e.key === "Enter") cfgBuild(); });

  $("cfgFillMine").addEventListener("click", () => {
    // best-effort: use the hostname the dashboard was loaded from
    $("cfgHost").value = location.hostname || "";
    if (!$("cfgPort").value && lastCtrl && lastCtrl.listen_port) {
      $("cfgPort").value = lastCtrl.listen_port;
    }
    cfgBuild();
  });

  // Copy buttons (shared for all cfg outputs)
  document.querySelectorAll(".cfg-copy").forEach(btn => {
    btn.addEventListener("click", async () => {
      const tgt = $(btn.dataset.target);
      if (!tgt) return;
      const text = tgt.textContent || "";
      try {
        await navigator.clipboard.writeText(text);
      } catch (e) {
        // fallback for non-secure contexts
        const ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta);
        ta.select(); try { document.execCommand("copy"); } catch(_){}
        document.body.removeChild(ta);
      }
      const orig = btn.textContent;
      btn.textContent = "Copied ✓";
      btn.classList.add("ok");
      setTimeout(() => { btn.textContent = orig; btn.classList.remove("ok"); }, 1400);
    });
  });

  // Pre-fill default port from controls snapshot once it arrives
  const cfgSeed = setInterval(() => {
    if (lastCtrl && lastCtrl.listen_port) {
      if (!$("cfgPort").value) $("cfgPort").value = lastCtrl.listen_port;
      if (!$("cfgHost").value) $("cfgHost").value = location.hostname || "";
      clearInterval(cfgSeed);
    }
  }, 500);

  // Check if auth is required on startup
  const checkAuthRequired = async () => {
    try {
      const r = await fetch('/api/stats', {cache:'no-store'});
      if (r.status === 401) {
        window.location.replace('/login');
      } else if (r.ok) {
        tick();
      }
    } catch (e) {
      tick();
    }
  };
  checkAuthRequired();
  setInterval(tick, 1000);
})();
</script>
</body></html>
"""
