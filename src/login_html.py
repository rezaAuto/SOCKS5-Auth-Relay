"""Standalone login-page HTML used by the web dashboard."""

LOGIN_HTML: str = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>SOCKS5 relay · sign in</title>
<style>
:root{--bg:#07090d;--panel:#131822;--border:#262d3d;--text:#e6edf3;--muted:#8b949e;--accent:#d2a0ff;--down:#5ac8fa;--bad:#f07878}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);
    font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
  min-height:100vh;display:flex;align-items:center;justify-content:center;
  background:
    radial-gradient(1000px 500px at 10% -10%,rgba(90,200,250,.14),transparent 55%),
    radial-gradient(900px 500px at 110% 10%,rgba(210,160,255,.10),transparent 60%),
    var(--bg)}
.card{background:linear-gradient(180deg,#161c28,#10151e);border:1px solid var(--border);
  border-radius:16px;padding:28px;width:360px;
  box-shadow:0 24px 60px -12px rgba(0,0,0,.6),0 8px 20px -4px rgba(0,0,0,.4),
             inset 0 1px 0 rgba(255,255,255,.05)}
h1{margin:0 0 4px;font-size:18px;font-weight:700;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:12px;margin-bottom:20px}
label{display:block;font-size:11px;color:var(--muted);text-transform:uppercase;
  letter-spacing:.08em;margin:12px 0 6px}
input{width:100%;background:#070a10;border:1px solid var(--border);border-radius:10px;
    color:var(--text);padding:10px 12px;font-family:ui-monospace,Consolas,monospace;
  font-size:13px;outline:none;transition:border-color .15s,box-shadow .15s}
input:focus{border-color:var(--down);box-shadow:0 0 0 3px rgba(90,200,250,.15)}
button{margin-top:18px;width:100%;background:linear-gradient(180deg,var(--accent),#a677e0);
  color:#1a0a2a;border:0;border-radius:10px;padding:11px 14px;font-weight:700;font-size:13px;
  cursor:pointer;letter-spacing:.02em;transition:transform .1s,box-shadow .2s;
    font-family:ui-sans-serif,system-ui,"Segoe UI",sans-serif}
button:hover{box-shadow:0 8px 20px -6px rgba(210,160,255,.5)}
button:active{transform:translateY(1px)}
.err{color:var(--bad);font-size:12px;margin-top:12px;min-height:16px}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.brand .dot{width:28px;height:28px;border-radius:8px;
  background:linear-gradient(135deg,var(--down),var(--accent));
  display:flex;align-items:center;justify-content:center;color:#0a0d14;font-weight:800;font-size:15px}
</style></head>
<body><div class="card">
  <div class="brand"><div class="dot">S5</div><div><div style="font-weight:700">SOCKS5 relay</div><div class="sub" style="margin:0">dashboard access</div></div></div>
  <h1>Sign in</h1>
  <div class="sub">Use the dashboard credentials from settings.json (login_user / login_password).</div>
  <form method="POST" action="/login" autocomplete="off">
    <label for="u">Username</label>
    <input id="u" name="username" required autofocus spellcheck="false" autocapitalize="off" />
    <label for="p">Password</label>
    <input id="p" name="password" type="password" required />
    <button type="submit">Sign in</button>
    <div class="err">__ERROR__</div>
  </form>
</div></body></html>
"""


def render_login_page(error: str = "") -> bytes:
    """Render login HTML bytes with safe inline error substitution."""
    safe = (error or "").replace("<", "&lt;").replace(">", "&gt;")
    return LOGIN_HTML.replace("__ERROR__", safe).encode("utf-8")
