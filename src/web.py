from __future__ import annotations

import asyncio
import ctypes
import json
import logging
import os
import secrets
import shutil
import threading
import time
from typing import Optional

from dashboard_html import _WEB_INDEX_HTML
# Login page markup was extracted to keep this transport/control file smaller.
from login_html import render_login_page
from utils import close_writer

from controls import (
    CONTROLS,
    apply_control_action,
    get_control_plane,
)
from stats import STATS
from whitelist import WHITELIST_CIDRS, WHITELIST_PRESETS

LOGGER = logging.getLogger("socks5_auth_relay")

_WEB_AUTH_ENABLED: bool = False
_WEB_AUTH_USER: str = ""
_WEB_AUTH_PASS: str = ""
_WEB_SESSIONS: dict[str, float] = {}
_SESSION_TTL: float = 12 * 3600.0
_COOKIE_NAME: str = "socks5_dash_sid"
_PANEL_IP_RESTRICTED: bool = False
_PANEL_ALLOWED_IPS: set[str] = set()
_WIN_CPU_LOCK = threading.Lock()
_WIN_CPU_LAST: tuple[int, int, int] | None = None
_WIN_CPU_LAST_PCT: float = 0.0


class _FILETIME(ctypes.Structure):
    _fields_ = [
        ("dwLowDateTime", ctypes.c_uint32),
        ("dwHighDateTime", ctypes.c_uint32),
    ]


class _MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_uint32),
        ("dwMemoryLoad", ctypes.c_uint32),
        ("ullTotalPhys", ctypes.c_uint64),
        ("ullAvailPhys", ctypes.c_uint64),
        ("ullTotalPageFile", ctypes.c_uint64),
        ("ullAvailPageFile", ctypes.c_uint64),
        ("ullTotalVirtual", ctypes.c_uint64),
        ("ullAvailVirtual", ctypes.c_uint64),
        ("ullAvailExtendedVirtual", ctypes.c_uint64),
    ]


def _ft_to_int(ft: _FILETIME) -> int:
    return (int(ft.dwHighDateTime) << 32) | int(ft.dwLowDateTime)


def _windows_cpu_percent() -> float:
    global _WIN_CPU_LAST_PCT

    def _sample() -> tuple[int, int, int] | None:
        try:
            kernel32 = ctypes.windll.kernel32
            idle_ft = _FILETIME()
            kernel_ft = _FILETIME()
            user_ft = _FILETIME()
            ok = kernel32.GetSystemTimes(
                ctypes.byref(idle_ft),
                ctypes.byref(kernel_ft),
                ctypes.byref(user_ft),
            )
            if not ok:
                return None
            return _ft_to_int(idle_ft), _ft_to_int(kernel_ft), _ft_to_int(user_ft)
        except Exception:
            return None

    with _WIN_CPU_LOCK:
        first = _sample()
        if first is None:
            return _WIN_CPU_LAST_PCT

        time.sleep(0.08)

        second = _sample()
        if second is None:
            return _WIN_CPU_LAST_PCT

        idle1, kernel1, user1 = first
        idle2, kernel2, user2 = second
        delta_idle = max(0, idle2 - idle1)
        delta_kernel = max(0, kernel2 - kernel1)
        delta_user = max(0, user2 - user1)
        total = delta_kernel + delta_user
        if total <= 0:
            return _WIN_CPU_LAST_PCT

        busy = max(0, total - delta_idle)
        pct = max(0.0, min(100.0, (busy / total) * 100.0))
        _WIN_CPU_LAST_PCT = pct
        return pct


def _windows_memory_snapshot() -> tuple[int, int, int, int]:
    try:
        mem = _MEMORYSTATUSEX()
        mem.dwLength = ctypes.sizeof(_MEMORYSTATUSEX)
        ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
        if not ok:
            return 0, 0, 0, 0

        ram_total = int(mem.ullTotalPhys)
        ram_used = max(0, ram_total - int(mem.ullAvailPhys))

        total_page_only = max(0, int(mem.ullTotalPageFile) - int(mem.ullTotalPhys))
        avail_page_only = max(0, int(mem.ullAvailPageFile) - int(mem.ullAvailPhys))
        swap_total = total_page_only
        swap_used = max(0, swap_total - avail_page_only)
        return ram_total, ram_used, swap_total, swap_used
    except Exception:
        return 0, 0, 0, 0


