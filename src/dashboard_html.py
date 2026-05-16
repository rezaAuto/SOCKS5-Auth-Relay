"""Inline HTML dashboard for the SOCKS5 auth relay web UI."""

_WEB_INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>SOCKS5 relay · live traffic</title>
<script>
  (function(){try{var pref=localStorage.getItem("s5themePref")||localStorage.getItem("s5theme")||"dark";
    var p=localStorage.getItem("s5palette")||"aurora";
    var f=localStorage.getItem("s5font")||"default";
    var t=(pref==="auto")
      ? (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark")
      : pref;
    document.documentElement.setAttribute("data-theme",t);
    document.documentElement.setAttribute("data-accent",p);
    document.documentElement.setAttribute("data-font",f);}catch(e){}})();
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
  --font:"Segoe UI Variable","Segoe UI",Tahoma,ui-sans-serif,system-ui,-apple-system,Roboto,sans-serif;
  --title-font:"Segoe UI Variable","Segoe UI",ui-sans-serif,system-ui,sans-serif;
  --mono:"Cascadia Mono","Cascadia Code","Consolas",ui-monospace,SFMono-Regular,monospace;
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
html[data-font="default"]{
  --font:"Segoe UI Variable","Segoe UI",Tahoma,ui-sans-serif,system-ui,-apple-system,Roboto,sans-serif;
  --title-font:"Segoe UI Variable","Segoe UI",ui-sans-serif,system-ui,sans-serif;
  --mono:"Cascadia Mono","Cascadia Code","Consolas",ui-monospace,SFMono-Regular,monospace;
}
html[data-font="modern"]{
  --font:"Bahnschrift","Segoe UI Variable","Segoe UI","Trebuchet MS",ui-sans-serif,system-ui,sans-serif;
  --title-font:"Bahnschrift","Segoe UI Variable","Segoe UI",ui-sans-serif,sans-serif;
  --mono:"Cascadia Code","Consolas","Lucida Console",ui-monospace,monospace;
}
html[data-font="classic"]{
  --font:"Trebuchet MS","Verdana","Segoe UI",ui-sans-serif,system-ui,sans-serif;
  --title-font:"Trebuchet MS","Verdana","Segoe UI",ui-sans-serif,sans-serif;
  --mono:"Consolas","Courier New",ui-monospace,monospace;
}
html[data-font="terminal"]{
  --font:"Lucida Console","Consolas","Cascadia Mono",ui-monospace,monospace;
  --title-font:"Lucida Console","Consolas",ui-monospace,monospace;
  --mono:"Lucida Console","Consolas","Cascadia Mono",ui-monospace,monospace;
}
html[data-font="neat"]{
  --font:"Tahoma","Segoe UI","Arial",ui-sans-serif,system-ui,sans-serif;
  --title-font:"Tahoma","Segoe UI",ui-sans-serif,sans-serif;
  --mono:"Consolas","Cascadia Mono",ui-monospace,monospace;
}
html[data-font="persian"]{
  --font:"B Yekan","IRANSans","Tahoma","Segoe UI",ui-sans-serif,system-ui,sans-serif;
  --title-font:"B Yekan","IRANSans","Tahoma","Segoe UI",ui-sans-serif,sans-serif;
  --mono:"Consolas","Cascadia Mono",ui-monospace,monospace;
}
html[data-font="pro"]{
  --font:"Aptos","Segoe UI Variable","Segoe UI","Arial Nova","Arial",ui-sans-serif,system-ui,sans-serif;
  --title-font:"Aptos Display","Aptos","Segoe UI Variable","Segoe UI",ui-sans-serif,sans-serif;
  --mono:"Cascadia Code","Consolas","Lucida Console",ui-monospace,monospace;
}
html[data-font="readable"]{
  --font:"Verdana","Tahoma","Segoe UI","Arial",ui-sans-serif,system-ui,sans-serif;
  --title-font:"Verdana","Segoe UI Semibold","Segoe UI",ui-sans-serif,sans-serif;
  --mono:"Consolas","Courier New","Cascadia Mono",ui-monospace,monospace;
}
html[data-font="rounded"]{
  --font:"Arial Rounded MT Bold","Segoe UI","Trebuchet MS","Tahoma",ui-sans-serif,system-ui,sans-serif;
  --title-font:"Arial Rounded MT Bold","Segoe UI Semibold","Segoe UI",ui-sans-serif,sans-serif;
  --mono:"Cascadia Mono","Consolas","Lucida Console",ui-monospace,monospace;
}
html[data-font="editorial"]{
  --font:"Cambria","Constantia","Georgia","Segoe UI",ui-serif,serif;
  --title-font:"Cambria","Constantia","Georgia","Segoe UI",ui-serif,serif;
  --mono:"Cascadia Mono","Consolas","Courier New",ui-monospace,monospace;
}
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
html[data-accent="cyber"]{
  --up:#f97316; --down:#22d3ee; --accent:#a78bfa; --good:#34d399; --warn:#facc15; --bad:#f43f5e;
  --bg-glow-a:rgba(34,211,238,.18); --bg-glow-b:rgba(167,139,250,.14); --bg-glow-c:rgba(249,115,22,.12);
  --orb-a-solid:#22d3ee; --orb-b-solid:#a78bfa; --orb-c-solid:#f97316;
  --title-grad-start:#ecfeff; --title-grad-end:#ddd6fe;
  --glow-accent:0 0 22px rgba(167,139,250,.28); --glow-down:0 0 24px rgba(34,211,238,.28);
}
html[data-theme="light"][data-accent="cyber"]{
  --title-grad-start:#0f172a; --title-grad-end:#4338ca;
  --bg-glow-a:rgba(34,211,238,.12); --bg-glow-b:rgba(167,139,250,.10); --bg-glow-c:rgba(249,115,22,.08);
}
html[data-accent="forest"]{
  --up:#84cc16; --down:#10b981; --accent:#14b8a6; --good:#22c55e; --warn:#eab308; --bad:#ef4444;
  --bg-glow-a:rgba(16,185,129,.18); --bg-glow-b:rgba(20,184,166,.12); --bg-glow-c:rgba(132,204,22,.11);
  --orb-a-solid:#10b981; --orb-b-solid:#14b8a6; --orb-c-solid:#84cc16;
  --title-grad-start:#ecfdf5; --title-grad-end:#a7f3d0;
  --glow-accent:0 0 22px rgba(20,184,166,.22); --glow-down:0 0 24px rgba(16,185,129,.24);
}
html[data-theme="light"][data-accent="forest"]{
  --title-grad-start:#052e16; --title-grad-end:#115e59;
  --bg-glow-a:rgba(16,185,129,.10); --bg-glow-b:rgba(20,184,166,.08); --bg-glow-c:rgba(132,204,22,.08);
}
html[data-accent="violet"]{
  --up:#fb7185; --down:#8b5cf6; --accent:#c084fc; --good:#4ade80; --warn:#fbbf24; --bad:#f43f5e;
  --bg-glow-a:rgba(139,92,246,.18); --bg-glow-b:rgba(192,132,252,.12); --bg-glow-c:rgba(251,113,133,.11);
  --orb-a-solid:#8b5cf6; --orb-b-solid:#c084fc; --orb-c-solid:#fb7185;
  --title-grad-start:#faf5ff; --title-grad-end:#e9d5ff;
  --glow-accent:0 0 22px rgba(192,132,252,.28); --glow-down:0 0 24px rgba(139,92,246,.24);
}
html[data-theme="light"][data-accent="violet"]{
  --title-grad-start:#3b0764; --title-grad-end:#6d28d9;
  --bg-glow-a:rgba(139,92,246,.10); --bg-glow-b:rgba(192,132,252,.08); --bg-glow-c:rgba(251,113,133,.07);
}
html[data-accent="mono"]{
  --up:#a3a3a3; --down:#d4d4d4; --accent:#f5f5f5; --good:#86efac; --warn:#fde047; --bad:#fca5a5;
  --bg-glow-a:rgba(212,212,212,.15); --bg-glow-b:rgba(163,163,163,.10); --bg-glow-c:rgba(245,245,245,.08);
  --orb-a-solid:#d4d4d4; --orb-b-solid:#a3a3a3; --orb-c-solid:#f5f5f5;
  --title-grad-start:#fafafa; --title-grad-end:#d4d4d4;
  --glow-accent:0 0 20px rgba(245,245,245,.18); --glow-down:0 0 20px rgba(212,212,212,.18);
}
html[data-theme="light"][data-accent="mono"]{
  --title-grad-start:#111827; --title-grad-end:#4b5563;
  --bg-glow-a:rgba(212,212,212,.08); --bg-glow-b:rgba(163,163,163,.07); --bg-glow-c:rgba(245,245,245,.06);
}
html[data-accent="lava"]{
  --up:#f97316; --down:#ef4444; --accent:#fb7185; --good:#34d399; --warn:#f59e0b; --bad:#dc2626;
  --bg-glow-a:rgba(239,68,68,.18); --bg-glow-b:rgba(249,115,22,.14); --bg-glow-c:rgba(251,113,133,.10);
  --orb-a-solid:#ef4444; --orb-b-solid:#f97316; --orb-c-solid:#fb7185;
  --title-grad-start:#fff7ed; --title-grad-end:#fecaca;
  --glow-accent:0 0 22px rgba(251,113,133,.24); --glow-down:0 0 24px rgba(239,68,68,.24);
}
html[data-theme="light"][data-accent="lava"]{
  --title-grad-start:#431407; --title-grad-end:#b91c1c;
  --bg-glow-a:rgba(239,68,68,.10); --bg-glow-b:rgba(249,115,22,.08); --bg-glow-c:rgba(251,113,133,.08);
}
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
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;font-family:var(--title-font)}
.header-actions{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-left:auto}
.theme-tools{position:relative;display:flex;align-items:center;justify-content:flex-end}
.theme-launcher{display:inline-flex;align-items:center;gap:9px;padding:7px 10px;border-radius:999px;
  border:1px solid var(--border);background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.01)),var(--panel);
  color:var(--text);font-size:11px;cursor:pointer;box-shadow:var(--sh-sm),var(--sh-inset);
  transition:border-color .2s ease,box-shadow .2s ease,transform .15s ease}
