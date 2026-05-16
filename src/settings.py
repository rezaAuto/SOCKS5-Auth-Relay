from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Final

LOGGER = logging.getLogger("socks5_auth_relay")


def _resolve_settings_path() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "settings.json"
    return Path(__file__).resolve().parent.parent / "settings.json"


_SETTINGS_PATH: Final[Path] = _resolve_settings_path()


@dataclass
class AppSettings:
    upstream_proxy: str = "127.0.0.1"
    upstream_port: int = 1080
    proxy_ip_listen: str = "0.0.0.0"
    proxy_port: int = 2080
    site_ip_listen: str = "127.0.0.1"
    site_port: int = 5656
    login_need: bool = True
    login_user: str = "admin"
    login_password: str = "change-me"
    default_socks_user: str = "socksuser"
    default_socks_password: str = "change-me"
    bandwidth_limit_kbps: int = 0
    max_conn_total: int = 0
    max_conn_per_client: int = 0
    geoip_enabled: bool = False
    auth_required: bool = True
    panel_ip_restricted: bool = True
    allowed_panel_ips: list[str] = field(default_factory=list)


def settings_path() -> Path:
    return _SETTINGS_PATH


def load_settings() -> AppSettings:
    defaults = AppSettings()
    data: dict = {}
    path = _SETTINGS_PATH

    if path.is_file():
        try:
            with path.open("r", encoding="utf-8") as f:
                parsed = json.load(f)
            if isinstance(parsed, dict):
                data = parsed
            else:
                LOGGER.warning("settings.json is not a JSON object; using defaults")
        except (OSError, ValueError) as exc:
            LOGGER.warning("could not read settings.json (%s) â€” using defaults", exc)

    merged = asdict(defaults)
    for k, v in data.items():
        if k in merged and isinstance(v, type(merged[k])):
            merged[k] = v
        elif k in merged and merged[k] is None:
            merged[k] = v

    # Coerce numeric ports defensively
    try:
        merged["upstream_port"] = int(merged["upstream_port"])
        merged["proxy_port"] = int(merged["proxy_port"])
        merged["site_port"] = int(merged["site_port"])
    except (TypeError, ValueError):
        pass
    merged["login_need"] = bool(merged.get("login_need", False))
    try:
        merged["bandwidth_limit_kbps"] = max(0, int(merged.get("bandwidth_limit_kbps", 0)))
    except (TypeError, ValueError):
        merged["bandwidth_limit_kbps"] = 0
    try:
        merged["max_conn_total"] = max(0, int(merged.get("max_conn_total", 0)))
    except (TypeError, ValueError):
        merged["max_conn_total"] = 0
    try:
        merged["max_conn_per_client"] = max(0, int(merged.get("max_conn_per_client", 0)))
    except (TypeError, ValueError):
        merged["max_conn_per_client"] = 0
    merged["geoip_enabled"] = bool(merged.get("geoip_enabled", False))
    merged["auth_required"] = bool(merged.get("auth_required", True))
    merged["panel_ip_restricted"] = bool(merged.get("panel_ip_restricted", False))
    # Ensure allowed_panel_ips is a list of strings
    allowed_ips = merged.get("allowed_panel_ips", [])
    if isinstance(allowed_ips, list):
        merged["allowed_panel_ips"] = [str(ip).strip() for ip in allowed_ips if ip]
    else:
        merged["allowed_panel_ips"] = []

    settings = AppSettings(**merged)

    try:
        save_settings(settings)
    except OSError as exc:
        LOGGER.warning("could not persist settings.json (%s)", exc)

    return settings


def save_settings(settings: AppSettings) -> None:
    path = _SETTINGS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    payload = json.dumps(asdict(settings), indent=2, ensure_ascii=False) + "\n"
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        f.write(payload)
    os.replace(tmp, path)