def set_web_auth(enabled: bool, username: str, password: str) -> None:
    global _WEB_AUTH_ENABLED, _WEB_AUTH_USER, _WEB_AUTH_PASS
    _WEB_AUTH_ENABLED = bool(enabled)
    _WEB_AUTH_USER = username or ""
    _WEB_AUTH_PASS = password or ""
    if enabled:
        LOGGER.info("Web dashboard login is ENABLED")
    else:
        LOGGER.info("Web dashboard login is disabled (open access)")


def set_panel_ip_acl(restricted: bool, allowed_ips: list[str]) -> None:
    global _PANEL_IP_RESTRICTED, _PANEL_ALLOWED_IPS
    _PANEL_IP_RESTRICTED = bool(restricted)
    _PANEL_ALLOWED_IPS = {str(ip).strip() for ip in (allowed_ips or []) if str(ip).strip()}
    if _PANEL_IP_RESTRICTED:
        LOGGER.info("Web dashboard IP ACL enabled for: %s", ", ".join(sorted(_PANEL_ALLOWED_IPS)) or "<none>")
        if not _PANEL_ALLOWED_IPS:
            LOGGER.warning("Web dashboard IP ACL has no allowed IPs; all dashboard requests will be denied")
    else:
        LOGGER.info("Web dashboard IP ACL disabled")


def _gc_sessions() -> None:
    now = time.monotonic()
    expired = [t for t, exp in _WEB_SESSIONS.items() if exp < now]
    for t in expired:
        _WEB_SESSIONS.pop(t, None)


def _issue_session() -> str:
    _gc_sessions()
    token = secrets.token_urlsafe(32)
    _WEB_SESSIONS[token] = time.monotonic() + _SESSION_TTL
    return token


def _session_valid(token: str) -> bool:
    if not token:
        return False
    exp = _WEB_SESSIONS.get(token)
    if exp is None:
        return False
    if exp < time.monotonic():
        _WEB_SESSIONS.pop(token, None)
        return False
    return True