.theme-launcher:hover{transform:translateY(-1px);border-color:var(--down);box-shadow:var(--sh-md),var(--sh-inset),0 0 14px rgba(90,200,250,.12)}
.theme-launcher[aria-expanded="true"]{border-color:rgba(90,200,250,.45);box-shadow:var(--sh-md),var(--glow-down)}
.theme-launcher .chip{width:20px;height:20px;border-radius:999px;border:1px solid rgba(255,255,255,.2);
  background:linear-gradient(135deg,var(--down),var(--accent),var(--up));box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 2px 8px rgba(0,0,0,.3)}
.theme-launcher-copy{display:flex;flex-direction:column;align-items:flex-start;gap:1px;min-width:0}
.theme-launcher-copy > span:first-child{font-size:10px;line-height:1;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}
.theme-launcher .mode{font-size:11px;line-height:1.15;color:var(--text);letter-spacing:.02em;text-transform:none;white-space:nowrap}
.theme-caret{width:7px;height:7px;border-right:1.5px solid var(--muted);border-bottom:1.5px solid var(--muted);
  transform:rotate(45deg) translateY(-2px);transition:transform .18s ease,border-color .18s ease}
.theme-launcher[aria-expanded="true"] .theme-caret{transform:rotate(225deg) translate(-1px,-1px);border-color:var(--down)}
.theme-panel{position:absolute;top:calc(100% + 10px);right:0;z-index:20;width:min(92vw,430px);max-width:430px;
  border:1px solid var(--border);border-radius:14px;padding:14px;
  background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.015)),var(--panel2);
  box-shadow:var(--sh-lg),var(--sh-inset);backdrop-filter:blur(14px) saturate(140%);
  -webkit-backdrop-filter:blur(14px) saturate(140%);opacity:0;transform:translateY(-6px) scale(.98);
  pointer-events:none;transition:opacity .18s ease,transform .18s ease}