def _parse_cookies(header_value: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for piece in header_value.split(";"):
        if "=" not in piece:
            continue
        k, _, v = piece.strip().partition("=")
        if k:
            out[k] = v
    return out


def _parse_form_urlencoded(raw: bytes) -> dict[str, str]:
    import urllib.parse
    try:
        pairs = urllib.parse.parse_qsl(raw.decode("utf-8", "replace"),
                                       keep_blank_values=True,
                                       strict_parsing=False)
    except ValueError:
        return {}
    out: dict[str, str] = {}
    for k, v in pairs:
        out[k] = v
    return out


def _geo_for(host_port: str) -> dict[str, str]:
    try:
        from geoip import GEO_CACHE
    except Exception:
        return {"cc": "", "country": ""}
    host = host_port.rsplit(":", 1)[0].strip().strip(".").lower()
    entry = GEO_CACHE.get(host)
    if not entry:
        return {"cc": "", "country": ""}
    return {"cc": entry.get("cc", ""), "country": entry.get("country", "")}


def _system_snapshot_dict() -> dict:
    cpu_count = max(1, os.cpu_count() or 1)
    if os.name == "nt":
        cpu_percent = _windows_cpu_percent()
    else:
        try:
            load1 = os.getloadavg()[0]
            cpu_percent = max(0.0, min(100.0, (load1 / cpu_count) * 100.0))
        except (AttributeError, OSError):
            cpu_percent = 0.0

    ram_total = 0
    ram_used = 0
    swap_total = 0
    swap_used = 0

    if os.name == "nt":
        ram_total, ram_used, swap_total, swap_used = _windows_memory_snapshot()
    else:
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as fh:
                meminfo: dict[str, int] = {}
                for line in fh:
                    key, _, rest = line.partition(":")
                    val = rest.strip().split()[0] if rest.strip() else "0"
                    meminfo[key] = int(val) * 1024
            ram_total = int(meminfo.get("MemTotal", 0))
            mem_available = int(meminfo.get("MemAvailable", 0))
            ram_used = max(0, ram_total - mem_available)
            swap_total = int(meminfo.get("SwapTotal", 0))
            swap_free = int(meminfo.get("SwapFree", 0))
            swap_used = max(0, swap_total - swap_free)
        except (OSError, ValueError):
            pass

    disk_path = os.getcwd()
    if os.name == "nt":
        drive, _ = os.path.splitdrive(disk_path)
        if drive:
            disk_path = drive + "\\"
    else:
        disk_path = "/"

    storage_total = 0
    storage_used = 0
    try:
        usage = shutil.disk_usage(disk_path)
        storage_total = int(usage.total)
        storage_used = int(usage.used)
    except OSError:
        pass

    return {
        "cpu_percent": cpu_percent,
        "cpu_cores": cpu_count,
        "ram_used": ram_used,
        "ram_total": ram_total,
        "swap_used": swap_used,
        "swap_total": swap_total,
        "storage_used": storage_used,
        "storage_total": storage_total,
    }


def _stats_snapshot_dict(listen_addr: str, upstream_addr: str) -> dict:
    up_bps = float(STATS.spark_up[-1]) if STATS.spark_up else float(STATS.ema_up_bps)
    down_bps = float(STATS.spark_down[-1]) if STATS.spark_down else float(STATS.ema_down_bps)

    hosts = []
    for host, hs in sorted(
        STATS.hosts.items(),
        key=lambda item: (-(item[1].bytes_up + item[1].bytes_down), item[0].lower()),
    ):
        geo = _geo_for(host)
        hosts.append({
            "host": host,
            "up": int(hs.bytes_up),
            "down": int(hs.bytes_down),
            "active": int(hs.active),
            "total": int(hs.total),
            "cc": geo.get("cc", ""),
            "country": geo.get("country", ""),
        })

    clients = []
    for ip, cs in sorted(
        STATS.clients.items(),
        key=lambda item: (-(item[1].bytes_up + item[1].bytes_down), item[0]),
    ):
        clients.append({
            "ip": ip,
            "bytes_up": int(cs.bytes_up),
            "bytes_down": int(cs.bytes_down),
            "active_tunnels": int(cs.active_tunnels),
            "total_tunnels": int(cs.total_tunnels),
        })

    return {
        "listen": listen_addr,
        "upstream": upstream_addr,
        "uptime": max(0.0, time.monotonic() - STATS.started_at),
        "up_bps": max(0.0, up_bps),
        "down_bps": max(0.0, down_bps),
        "peak_up_bps": max(0.0, float(STATS.peak_up_bps)),
        "peak_down_bps": max(0.0, float(STATS.peak_down_bps)),
        "avg_up_bps": max(0.0, float(STATS.ema_up_bps)),
        "avg_down_bps": max(0.0, float(STATS.ema_down_bps)),
        "bytes_up": int(STATS.bytes_up),
        "bytes_down": int(STATS.bytes_down),
        "active": int(STATS.active),
        "peak_active": int(STATS.peak_active),
        "total": int(STATS.total),
        "errors": int(STATS.errors),
        "auth_fail": int(STATS.auth_fail),
        "refused": int(STATS.refused),
        "reset": int(STATS.reset),
        "conns_per_sec": float(STATS.conns_per_sec),
        "host_count": len(hosts),
        "client_count": len(clients),
        "spark_up": [float(v) for v in STATS.spark_up],
        "spark_down": [float(v) for v in STATS.spark_down],
        "hosts": hosts,
        "clients": clients,
        "system": _system_snapshot_dict(),
        "controls": _controls_snapshot_dict(),
    }


def _controls_snapshot_dict() -> dict:
    username = ""
    password_set = False
    plane = get_control_plane()
    if plane is not None:
        try:
            username = plane.get_username() or ""
        except Exception:
            username = ""
        try:
            password_set = bool(plane.get_password() or "")
        except Exception:
            password_set = False
    return {
        "proxy_enabled": CONTROLS.proxy_enabled,
        "whitelist_enabled": CONTROLS.whitelist_enabled,
        "whitelist_strict": CONTROLS.whitelist_strict,
        "ir_redirect": CONTROLS.ir_redirect,
        "presets": {name: (name in CONTROLS.presets) for name in WHITELIST_PRESETS},
        "preset_domains": {name: sorted(WHITELIST_PRESETS[name]) for name in WHITELIST_PRESETS},
        "preset_cidrs": {
            name: (len(v4) + len(v6))
            for name, (v4, v6) in WHITELIST_CIDRS.items()
        },
        "custom_domains": sorted(CONTROLS.custom_domains),
        "traffic_limit_bytes": CONTROLS.traffic_limit_bytes,
        "bandwidth_limit_bps": CONTROLS.bandwidth_limit_bps,
        "max_conn_total": CONTROLS.max_conn_total,
        "max_conn_per_client": CONTROLS.max_conn_per_client,
        "conn_refused": CONTROLS.conn_refused,
        "geoip_enabled": CONTROLS.geoip_enabled,
        "auth_required": CONTROLS.auth_required,
        "bypassed": CONTROLS.bypassed,
        "bypassed_active": CONTROLS.bypassed_active,
        "listen_host": CONTROLS.listen_host,
        "listen_port": CONTROLS.listen_port,
        "username": username,
        "password_set": password_set,
    }


async def _web_handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    listen_addr: str,
    upstream_addr: str,
) -> None:
    client_ip = ""
    try:
        peername = writer.get_extra_info("peername")
        if isinstance(peername, (tuple, list)) and peername:
            client_ip = str(peername[0])
    except Exception:
        pass

    if _PANEL_IP_RESTRICTED and client_ip not in _PANEL_ALLOWED_IPS:
        LOGGER.warning(
            "Dashboard request denied by IP ACL: client_ip=%s allowed=%s",
            client_ip or "<unknown>",
            ",".join(sorted(_PANEL_ALLOWED_IPS)) or "<none>",
        )
        denied_resp = (
            b"HTTP/1.1 403 Forbidden\r\n"
            b"Content-Type: text/plain; charset=utf-8\r\n"
            b"Connection: close\r\n"
            b"Content-Length: 29\r\n\r\n"
            b"Access denied: IP not allowed"
        )
        try:
            writer.write(denied_resp)
            await writer.drain()
        except Exception:
            pass
        finally:
            await close_writer(writer)
        return

    def _resp(status: str, body: bytes, ctype: str, extra_headers: str = "") -> bytes:
        return (
            f"HTTP/1.1 {status}\r\n".encode("ascii")
            + f"Content-Type: {ctype}\r\n".encode("ascii")
            + b"Cache-Control: no-store\r\n"
            b"X-Content-Type-Options: nosniff\r\n"
            + (extra_headers.encode("ascii") if extra_headers else b"")
            + f"Content-Length: {len(body)}\r\n".encode("ascii")
            + b"Connection: close\r\n\r\n"
            + body
        )

    try:
        request_line = await asyncio.wait_for(reader.readline(), timeout=5.0)
        if not request_line:
            return
        try:
            method, path, _ = request_line.decode("latin-1", "replace").split(" ", 2)
        except ValueError:
            return
        method = method.upper()

        content_length = 0
        cookie_hdr = ""
        while True:
            line = await asyncio.wait_for(reader.readline(), timeout=5.0)
            if line in (b"\r\n", b"\n", b""):
                break
            try:
                k, _, v = line.decode("latin-1", "replace").partition(":")
                kl = k.strip().lower()
                if kl == "content-length":
                    content_length = max(0, min(int(v.strip()), 64 * 1024))
                elif kl == "cookie":
                    cookie_hdr = v.strip()
            except (ValueError, UnicodeDecodeError):
                pass

        path = path.split("?", 1)[0]

        cookies = _parse_cookies(cookie_hdr)
        authed = (not _WEB_AUTH_ENABLED) or _session_valid(cookies.get(_COOKIE_NAME, ""))

        if path == "/login":
            # Serve and validate dashboard login separately from API/session routes.
            if not _WEB_AUTH_ENABLED:
                writer.write(_resp("302 Found", b"", "text/plain; charset=utf-8",
                                   "Location: /\r\n"))
                await writer.drain()
                return
            if method == "GET" or method == "HEAD":
                body = render_login_page()
                writer.write(_resp("200 OK", b"" if method == "HEAD" else body,
                                   "text/html; charset=utf-8"))
                await writer.drain()
                return
            if method == "POST":
                raw = b""
                if content_length:
                    try:
                        raw = await asyncio.wait_for(reader.readexactly(content_length), timeout=5.0)
                    except (asyncio.IncompleteReadError, asyncio.TimeoutError):
                        raw = b""
                form = _parse_form_urlencoded(raw)
                u = form.get("username", "")
                p = form.get("password", "")
                if u and p and secrets.compare_digest(u, _WEB_AUTH_USER) \
                        and secrets.compare_digest(p, _WEB_AUTH_PASS):
                    token = _issue_session()
                    cookie = (
                        f"Set-Cookie: {_COOKIE_NAME}={token}; Path=/; HttpOnly; "
                        f"SameSite=Strict; Max-Age={int(_SESSION_TTL)}\r\n"
                    )
                    writer.write(_resp("302 Found", b"", "text/plain; charset=utf-8",
                                       f"Location: /\r\n{cookie}"))
                else:
                    body = render_login_page("Invalid username or password.")
                    writer.write(_resp("401 Unauthorized", body, "text/html; charset=utf-8"))
                await writer.drain()
                return
            writer.write(_resp("405 Method Not Allowed", b"method not allowed",
                               "text/plain; charset=utf-8"))
            await writer.drain()
            return

        if path == "/logout":
            sid = cookies.get(_COOKIE_NAME, "")
            if sid:
                _WEB_SESSIONS.pop(sid, None)
            writer.write(_resp("302 Found", b"", "text/plain; charset=utf-8",
                               f"Location: /login\r\nSet-Cookie: {_COOKIE_NAME}=; Path=/; "
                               "Max-Age=0; HttpOnly; SameSite=Strict\r\n"))
            await writer.drain()
            return

        if not authed:
            if path.startswith("/api/"):
                body = json.dumps({"ok": False, "error": "authentication required"}).encode("utf-8")
                writer.write(_resp("401 Unauthorized", body, "application/json; charset=utf-8"))
            else:
                writer.write(_resp("302 Found", b"", "text/plain; charset=utf-8",
                                   "Location: /login\r\n"))
            await writer.drain()
            return

        if method in ("GET", "HEAD"):
            if path in ("/", "/index.html"):
                body = _WEB_INDEX_HTML.encode("utf-8")
                writer.write(_resp("200 OK",
                                   b"" if method == "HEAD" else body,
                                   "text/html; charset=utf-8"))
            elif path == "/api/stats":
                body = json.dumps(_stats_snapshot_dict(listen_addr, upstream_addr)).encode("utf-8")
                writer.write(_resp("200 OK", b"" if method == "HEAD" else body,
                                   "application/json; charset=utf-8"))
            elif path == "/api/controls":
                body = json.dumps(_controls_snapshot_dict()).encode("utf-8")
                writer.write(_resp("200 OK", b"" if method == "HEAD" else body,
                                   "application/json; charset=utf-8"))
            else:
                writer.write(_resp("404 Not Found", b"not found", "text/plain; charset=utf-8"))
        elif method == "POST" and path == "/api/control":
            raw = b""
            if content_length:
                try:
                    raw = await asyncio.wait_for(reader.readexactly(content_length), timeout=5.0)
                except (asyncio.IncompleteReadError, asyncio.TimeoutError):
                    raw = b""
            try:
                payload = json.loads(raw.decode("utf-8")) if raw else {}
                if not isinstance(payload, dict):
                    raise ValueError("body must be a JSON object")
            except (ValueError, UnicodeDecodeError) as exc:
                body = json.dumps({"ok": False, "error": f"bad json: {exc}"}).encode("utf-8")
                writer.write(_resp("400 Bad Request", body, "application/json; charset=utf-8"))
                await writer.drain()
                return
            action = str(payload.pop("action", ""))
            result = await apply_control_action(action, payload)
            body = json.dumps(result).encode("utf-8")
            status = "200 OK" if result.get("ok") else "400 Bad Request"
            writer.write(_resp(status, body, "application/json; charset=utf-8"))
        else:
            writer.write(_resp("405 Method Not Allowed", b"method not allowed",
                               "text/plain; charset=utf-8"))
        await writer.drain()
    except (asyncio.TimeoutError, ConnectionResetError, BrokenPipeError, OSError):
        pass
    except Exception:
        LOGGER.debug("web dashboard request failed", exc_info=True)
    finally:
        await close_writer(writer)


async def start_web_dashboard(
    host: str,
    port: int,
    listen_addr: str,
    upstream_addr: str,
) -> asyncio.base_events.Server:
    async def _handler(r: asyncio.StreamReader, w: asyncio.StreamWriter) -> None:
        await _web_handle_client(r, w, listen_addr, upstream_addr)

    server = await asyncio.start_server(_handler, host=host, port=port)
    sockets = server.sockets or []
    for s in sockets:
        LOGGER.info("Web dashboard available at http://%s:%d", *s.getsockname()[:2])
    return server