.theme-panel.open{opacity:1;transform:translateY(0) scale(1);pointer-events:auto}
.theme-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:12px}
.theme-head b{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.theme-summary{display:block;margin-top:3px;font-size:12px;color:var(--text)}
.theme-actions{display:flex;align-items:center;gap:6px;flex:0 0 auto}
.theme-random,.theme-reset{padding:5px 9px !important;font-size:11px !important}
.theme-preview{display:grid;grid-template-columns:42px minmax(0,1fr);align-items:center;gap:10px;
  border:1px solid var(--border);border-radius:12px;padding:10px;margin-bottom:12px;
  background:linear-gradient(135deg,rgba(90,200,250,.08),rgba(210,160,255,.08) 48%,rgba(255,150,80,.06))}
.theme-preview-swatch{width:42px;height:42px;border-radius:12px;border:1px solid rgba(255,255,255,.16);
  background:linear-gradient(135deg,var(--down),var(--accent),var(--up));box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 8px 18px rgba(0,0,0,.24)}
.theme-preview b{display:block;font-size:13px;color:var(--text);line-height:1.2}
.theme-preview-text{display:block;margin-top:2px;font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.theme-section{margin-top:12px}
.theme-section-title{display:flex;align-items:center;justify-content:space-between;margin-bottom:7px;
  font-size:10px;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}
.theme-modes{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.theme-mode-btn{position:relative;display:flex;align-items:center;justify-content:center;gap:6px;min-height:34px;
  border:1px solid var(--border);border-radius:9px;padding:7px 8px;background:rgba(255,255,255,.025);color:var(--muted);
  font-size:11px;cursor:pointer;transition:all .18s ease;text-transform:uppercase;letter-spacing:.05em}
.theme-mode-btn:hover{color:var(--text);border-color:var(--down);background:rgba(90,200,250,.055)}
.theme-mode-btn.active{color:#fff;border-color:rgba(90,200,250,.48);background:linear-gradient(180deg,rgba(90,200,250,.2),rgba(90,200,250,.07));box-shadow:0 0 0 1px rgba(90,200,250,.14),0 0 12px rgba(90,200,250,.16)}
.theme-mode-icon{display:inline-grid;place-items:center;width:17px;height:17px;border-radius:6px;
  background:rgba(255,255,255,.06);color:var(--down);font-size:10px;line-height:1}
.theme-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.theme-option{position:relative;display:flex;align-items:center;gap:9px;width:100%;min-height:54px;border:1px solid var(--border);border-radius:11px;
  padding:8px 30px 8px 8px;background:linear-gradient(180deg,rgba(255,255,255,.035),transparent);color:var(--text);
  cursor:pointer;transition:all .18s ease;text-align:left}
.theme-option:hover{border-color:var(--accent);transform:translateY(-1px);background:linear-gradient(180deg,rgba(255,255,255,.055),transparent)}
.theme-option.active{border-color:rgba(210,160,255,.55);box-shadow:0 0 0 1px rgba(210,160,255,.22),0 0 14px rgba(210,160,255,.16)}
.theme-option.active::after{content:"✓";position:absolute;right:9px;top:50%;transform:translateY(-50%);
  width:16px;height:16px;border-radius:999px;display:grid;place-items:center;font-size:10px;color:#fff;
  background:linear-gradient(135deg,var(--accent),var(--down));box-shadow:0 0 10px rgba(90,200,250,.22)}
.theme-dot{width:24px;height:24px;border-radius:999px;border:1px solid rgba(255,255,255,.18);flex:0 0 24px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 2px 8px rgba(0,0,0,.28)}
.theme-dot.aurora{background:linear-gradient(135deg,#5ac8fa,#d2a0ff,#ff9650)}
.theme-dot.ocean{background:linear-gradient(135deg,#38bdf8,#7dd3fc,#22d3ee)}
.theme-dot.emerald{background:linear-gradient(135deg,#34d399,#10b981,#fbbf24)}
.theme-dot.sunset{background:linear-gradient(135deg,#fb923c,#f472b6,#a78bfa)}
.theme-dot.rose{background:linear-gradient(135deg,#f472b6,#2dd4bf,#fb7185)}
.theme-dot.cyber{background:linear-gradient(135deg,#22d3ee,#a78bfa,#f97316)}
.theme-dot.forest{background:linear-gradient(135deg,#10b981,#14b8a6,#84cc16)}
.theme-dot.violet{background:linear-gradient(135deg,#8b5cf6,#c084fc,#fb7185)}
.theme-dot.mono{background:linear-gradient(135deg,#d4d4d4,#a3a3a3,#f5f5f5)}
.theme-dot.lava{background:linear-gradient(135deg,#ef4444,#f97316,#fb7185)}
.theme-option .meta{display:flex;flex-direction:column;gap:2px;min-width:0}
.theme-option .meta b{font-size:12px;line-height:1.1}
.theme-option .meta span{font-size:10px;color:var(--muted);line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#themeFonts{grid-template-columns:repeat(2,minmax(0,1fr)) !important}
#themeFonts .theme-mode-btn{justify-content:flex-start;text-align:left;text-transform:none;letter-spacing:0;min-height:40px}
#themeFonts .theme-mode-btn::after{content:attr(data-sample);margin-left:auto;color:var(--dim);font-size:10px;letter-spacing:0;text-transform:none}
.theme-subtitle{margin:8px 0 6px;font-size:10px;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}
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
@media(max-width:640px){
  .sys-grid{grid-template-columns:1fr}
  .theme-tools{width:100%;justify-content:flex-start}
  .theme-launcher{max-width:100%}
  .theme-panel{position:fixed;left:12px;right:12px;top:76px;width:auto;max-width:none;
    max-height:calc(100vh - 96px);overflow:auto}
  .theme-head{align-items:stretch;flex-direction:column}
  .theme-actions{width:100%}
  .theme-actions .btn{flex:1}
  .theme-grid,#themeFonts{grid-template-columns:1fr !important}
}
</style>
</head>
<body>
<div class="orbs"><div class="orb a"></div><div class="orb b"></div><div class="orb c"></div></div>

<div class="wrap">
  <header>
    <div class="title">
      <div class="logo"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" fill="currentColor" fill-opacity=".2"></polygon></svg></div>
      <div>
        <h1 id="appTitle">SOCKS5 relay · live traffic</h1>
        <div class="sub" id="sub">connecting…</div>
      </div>
    </div>
    <div class="header-actions">
      <div class="pill" id="status"><span class="dot"></span><span id="statusText">live</span></div>
      <div class="theme-tools">
        <button class="theme-launcher" id="themeLauncher" type="button" title="Open Theme Studio" aria-expanded="false">
          <span class="chip"></span>
          <span class="theme-launcher-copy">
            <span id="themeStudioLabel">Theme Studio</span>
            <span class="mode" id="themeModeLabel">dark · aurora</span>
          </span>
          <span class="theme-caret" aria-hidden="true"></span>
        </button>
        <div class="theme-panel" id="themePanel" aria-label="Theme selector">
          <div class="theme-head">
            <div>
              <b id="themeSelectorTitle">Theme selector</b>
              <span class="theme-summary" id="themeSummary">Dark · Aurora · Default</span>
            </div>
            <div class="theme-actions">
              <button class="btn ghost theme-random" id="themeRandom" type="button">Random</button>
              <button class="btn ghost theme-reset" id="themeReset" type="button">Reset</button>
            </div>
          </div>
          <div class="theme-preview" aria-hidden="true">
            <span class="theme-preview-swatch"></span>
            <span>
              <b id="themePreviewTitle">SOCKS5 relay</b>
              <span class="theme-preview-text" id="themePreviewText">Dark · Aurora · Default</span>
            </span>
          </div>
          <div class="theme-section">
            <div class="theme-section-title" id="themeSubtitleMode">Mode</div>
            <div class="theme-modes" id="themeModes">
              <button class="theme-mode-btn" type="button" data-mode="auto"><span class="theme-mode-icon">A</span>Auto</button>
              <button class="theme-mode-btn" type="button" data-mode="dark"><span class="theme-mode-icon">D</span>Dark</button>
              <button class="theme-mode-btn" type="button" data-mode="light"><span class="theme-mode-icon">L</span>Light</button>
            </div>
          </div>
          <div class="theme-section">
            <div class="theme-section-title" id="themeSubtitlePalette">Palette</div>
            <div class="theme-grid" id="themeGrid">
              <button class="theme-option" type="button" data-palette="aurora"><span class="theme-dot aurora"></span><span class="meta"><b>Aurora</b><span>neon night</span></span></button>
              <button class="theme-option" type="button" data-palette="ocean"><span class="theme-dot ocean"></span><span class="meta"><b>Ocean</b><span>cool blue</span></span></button>
              <button class="theme-option" type="button" data-palette="emerald"><span class="theme-dot emerald"></span><span class="meta"><b>Emerald</b><span>clean green</span></span></button>
              <button class="theme-option" type="button" data-palette="sunset"><span class="theme-dot sunset"></span><span class="meta"><b>Sunset</b><span>warm glow</span></span></button>
              <button class="theme-option" type="button" data-palette="rose"><span class="theme-dot rose"></span><span class="meta"><b>Rose</b><span>pink mint</span></span></button>
              <button class="theme-option" type="button" data-palette="cyber"><span class="theme-dot cyber"></span><span class="meta"><b>Cyber</b><span>arcade glow</span></span></button>
              <button class="theme-option" type="button" data-palette="forest"><span class="theme-dot forest"></span><span class="meta"><b>Forest</b><span>nature vibe</span></span></button>
              <button class="theme-option" type="button" data-palette="violet"><span class="theme-dot violet"></span><span class="meta"><b>Violet</b><span>dreamy purple</span></span></button>
              <button class="theme-option" type="button" data-palette="mono"><span class="theme-dot mono"></span><span class="meta"><b>Mono</b><span>minimal steel</span></span></button>
              <button class="theme-option" type="button" data-palette="lava"><span class="theme-dot lava"></span><span class="meta"><b>Lava</b><span>hot energy</span></span></button>
            </div>
          </div>
          <div class="theme-section">
            <div class="theme-section-title" id="themeSubtitleFont">Font pack</div>
            <div class="theme-modes" id="themeFonts">
              <button class="theme-mode-btn" type="button" data-font="default" data-sample="Aa">Default</button>
              <button class="theme-mode-btn" type="button" data-font="pro" data-sample="Aa">Pro UI</button>
              <button class="theme-mode-btn" type="button" data-font="readable" data-sample="Aa">Readable</button>
              <button class="theme-mode-btn" type="button" data-font="modern" data-sample="Aa">Modern</button>
              <button class="theme-mode-btn" type="button" data-font="classic" data-sample="Aa">Classic</button>
              <button class="theme-mode-btn" type="button" data-font="rounded" data-sample="Aa">Rounded</button>
              <button class="theme-mode-btn" type="button" data-font="editorial" data-sample="Aa">Editorial</button>
              <button class="theme-mode-btn" type="button" data-font="terminal" data-sample="01">Terminal</button>
              <button class="theme-mode-btn" type="button" data-font="neat" data-sample="Aa">Neat</button>
              <button class="theme-mode-btn" type="button" data-font="persian" data-sample="فا">Persian</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>

  <div class="paused-banner" id="pausedBanner">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;margin-right:6px"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>proxy is paused — new connections are refused until you re-enable it.
  </div>

  <nav class="tabs" role="tablist">
    <button class="tab active" id="tabOverview" data-tab="overview"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg></span>Overview</button>
    <button class="tab" id="tabAccess" data-tab="access"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></span>Access &amp; whitelist</button>
    <button class="tab" id="tabNetwork" data-tab="network"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg></span>Network &amp; limit</button>
    <button class="tab" id="tabSecurity" data-tab="security"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></span>Security</button>
    <button class="tab" id="tabHosts" data-tab="hosts"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9"></path><path d="M4 4a16 16 0 0 1 16 16"></path><circle cx="5" cy="19" r="1"></circle></svg></span>Destinations</button>
    <button class="tab" id="tabClients" data-tab="clients"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></span>Clients</button>
    <button class="tab" id="tabConfigs" data-tab="configs"><span class="ic"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg></span>Configs</button>
  </nav>

  <section class="tab-pane active" id="pane-overview">
    <div class="grid">
      <div class="card span-12">
        <h2><span id="hServerResources">Server resources</span> <span class="muted" id="hServerResourcesSub" style="text-transform:none;letter-spacing:0;font-weight:400">· live host snapshot</span></h2>
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
            <p class="title" id="quickStartTitle">Quick start</p>
            <p class="desc" id="quickGuideText">No traffic yet — start a client connection, then open Destinations or Clients to inspect usage.</p>
          </div>
          <div class="ux-actions">
            <button class="btn" id="goClients">Open clients</button>
            <button class="btn" id="goHosts">Open destinations</button>
            <button class="btn ghost" id="goNetwork">Open network tools</button>
          </div>
        </div>
        <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
          <span class="mini-chip"><span id="miniActiveLabel">active tunnels</span> <b id="quickActive">0</b></span>
          <span class="mini-chip"><span id="miniClientLabel">client count</span> <b id="quickClients">0</b></span>
          <span class="mini-chip"><span id="miniUpdatedLabel">last update</span> <b id="quickUpdated">--:--:--</b></span>
        </div>
      </div>

      <div class="card span-3"><h2 id="hUpload">Upload</h2>
        <div class="stat"><span class="v up" id="upSpeed">0 B/s</span>
          <span class="s"><span id="labelPeakUp">peak</span> <span id="upPeak">0 B/s</span></span></div></div>
      <div class="card span-3"><h2 id="hDownload">Download</h2>
        <div class="stat"><span class="v down" id="downSpeed">0 B/s</span>
          <span class="s"><span id="labelPeakDown">peak</span> <span id="downPeak">0 B/s</span></span></div></div>
      <div class="card span-3"><h2 id="hActiveTunnels">Active tunnels</h2>
        <div class="stat"><span class="v acc" id="active">0</span>
          <span class="s"><span id="labelPeakActive">peak</span> <span id="peakActive">0</span> · <span id="total">0</span> <span id="labelTotalConns">total</span> · <span id="rate">0.0</span>/s</span></div></div>
      <div class="card span-3"><h2 id="hUptime">Uptime</h2>
        <div class="stat"><span class="v" id="uptime">0s</span>
          <span class="s" id="labelSinceStart">since start</span></div></div>

      <div class="card span-4">
        <h2 id="hTotals">Totals</h2>
        <div class="row"><span class="muted" id="labelLiveConnections">Live connections</span>
          <span class="v acc" style="font-size:18px" id="tcpConnections">0</span></div>
        <div class="row"><span class="muted" id="labelTotalTraffic">Total</span>
          <span class="v" style="font-size:18px" id="totalBytes">0 B</span></div>
        <div class="row" style="margin-top:8px"><span class="up">↑</span>
          <span class="mono" id="upBytes">0 B</span>
          <span class="muted" id="labelAvgUp">avg</span><span class="mono" id="upAvg">0 B/s</span></div>
        <div class="row" style="margin-top:4px"><span class="down">↓</span>
          <span class="mono" id="downBytes">0 B</span>
          <span class="muted" id="labelAvgDown">avg</span><span class="mono" id="downAvg">0 B/s</span></div>
        <h2 id="hEvents" style="margin-top:16px">Events</h2>
        <div class="events">
          <div class="ev err"><b id="errors">0</b> <span id="labelErrors">errors</span></div>
          <div class="ev auth"><b id="authFail">0</b> <span id="labelAuthFail">auth fail</span></div>
          <div class="ev ref"><b id="refused">0</b> <span id="labelRefused">refused</span></div>
          <div class="ev"><b id="resets">0</b> <span id="labelResets">resets</span></div>
        </div>
      </div>

      <div class="card span-8">
        <h2><span id="hThroughput">Throughput</span>
          <span class="legend"><span class="sw up"></span> <span id="legendUp">up</span></span>
          <span class="legend"><span class="sw down"></span> <span id="legendDown">down</span></span>
        </h2>
        <canvas id="chart" height="220"></canvas>
      </div>
    </div>
  </section>

  <section class="tab-pane" id="pane-access">
    <div class="grid">
      <div class="card span-6">
        <h2><span id="hProxyWhitelist">Proxy &amp; whitelist</span>
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
        <h2 id="hWhitelistPresets">Whitelist presets</h2>
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
        <h2 id="hListener">Listener</h2>
        <div class="muted" style="font-size:12px;margin-bottom:8px">
          Currently listening on <span class="mono" id="listenAddr">…</span>
        </div>
        <div class="section-label">SOCKS port</div>
        <div class="inline-form">
          <input type="number" id="portInput" min="1" max="65535" step="1"/>
          <button class="btn primary" id="portBtn">Apply</button>
        </div>
        <div class="muted" id="listenerHint" style="font-size:11px;margin-top:4px">Rebinds the listener without restart.</div>
        <div class="section-label" style="margin-top:14px">Upstream health</div>
        <div class="inline-form">
          <button class="btn" id="upstreamCheckBtn">Check upstream</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:6px;min-height:16px" id="upstreamCheckStatus">Click to test upstream and detect public IP.</div>
      </div>

      <div class="card span-6">
        <h2 id="hTrafficLimit">Traffic limit</h2>
        <div class="inline-form">
          <input type="number" id="limitInput" min="0" step="1" placeholder="MB (0=off)"/>
          <button class="btn primary" id="limitBtn">Set</button>
          <button class="btn ghost" id="limitOff">Off</button>
        </div>
        <div class="muted" style="font-size:11px;margin-top:6px" id="limitStatus">no limit set</div>
        <div class="limit-progress"><i id="limitBar"></i></div>

        <div class="section-label" id="hBandwidthCap" style="margin-top:14px">Bandwidth cap</div>
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
        <div class="muted" id="resetHint" style="font-size:11px;margin-top:4px">
          Clears totals, peaks, per-host stats.
        </div>
      </div>

      <div class="card span-6">
        <h2 id="hConnectionCaps">Connection caps</h2>
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
        <h2 id="hGeoipLookup">GeoIP lookup</h2>
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
        <h2 id="hSocksCreds">SOCKS5 credentials</h2>
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
        <h2 id="hKillSwitch">Kill switch</h2>
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
      <h2><span id="hTopDestinations">Top destinations</span> <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">
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
      <h2><span id="hConnectedClients">Connected clients</span> <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">
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
        <h2><span id="hConfigGenerator">Config generator</span> <span class="muted" style="text-transform:none;letter-spacing:0;font-weight:400">· V2Ray JSON · Telegram · URI</span></h2>
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

  const tabs = document.querySelectorAll(".tab");
  const panes = document.querySelectorAll(".tab-pane");
  const setActiveTab = (name) => {
    tabs.forEach(x => x.classList.toggle("active", x.dataset.tab === name));
    panes.forEach(p => p.classList.toggle("active", p.id === "pane-" + name));
    if (name === "overview") requestAnimationFrame(fit);
  };
  tabs.forEach(t => t.addEventListener("click", () => setActiveTab(t.dataset.tab)));
  $("goClients").addEventListener("click", () => setActiveTab("clients"));
  $("goHosts").addEventListener("click", () => setActiveTab("hosts"));
  $("goNetwork").addEventListener("click", () => setActiveTab("network"));

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
  const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[ch]));
  const escapeAttr = escapeHtml;

  const I18N = {
    en: {
      appTitle: "SOCKS5 relay · live traffic",
      themeStudio: "Theme Studio",
      themeSelector: "Theme selector",
      random: "Random",
      palette: "Palette",
      fontPack: "Font pack (local only)",
      language: "Language",
      tabOverview: "Overview",
      tabAccess: "Access & whitelist",
      tabNetwork: "Network & limit",
      tabSecurity: "Security",
      tabHosts: "Destinations",
      tabClients: "Clients",
      tabConfigs: "Configs",
      openClients: "Open clients",
      openHosts: "Open destinations",
      openNetwork: "Open network tools",
      statusLive: "live",
      statusAuth: "auth",
      statusDenied: "denied",
      statusOffline: "offline",
      subAuth: "authentication required — redirecting to login...",
      subDenied: "panel access denied by IP ACL (allowed_panel_ips).",
      subOffline: "cannot fetch /api/stats — check server status, ACL, or auth.",
      quickNone: "No traffic yet — start a client connection, then open Destinations or Clients to inspect usage.",
      quickActive: "Relay is active now — open Clients for per-IP usage and Destinations for top domains.",
      quickPast: "Traffic was detected — explore Destinations and Clients tabs for detailed history.",
      rowNoTraffic: "no traffic yet",
      rowNoClients: "no clients yet",
      connecting: "connecting…",
      hServerResources: "Server resources",
      hServerResourcesSub: "· live host snapshot",
      quickStartTitle: "Quick start",
      miniActiveLabel: "active tunnels",
      miniClientLabel: "client count",
      miniUpdatedLabel: "last update",
      hUpload: "Upload",
      hDownload: "Download",
      hActiveTunnels: "Active tunnels",
      hUptime: "Uptime",
      hTotals: "Totals",
      hEvents: "Events",
      hThroughput: "Throughput",
      legendUp: "up",
      legendDown: "down",
      hProxyWhitelist: "Proxy & whitelist",
      hWhitelistPresets: "Whitelist presets",
      hListener: "Listener",
      listenerHint: "Rebinds the listener without restart.",
      hTrafficLimit: "Traffic limit",
      hBandwidthCap: "Bandwidth cap",
      hConnectionCaps: "Connection caps",
      hGeoipLookup: "GeoIP lookup",
      hSocksCreds: "SOCKS5 credentials",
      hKillSwitch: "Kill switch",
      hTopDestinations: "Top destinations",
      hConnectedClients: "Connected clients",
      hConfigGenerator: "Config generator",
      btnResetTraffic: "Reset traffic",
      btnCheckUpstream: "Check upstream",
      btnKillNow: "Kill now",
      btnGenerate: "Generate",
      btnUseMyIp: "Use my local IP",
      noLimitSet: "no limit set",
      noBandwidthCap: "no bandwidth cap · all tunnels share this limit",
      noCapsSet: "no caps set",
      connGlobal: "global",
      connPerClient: "per-client",
      connRefused: "refused",
      upstreamClickHint: "Click to test upstream and detect public IP.",
      upstreamChecking: "Checking upstream via IP API…",
      upstreamDownRequest: "DOWN · request failed"
    },
    fa: {
      appTitle: "SOCKS5 relay · ترافیک زنده",
      themeStudio: "استودیو تم",
      themeSelector: "انتخاب‌گر تم",
      random: "تصادفی",
      palette: "پالت رنگ",
      fontPack: "بسته فونت (لوکال)",
      language: "زبان",
      tabOverview: "نمای کلی",
      tabAccess: "دسترسی و وایت‌لیست",
      tabNetwork: "شبکه و محدودیت",
      tabSecurity: "امنیت",
      tabHosts: "مقصدها",
      tabClients: "کلاینت‌ها",
      tabConfigs: "کانفیگ‌ها",
      openClients: "رفتن به کلاینت‌ها",
      openHosts: "رفتن به مقصدها",
      openNetwork: "ابزار شبکه",
      statusLive: "آنلاین",
      statusAuth: "احراز هویت",
      statusDenied: "عدم دسترسی",
      statusOffline: "آفلاین",
      subAuth: "احراز هویت لازم است — انتقال به صفحه ورود...",
      subDenied: "دسترسی پنل توسط ACL آی‌پی مسدود شد.",
      subOffline: "دریافت /api/stats انجام نشد — وضعیت سرور، ACL یا احراز هویت را بررسی کن.",
      quickNone: "هنوز ترافیکی ثبت نشده — یک اتصال کلاینت بزن و سپس مقصدها یا کلاینت‌ها را ببین.",
      quickActive: "الان رله فعاله — برای مصرف هر آی‌پی وارد بخش کلاینت‌ها و برای دامنه‌ها وارد مقصدها شو.",
      quickPast: "قبلاً ترافیک ثبت شده — برای جزئیات تاریخچه، مقصدها و کلاینت‌ها را بررسی کن.",
      rowNoTraffic: "هنوز ترافیکی نیست",
      rowNoClients: "هنوز کلاینتی نیست",
      connecting: "در حال اتصال…",
      hServerResources: "منابع سرور",
      hServerResourcesSub: "· وضعیت زنده میزبان",
      quickStartTitle: "شروع سریع",
      miniActiveLabel: "تانل فعال",
      miniClientLabel: "تعداد کلاینت",
      miniUpdatedLabel: "آخرین بروزرسانی",
      hUpload: "آپلود",
      hDownload: "دانلود",
      hActiveTunnels: "تانل‌های فعال",
      hUptime: "زمان اجرا",
      hTotals: "مجموع",
      hEvents: "رویدادها",
      hThroughput: "نرخ انتقال",
      legendUp: "ارسال",
      legendDown: "دریافت",
      hProxyWhitelist: "پروکسی و وایت‌لیست",
      hWhitelistPresets: "پریست‌های وایت‌لیست",
      hListener: "شنونده",
      listenerHint: "بدون ری‌استارت، پورت شنونده را مجدداً bind می‌کند.",
      hTrafficLimit: "محدودیت ترافیک",
      hBandwidthCap: "سقف پهنای‌باند",
      hConnectionCaps: "سقف اتصال",
      hGeoipLookup: "جستجوی GeoIP",
      hSocksCreds: "اعتبارنامه SOCKS5",
      hKillSwitch: "کلید قطع اضطراری",
      hTopDestinations: "مقصدهای برتر",
      hConnectedClients: "کلاینت‌های متصل",
      hConfigGenerator: "سازنده کانفیگ",
      btnResetTraffic: "ریست ترافیک",
      btnCheckUpstream: "بررسی upstream",
      btnKillNow: "قطع فوری",
      btnGenerate: "تولید",
      btnUseMyIp: "استفاده از IP من",
      noLimitSet: "محدودیتی تنظیم نشده",
      noBandwidthCap: "سقف پهنای‌باند غیرفعال است · همه تانل‌ها این ظرفیت را مشترک دارند",
      noCapsSet: "سقف اتصال تنظیم نشده",
      connGlobal: "سراسری",
      connPerClient: "هر کلاینت",
      connRefused: "رد شده",
      upstreamClickHint: "برای تست upstream و تشخیص IP عمومی کلیک کن.",
      upstreamChecking: "در حال بررسی upstream از طریق IP API…",
      upstreamDownRequest: "DOWN · خطا در درخواست"
    },
    zh: {
      appTitle: "SOCKS5 中继 · 实时流量",
      themeStudio: "主题工作室",
      themeSelector: "主题选择器",
      random: "随机",
      palette: "配色",
      fontPack: "字体包（仅本地）",
      language: "语言",
      tabOverview: "概览",
      tabAccess: "访问与白名单",
      tabNetwork: "网络与限制",
      tabSecurity: "安全",
      tabHosts: "目标",
      tabClients: "客户端",
      tabConfigs: "配置",
      openClients: "打开客户端",
      openHosts: "打开目标",
      openNetwork: "打开网络工具",
      statusLive: "在线",
      statusAuth: "认证",
      statusDenied: "拒绝",
      statusOffline: "离线",
      subAuth: "需要身份验证 — 正在跳转到登录页...",
      subDenied: "面板访问被 IP ACL 拒绝。",
      subOffline: "无法获取 /api/stats — 请检查服务、ACL 或认证。",
      quickNone: "暂无流量 — 先建立客户端连接，再查看目标或客户端页。",
      quickActive: "中继当前活跃 — 打开客户端查看每 IP 用量，打开目标查看热门域名。",
      quickPast: "检测到历史流量 — 请在目标和客户端页查看详细记录。",
      rowNoTraffic: "暂无流量",
      rowNoClients: "暂无客户端",
      connecting: "连接中…",
      hServerResources: "服务器资源",
      hServerResourcesSub: "· 主机实时快照",
      quickStartTitle: "快速开始",
      miniActiveLabel: "活动隧道",
      miniClientLabel: "客户端数量",
      miniUpdatedLabel: "最后更新",
      hUpload: "上传",
      hDownload: "下载",
      hActiveTunnels: "活动隧道",
      hUptime: "运行时长",
      hTotals: "总计",
      hEvents: "事件",
      hThroughput: "吞吐量",
      legendUp: "上行",
      legendDown: "下行",
      hProxyWhitelist: "代理与白名单",
      hWhitelistPresets: "白名单预设",
      hListener: "监听器",
      listenerHint: "无需重启即可重新绑定监听端口。",
      hTrafficLimit: "流量限制",
      hBandwidthCap: "带宽上限",
      hConnectionCaps: "连接上限",
      hGeoipLookup: "GeoIP 查询",
      hSocksCreds: "SOCKS5 凭据",
      hKillSwitch: "紧急终止",
      hTopDestinations: "热门目标",
      hConnectedClients: "已连接客户端",
      hConfigGenerator: "配置生成器",
      btnResetTraffic: "重置流量",
      btnCheckUpstream: "检查上游",
      btnKillNow: "立即终止",
      btnGenerate: "生成",
      btnUseMyIp: "使用我的本机 IP",
      noLimitSet: "未设置限制",
      noBandwidthCap: "未限制带宽 · 所有隧道共享该限制",
      noCapsSet: "未设置连接上限",
      connGlobal: "全局",
      connPerClient: "每客户端",
      connRefused: "已拒绝",
      upstreamClickHint: "点击测试上游并检测公网 IP。",
      upstreamChecking: "正在通过 IP API 检查上游…",
      upstreamDownRequest: "DOWN · 请求失败"
    },
    ru: {
      appTitle: "SOCKS5 relay · живой трафик",
      themeStudio: "Студия тем",
      themeSelector: "Выбор темы",
      random: "Случайно",
      palette: "Палитра",
      fontPack: "Набор шрифтов (локально)",
      language: "Язык",
      tabOverview: "Обзор",
      tabAccess: "Доступ и whitelist",
      tabNetwork: "Сеть и лимиты",
      tabSecurity: "Безопасность",
      tabHosts: "Назначения",
      tabClients: "Клиенты",
      tabConfigs: "Конфиги",
      openClients: "Открыть клиентов",
      openHosts: "Открыть назначения",
      openNetwork: "Сетевые инструменты",
      statusLive: "онлайн",
      statusAuth: "авторизация",
      statusDenied: "доступ запрещён",
      statusOffline: "оффлайн",
      subAuth: "требуется авторизация — переход на страницу входа...",
      subDenied: "доступ к панели запрещён IP ACL.",
      subOffline: "не удаётся получить /api/stats — проверьте сервер, ACL или авторизацию.",
      quickNone: "Трафика пока нет — подключите клиент и откройте разделы назначений/клиентов.",
      quickActive: "Релей активен — откройте Клиенты и Назначения для подробностей.",
      quickPast: "Обнаружен прошлый трафик — изучите историю в разделах назначений и клиентов.",
      rowNoTraffic: "трафика пока нет",
      rowNoClients: "клиентов пока нет",
      connecting: "подключение…",
      hServerResources: "Ресурсы сервера",
      hServerResourcesSub: "· живой снимок хоста",
      quickStartTitle: "Быстрый старт",
      miniActiveLabel: "активные туннели",
      miniClientLabel: "число клиентов",
      miniUpdatedLabel: "последнее обновление",
      hUpload: "Отправка",
      hDownload: "Загрузка",
      hActiveTunnels: "Активные туннели",
      hUptime: "Время работы",
      hTotals: "Итого",
      hEvents: "События",
      hThroughput: "Пропускная способность",
      legendUp: "вверх",
      legendDown: "вниз",
      hProxyWhitelist: "Прокси и whitelist",
      hWhitelistPresets: "Пресеты whitelist",
      hListener: "Слушатель",
      listenerHint: "Перепривязка порта слушателя без перезапуска.",
      hTrafficLimit: "Лимит трафика",
      hBandwidthCap: "Лимит пропускной",
      hConnectionCaps: "Ограничения подключений",
      hGeoipLookup: "GeoIP поиск",
      hSocksCreds: "Учётные данные SOCKS5",
      hKillSwitch: "Аварийный стоп",
      hTopDestinations: "Топ направлений",
      hConnectedClients: "Подключённые клиенты",
      hConfigGenerator: "Генератор конфигов",
      btnResetTraffic: "Сбросить трафик",
      btnCheckUpstream: "Проверить upstream",
      btnKillNow: "Остановить",
      btnGenerate: "Сгенерировать",
      btnUseMyIp: "Использовать мой локальный IP",
      noLimitSet: "лимит не задан",
      noBandwidthCap: "лимит пропускной не задан · все туннели делят общий лимит",
      noCapsSet: "лимиты подключений не заданы",
      connGlobal: "глобально",
      connPerClient: "на клиента",
      connRefused: "отклонено",
      upstreamClickHint: "Нажмите, чтобы проверить upstream и узнать публичный IP.",
      upstreamChecking: "Проверка upstream через IP API…",
      upstreamDownRequest: "DOWN · ошибка запроса"
    }
  };
  let currentLang = "en";
  const tr = key => ((I18N[currentLang] && I18N[currentLang][key]) || I18N.en[key] || key);

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
    if (!hosts.length) { tb.innerHTML = `<tr><td colspan="7" class="muted">no traffic yet</td></tr>`; return; }
    const mx = Math.max(1, ...hosts.map(h => h.up + h.down));
    const flagOf = cc => {
      if (!cc || cc.length !== 2) return "";
      const A = 127397;
      return String.fromCodePoint(cc.charCodeAt(0)+A) + String.fromCodePoint(cc.charCodeAt(1)+A);
    };
    tb.innerHTML = hosts.map((h,i) => {
      const total = h.up + h.down, ratio = total / mx;
      const flag = flagOf((h.cc || "").toUpperCase());
      const countryTitle = h.country ? ` title="${escapeAttr(h.country)}"` : "";
      const hostCell = flag
        ? `<span${countryTitle} style="margin-right:6px">${escapeHtml(flag)}</span><span class="mono">${escapeHtml(h.host)}</span>`
        : `<span class="mono">${escapeHtml(h.host)}</span>`;
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
    if (!clients.length) { tb.innerHTML = `<tr><td colspan="7" class="muted">no clients yet</td></tr>`; return; }
    const mx = Math.max(1, ...clients.map(c => c.bytes_up + c.bytes_down));
    tb.innerHTML = clients.map((c,i) => {
      const total = c.bytes_up + c.bytes_down, ratio = total / mx;
      return `<tr>
        <td><span class="dot ${c.active_tunnels>0?'on':'off'}"></span></td>
        <td class="mono muted">${i+1}</td>
        <td class="mono">${escapeHtml(c.ip)}</td>
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

  let lastCtrl = {};
  let portDirty = false, limitDirty = false, userDirty = false, bwDirty = false;
  let connTotalDirty = false, connPerDirty = false;
  $("portInput").addEventListener("input", () => portDirty = true);
  $("limitInput").addEventListener("input", () => limitDirty = true);
  $("userInput").addEventListener("input", () => userDirty = true);
  $("bwInput").addEventListener("input", () => bwDirty = true);
  $("connTotalInput").addEventListener("input", () => connTotalDirty = true);
  $("connPerInput").addEventListener("input", () => connPerDirty = true);

  const themeModeLabel = $("themeModeLabel");
  const themeSummary = $("themeSummary");
  const themePreviewText = $("themePreviewText");
  const themeLauncher = $("themeLauncher");
  const themePanel = $("themePanel");
  const themeOptions = document.querySelectorAll(".theme-option");
  const themeFontButtons = document.querySelectorAll("#themeFonts .theme-mode-btn");
  const themeModeButtons = document.querySelectorAll("#themeModes .theme-mode-btn");
  const THEME_PALETTES = ["aurora", "ocean", "emerald", "sunset", "rose", "cyber", "forest", "violet", "mono", "lava"];
  const THEME_FONTS = ["default", "pro", "readable", "modern", "classic", "rounded", "editorial", "terminal", "neat", "persian"];

  const getEffectiveTheme = mode => {
    const m = (mode || "dark").toLowerCase();
    if (m !== "auto") return (m === "light" ? "light" : "dark");
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches)
      ? "light"
      : "dark";
  };

  const themeName = value => String(value || "")
    .replace(/-/g, " ")
    .replace(/\b\w/g, ch => ch.toUpperCase());

  const syncThemeControls = (mode, palette, font) => {
    const label = `${themeName(mode)} · ${themeName(palette)} · ${themeName(font)}`;
    themeModeButtons.forEach(btn => {
      const active = btn.dataset.mode === mode;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
    themeOptions.forEach(btn => {
      const active = btn.dataset.palette === palette;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
    themeFontButtons.forEach(btn => {
      const active = btn.dataset.font === font;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
    if (themeModeLabel) themeModeLabel.textContent = `${themeName(mode)} · ${themeName(palette)}`;
    if (themeSummary) themeSummary.textContent = label;
    if (themePreviewText) themePreviewText.textContent = label;
  };

  const applyTheme = (mode, palette, font, persist=true) => {
    const requestedMode = mode || localStorage.getItem("s5themePref") || localStorage.getItem("s5theme") || "dark";
    const requestedPalette = palette || localStorage.getItem("s5palette") || "aurora";
    const requestedFont = font || localStorage.getItem("s5font") || "default";
    const nextMode = ["auto", "dark", "light"].includes(requestedMode) ? requestedMode : "dark";
    const nextPalette = THEME_PALETTES.includes(requestedPalette) ? requestedPalette : "aurora";
    const nextFont = THEME_FONTS.includes(requestedFont) ? requestedFont : "default";
    const effectiveTheme = getEffectiveTheme(nextMode);
    document.documentElement.setAttribute("data-theme", effectiveTheme);
    document.documentElement.setAttribute("data-accent", nextPalette);
    document.documentElement.setAttribute("data-font", nextFont);
    syncThemeControls(nextMode, nextPalette, nextFont);
    if (persist) {
      try {
        localStorage.setItem("s5themePref", nextMode);
        localStorage.setItem("s5theme", effectiveTheme);
        localStorage.setItem("s5palette", nextPalette);
        localStorage.setItem("s5font", nextFont);
      } catch(e) {}
    }
    requestAnimationFrame(() => draw(lastSparkUp, lastSparkDown));
  };

  const toggleThemePanel = force => {
    const open = typeof force === "boolean" ? force : !themePanel.classList.contains("open");
    themePanel.classList.toggle("open", open);
    themeLauncher.setAttribute("aria-expanded", open ? "true" : "false");
  };

  themeLauncher.addEventListener("click", e => {
    e.stopPropagation();
    toggleThemePanel();
  });

  document.addEventListener("click", e => {
    if (!themePanel.classList.contains("open")) return;
    if (themePanel.contains(e.target) || themeLauncher.contains(e.target)) return;
    toggleThemePanel(false);
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape") toggleThemePanel(false);
  });

  themeModeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const palette = document.documentElement.getAttribute("data-accent") || "aurora";
      const font = document.documentElement.getAttribute("data-font") || "default";
      applyTheme(btn.dataset.mode || "dark", palette, font, true);
    });
  });

  themeOptions.forEach(btn => {
    btn.addEventListener("click", () => {
      const mode = localStorage.getItem("s5themePref") || localStorage.getItem("s5theme") || "dark";
      const font = document.documentElement.getAttribute("data-font") || "default";
      applyTheme(mode, btn.dataset.palette || "aurora", font, true);
    });
  });

  themeFontButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const mode = localStorage.getItem("s5themePref") || localStorage.getItem("s5theme") || "dark";
      const palette = document.documentElement.getAttribute("data-accent") || "aurora";
      applyTheme(mode, palette, btn.dataset.font || "default", true);
    });
  });

  $("themeRandom").addEventListener("click", () => {
    const mode = localStorage.getItem("s5themePref") || localStorage.getItem("s5theme") || "dark";
    const current = document.documentElement.getAttribute("data-accent") || "aurora";
    const font = document.documentElement.getAttribute("data-font") || "default";
    const pool = THEME_PALETTES.filter(x => x !== current);
    const next = pool[Math.floor(Math.random() * pool.length)] || "aurora";
    applyTheme(mode, next, font, true);
  });

  $("themeReset").addEventListener("click", () => {
    try {
      localStorage.removeItem("s5themePref");
      localStorage.removeItem("s5theme");
      localStorage.removeItem("s5palette");
      localStorage.removeItem("s5font");
    } catch(e) {}
    applyTheme("dark", "aurora", "default", true);
  });

  const initialMode = localStorage.getItem("s5themePref") || localStorage.getItem("s5theme") || "dark";
  const initialPalette = localStorage.getItem("s5palette") || document.documentElement.getAttribute("data-accent") || "aurora";
  const initialFont = localStorage.getItem("s5font") || document.documentElement.getAttribute("data-font") || "default";
  applyTheme(initialMode, initialPalette, initialFont, false);

  try {
    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", () => {
        const mode = localStorage.getItem("s5themePref") || "dark";
        if (mode === "auto") applyTheme(
          mode,
          document.documentElement.getAttribute("data-accent") || "aurora",
          document.documentElement.getAttribute("data-font") || "default",
          false,
        );
      });
    }
  } catch(e) {}

  const post = async (action, params={}, refresh=true) => {
    try {
      const r = await fetch("/api/control", {
        method:"POST", headers:{"Content-Type":"application/json"},
        body: JSON.stringify({action, ...params}),
      });
      const j = await r.json().catch(()=>({}));
      if (!j.ok) console.warn("control failed", action, j);
      if (refresh) tick();
      return j;
    } catch(e) { console.warn("control error", e); return {}; }
  };

  const loadCredentials = async () => {
    const j = await post("get_credentials", {}, false);
    if (j && j.ok) {
      window.__liveUser = j.username || "";
      window.__livePass = j.password || "";
    }
    return j || {};
  };

  const applyControls = (c, totalBytes) => {
    lastCtrl = c;
    $("listenAddr").textContent = (c.listen_host || "?") + ":" + (c.listen_port || "?");
    $("bypassBadge").textContent = "bypassed " + (c.bypassed || 0)
      + (c.bypassed_active ? " (" + c.bypassed_active + " live)" : "");

    const tgP = $("tgProxy");
    tgP.classList.toggle("ok", !!c.proxy_enabled);
    tgP.classList.remove("danger");
    $("pausedBanner").classList.toggle("show", !c.proxy_enabled);

    $("tgWhitelist").classList.toggle("on", !!c.whitelist_enabled);
    const tgS = $("tgStrict");
    tgS.classList.toggle("on", !!c.whitelist_strict);
    tgS.classList.toggle("danger", !!c.whitelist_strict);
    $("tgIr").classList.toggle("ok", !!c.ir_redirect);

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

    if (!portDirty) $("portInput").value = c.listen_port || "";

    const u = c.username || "";
    const pw = window.__livePass || "";
    const pwSet = !!c.password_set || !!pw;
    window.__liveUser = u || window.__liveUser || "";
    $("currentUser").textContent = u || "—";
    $("credsUser").textContent = u || "—";
    const revealed = window.__credsRevealed === true;
    $("credsPass").textContent = revealed
      ? (pw || (pwSet ? "click Show to load" : "—"))
      : (pwSet ? "•".repeat(pw ? Math.min(pw.length, 12) : 8) : "—");
    if (!userDirty) $("userInput").value = u;

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

    const bps = c.bandwidth_limit_bps || 0;
    if (!bwDirty) $("bwInput").value = bps ? Math.round(bps / 1024) : "";
    const bwS = $("bwStatus");
    if (bps > 0) {
      const kb = bps / 1024;
      bwS.textContent = `cap: ${kb >= 1024 ? (kb/1024).toFixed(2) + " MB/s" : kb.toFixed(0) + " KB/s"} · shared across all tunnels`;
    } else {
      bwS.textContent = "no bandwidth cap · all tunnels share this limit";
    }

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

    $("tgGeoip").classList.toggle("ok", !!c.geoip_enabled);

    const tgA = $("tgAuth");
    const authOn = c.auth_required !== false;
    tgA.classList.toggle("ok", authOn);
    tgA.classList.toggle("danger", !authOn);
  };

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

  $("portBtn").addEventListener("click", async () => {
    const port = parseInt($("portInput").value, 10);
    if (!port || port < 1 || port > 65535) { alert("Port must be 1-65535"); return; }
    const j = await post("change_port", {port});
    portDirty = false;
    if (j && j.ok === false) alert("Port change failed: " + (j.error || "unknown"));
  });

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

  $("tgGeoip").addEventListener("click", () => {
    post("set_geoip", {enabled: !lastCtrl.geoip_enabled});
  });

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

  $("resetBtn").addEventListener("click", async () => {
    if (confirm("Reset all traffic counters (up/down totals, peaks, per-host)?")) {
      await post("reset_traffic");
    }
  });

  $("killBtn").addEventListener("click", async () => {
    if (!confirm("⚠ This will TERMINATE the relay process immediately.\nAll active tunnels will drop. Continue?")) return;
    await post("kill");
    $("status").classList.add("bad");
    $("statusText").textContent = "terminated";
  });

  $("passReveal").addEventListener("click", () => {
    const p = $("passInput");
    p.type = (p.type === "password") ? "text" : "password";
  });
  $("credsReveal").addEventListener("click", async () => {
    window.__credsRevealed = !window.__credsRevealed;
    $("credsRevealLabel").textContent = window.__credsRevealed ? "Hide" : "Show";
    if (!window.__credsRevealed) {
      window.__livePass = "";
    }
    if (window.__credsRevealed && !window.__livePass) {
      await loadCredentials();
    }
    const pw = window.__livePass || "";
    $("credsPass").textContent = window.__credsRevealed
      ? (pw || "—")
      : (pw ? "•".repeat(Math.min(pw.length, 12)) : "—");
  });
  $("credsCopy").addEventListener("click", async () => {
    if (!window.__livePass) await loadCredentials();
    const u = window.__liveUser || $("credsUser").textContent.trim();
    const pw = window.__livePass || "";
    if (!u || !pw) return;
    try {
      await navigator.clipboard.writeText(u + ":" + pw);
      if (!window.__credsRevealed) window.__livePass = "";
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
      window.__livePass = "";
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

  const cfgBuild = async () => {
    const host = ($("cfgHost").value || "").trim();
    const port = parseInt($("cfgPort").value, 10);
    const tag  = ($("cfgTag").value || "socks-relay").trim() || "socks-relay";
    const st   = $("cfgStatus");
    if (!host || !port || port < 1 || port > 65535) {
      st.textContent = "✖ enter a valid host and port";
      st.style.color = "var(--bad)";
      return;
    }
    const creds = await loadCredentials();
    const user = (creds && creds.username) || (lastCtrl && lastCtrl.username) || "";
    const pass = (creds && creds.password) || "";
    if (!user || !pass) {
      st.textContent = "✖ server credentials not loaded yet";
      st.style.color = "var(--bad)";
      return;
    }
    st.style.color = "var(--good)";
    st.textContent = "✓ generated — credentials pulled from live relay";

    const pwShown = pass;

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

    const tgParams = new URLSearchParams({
      server: host, port: String(port), user: user, pass: pwShown
    }).toString();
    $("outTelegram").textContent =
      "https://t.me/socks?" + tgParams + "\n" +
      "tg://socks?" + tgParams;

    const enc = encodeURIComponent;
    const utf8 = new TextEncoder().encode(user + ":" + pwShown);
    let bin = "";
    for (let i = 0; i < utf8.length; i++) bin += String.fromCharCode(utf8[i]);
    const b64 = btoa(bin);
    const remark = enc(tag);
    $("outUri").textContent =
      `socks://${b64}@${host}:${port}#${remark}\n` +
      `socks5://${enc(user)}:${enc(pwShown)}@${host}:${port}`;

    $("outCurl").textContent =
      `curl -x socks5h://${enc(user)}:${enc(pwShown)}@${host}:${port} https://ifconfig.me\n` +
      `curl --proxy-user ${user}:${pwShown} --socks5-hostname ${host}:${port} https://api.ipify.org`;
    if (!window.__credsRevealed) window.__livePass = "";
  };

  $("cfgBuildBtn").addEventListener("click", cfgBuild);
  $("cfgHost").addEventListener("keydown", e => { if (e.key === "Enter") cfgBuild(); });
  $("cfgPort").addEventListener("keydown", e => { if (e.key === "Enter") cfgBuild(); });
  $("cfgTag").addEventListener("keydown",  e => { if (e.key === "Enter") cfgBuild(); });

  $("cfgFillMine").addEventListener("click", () => {
    $("cfgHost").value = location.hostname || "";
    if (!$("cfgPort").value && lastCtrl && lastCtrl.listen_port) {
      $("cfgPort").value = lastCtrl.listen_port;
    }
    cfgBuild();
  });

  document.querySelectorAll(".cfg-copy").forEach(btn => {
    btn.addEventListener("click", async () => {
      const tgt = $(btn.dataset.target);
      if (!tgt) return;
      const text = tgt.textContent || "";
      try {
        await navigator.clipboard.writeText(text);
      } catch (e) {
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

  const cfgSeed = setInterval(() => {
    if (lastCtrl && lastCtrl.listen_port) {
      if (!$("cfgPort").value) $("cfgPort").value = lastCtrl.listen_port;
      if (!$("cfgHost").value) $("cfgHost").value = location.hostname || "";
      clearInterval(cfgSeed);
    }
  }, 500);

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
