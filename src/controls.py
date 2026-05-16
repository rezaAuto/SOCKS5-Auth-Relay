from __future__ import annotations

import asyncio
import ipaddress
import logging
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

from stats import STATS
from whitelist import (
    WHITELIST_CIDRS,
    WHITELIST_PRESETS,
    _parse_ip_literal,
)

LOGGER = logging.getLogger("socks5_auth_relay")


@dataclass
class Controls:
    proxy_enabled: bool = True
    whitelist_enabled: bool = False
    whitelist_strict: bool = False
    ir_redirect: bool = False
    presets: set[str] = field(default_factory=set)
    custom_domains: set[str] = field(default_factory=set)
    traffic_limit_bytes: int = 0
    bandwidth_limit_bps: int = 0
    max_conn_total: int = 0
    max_conn_per_client: int = 0
    conn_refused: int = 0
    geoip_enabled: bool = False
    auth_required: bool = True
    bypassed: int = 0
    bypassed_active: int = 0

    listen_host: str = ""
    listen_port: int = 0

    def limit_exceeded(self) -> bool:
        if self.traffic_limit_bytes <= 0:
            return False
        return (STATS.bytes_up + STATS.bytes_down) >= self.traffic_limit_bytes

    def active_domains(self) -> set[str]:
        result: set[str] = set(self.custom_domains)
        for name in self.presets:
            result |= WHITELIST_PRESETS.get(name, set())
        return result

    def _ip_matches_active_cidrs(self, ip: ipaddress._BaseAddress) -> bool:
        for name in self.presets:
            nets = WHITELIST_CIDRS.get(name)
            if not nets:
                continue
            v4_nets, v6_nets = nets
            family_nets = v6_nets if ip.version == 6 else v4_nets
            for net in family_nets:
                if ip in net:
                    return True
        return False

    def should_bypass(self, host: str) -> bool:
        h = host.lower().strip(".")
        if self.ir_redirect and (h == "ir" or h.endswith(".ir")):
            return True
        if not self.whitelist_enabled:
            return False
        if self.whitelist_strict:
            return False
        ip = _parse_ip_literal(h)
        if ip is not None:
            # Raw IP literal â€” match against preset CIDRs.
            return self._ip_matches_active_cidrs(ip)
        for suffix in self.active_domains():
            if h == suffix or h.endswith("." + suffix):
                return True
        return False

    def is_blocked(self, host: str) -> bool:
        if not (self.whitelist_enabled and self.whitelist_strict):
            return False
        h = host.lower().strip(".")
        if self.ir_redirect and (h == "ir" or h.endswith(".ir")):
            return False
        ip = _parse_ip_literal(h)
        if ip is not None:
            return not self._ip_matches_active_cidrs(ip)
        for suffix in self.active_domains():
            if h == suffix or h.endswith("." + suffix):
                return False
        return True


CONTROLS = Controls()


class BandwidthBucket:

    def __init__(self) -> None:
        self._tokens: float = 0.0
        self._last: float = time.monotonic()
        self._lock = asyncio.Lock()

    async def consume(self, nbytes: int) -> None:
        if nbytes <= 0:
            return
        rate = float(CONTROLS.bandwidth_limit_bps)
        if rate <= 0:
            return
        capacity = rate
        async with self._lock:
            while True:
                now = time.monotonic()
                self._tokens = min(capacity, self._tokens + (now - self._last) * rate)
                self._last = now
                if self._tokens >= nbytes:
                    self._tokens -= nbytes
                    return
                needed = (nbytes - self._tokens) / rate
                await asyncio.sleep(min(needed, 0.25))


BANDWIDTH_BUCKET = BandwidthBucket()


@dataclass
class ControlPlane:
    rebind_socks: Callable[..., object]
    trigger_kill: Callable[..., object]
    drop_tunnels: Callable[..., object]
    update_credentials: Callable[..., object]
    get_username: Callable[..., object]
    get_password: Callable[..., object]
    check_upstream: Callable[..., object]


_CONTROL_PLANE: "Optional[ControlPlane]" = None


def get_control_plane() -> "Optional[ControlPlane]":
    return _CONTROL_PLANE


def set_control_plane(plane: "Optional[ControlPlane]") -> None:
    global _CONTROL_PLANE
    _CONTROL_PLANE = plane


async def stats_sampler_loop(interval: float = 1.0) -> None:
    limit_tripped = False
    try:
        while True:
            STATS.snapshot_speed()

            if CONTROLS.limit_exceeded():
                plane = _CONTROL_PLANE
                if not limit_tripped and plane is not None:
                    try:
                        dropped = plane.drop_tunnels()
                        LOGGER.warning(
                            "traffic limit reached (%d bytes) — dropped %d active tunnel writer(s)",
                            CONTROLS.traffic_limit_bytes, dropped,
                        )
                    except Exception:
                        LOGGER.debug("drop_tunnels on limit failed", exc_info=True)
                    limit_tripped = True
            else:
                limit_tripped = False

            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        raise


async def apply_control_action(action: str, params: dict) -> dict:
    plane = _CONTROL_PLANE

    if action == "set_proxy":
        CONTROLS.proxy_enabled = bool(params.get("enabled", True))
        LOGGER.info("proxy %s via web", "enabled" if CONTROLS.proxy_enabled else "paused")
        if not CONTROLS.proxy_enabled and plane is not None:
            try:
                dropped = plane.drop_tunnels()
                if dropped:
                    LOGGER.info("paused: dropped %d active tunnel writer(s)", dropped)
            except Exception:
                LOGGER.debug("drop_tunnels on pause failed", exc_info=True)
        return {"ok": True}

    if action == "set_whitelist":
        CONTROLS.whitelist_enabled = bool(params.get("enabled", False))
        LOGGER.info("whitelist %s via web", "on" if CONTROLS.whitelist_enabled else "off")
        if CONTROLS.whitelist_strict and plane is not None:
            try:
                dropped = plane.drop_tunnels()
                if dropped:
                    LOGGER.info("whitelist toggle: dropped %d active tunnel writer(s)", dropped)
            except Exception:
                LOGGER.debug("drop_tunnels on whitelist toggle failed", exc_info=True)
        return {"ok": True}

    if action == "set_whitelist_strict":
        CONTROLS.whitelist_strict = bool(params.get("enabled", False))
        if CONTROLS.whitelist_strict and not CONTROLS.whitelist_enabled:
            CONTROLS.whitelist_enabled = True
            LOGGER.info("whitelist auto-enabled because strict mode was turned on")
        LOGGER.info("whitelist strict mode %s via web", "on" if CONTROLS.whitelist_strict else "off")
        if (CONTROLS.whitelist_strict and CONTROLS.whitelist_enabled
                and plane is not None):
            try:
                dropped = plane.drop_tunnels()
                if dropped:
                    LOGGER.info("strict mode: dropped %d active tunnel writer(s)", dropped)
            except Exception:
                LOGGER.debug("drop_tunnels on strict toggle failed", exc_info=True)
        return {"ok": True}

    if action == "set_ir_redirect":
        CONTROLS.ir_redirect = bool(params.get("enabled", False))
        LOGGER.info(".ir redirect %s via web", "on" if CONTROLS.ir_redirect else "off")
        return {"ok": True}

    if action == "set_preset":
        name = str(params.get("name", ""))
        if name not in WHITELIST_PRESETS:
            return {"ok": False, "error": f"unknown preset: {name}"}
        enabled = bool(params.get("enabled", False))
        was_in = name in CONTROLS.presets
        if enabled:
            CONTROLS.presets.add(name)
        else:
            CONTROLS.presets.discard(name)
        if (was_in and not enabled
                and CONTROLS.whitelist_strict and CONTROLS.whitelist_enabled
                and plane is not None):
            try:
                dropped = plane.drop_tunnels()
                if dropped:
                    LOGGER.info(
                        "preset '%s' disabled under strict: dropped %d tunnel writer(s)",
                        name, dropped,
                    )
            except Exception:
                LOGGER.debug("drop_tunnels on preset disable failed", exc_info=True)
        return {"ok": True}

    if action == "set_limit":
        if "mb" in params:
            CONTROLS.traffic_limit_bytes = max(0, int(float(params["mb"]) * 1024 * 1024))
        else:
            CONTROLS.traffic_limit_bytes = max(0, int(params.get("bytes", 0)))
        LOGGER.info("traffic limit set to %d bytes", CONTROLS.traffic_limit_bytes)
        return {"ok": True}

    if action == "set_bandwidth":
        try:
            if "kbps" in params:
                CONTROLS.bandwidth_limit_bps = max(0, int(float(params["kbps"]) * 1024))
            else:
                CONTROLS.bandwidth_limit_bps = max(0, int(params.get("bps", 0)))
        except (TypeError, ValueError):
            return {"ok": False, "error": "invalid bandwidth value"}
        LOGGER.info("bandwidth limit set to %d B/s", CONTROLS.bandwidth_limit_bps)
        return {"ok": True}

    if action == "set_conn_cap":
        try:
            if "total" in params:
                CONTROLS.max_conn_total = max(0, int(params["total"]))
            if "per_client" in params:
                CONTROLS.max_conn_per_client = max(0, int(params["per_client"]))
        except (TypeError, ValueError):
            return {"ok": False, "error": "invalid connection cap value"}
        LOGGER.info(
            "connection caps updated: total=%d per_client=%d",
            CONTROLS.max_conn_total, CONTROLS.max_conn_per_client,
        )
        return {"ok": True}

    if action == "set_geoip":
        flag = bool(params.get("enabled", False))
        CONTROLS.geoip_enabled = flag
        try:
            from geoip import set_enabled as _geo_set_enabled
            _geo_set_enabled(flag)
        except Exception:
            LOGGER.debug("geoip module not available", exc_info=True)
        LOGGER.info("geoip lookups %s via web", "on" if flag else "off")
        return {"ok": True}

    if action == "set_auth_required":
        CONTROLS.auth_required = bool(params.get("enabled", True))
        LOGGER.warning(
            "SOCKS5 client auth %s via web — %s",
            "required" if CONTROLS.auth_required else "DISABLED",
            "clients now must authenticate" if CONTROLS.auth_required
            else "clients can connect WITHOUT credentials",
        )
        # Kick active tunnels so the new policy applies immediately.
        if plane is not None:
            try:
                plane.drop_tunnels()
            except Exception:
                LOGGER.debug("drop_tunnels on auth toggle failed", exc_info=True)
        return {"ok": True}

    if action == "reset_traffic":
        STATS.bytes_up = 0
        STATS.bytes_down = 0
        STATS._last_up = 0
        STATS._last_down = 0
        STATS.peak_up_bps = 1.0
        STATS.peak_down_bps = 1.0
        STATS.peak_active = STATS.active
        STATS.spark_up.clear()
        STATS.spark_down.clear()
        STATS.hosts.clear()
        LOGGER.info("traffic counters reset via web")
        return {"ok": True}

    if action == "change_port":
        try:
            port = int(params.get("port", 0))
        except (TypeError, ValueError):
            return {"ok": False, "error": "invalid port"}
        if not (1 <= port <= 65535):
            return {"ok": False, "error": "port out of range"}
        if plane is None:
            return {"ok": False, "error": "control plane not ready"}
        try:
            await plane.rebind_socks(port)
        except OSError as exc:
            return {"ok": False, "error": f"bind failed: {exc}"}
        return {"ok": True, "port": port}

    if action == "kill":
        LOGGER.warning("KILL SWITCH triggered via web — process will exit")
        if plane is not None:
            loop = asyncio.get_running_loop()
            loop.call_later(0.15, plane.trigger_kill)
        return {"ok": True, "killed": True}

    if action == "set_credentials":
        user = str(params.get("username", "")).strip()
        pw = str(params.get("password", ""))
        if not user or not pw:
            return {"ok": False, "error": "username and password are required"}
        if len(user) > 255 or len(pw) > 255:
            return {"ok": False, "error": "username/password max length is 255"}
        if plane is None:
            return {"ok": False, "error": "control plane not ready"}
        try:
            dropped = plane.update_credentials(user, pw)
        except Exception as exc:
            LOGGER.exception("set_credentials failed")
            return {"ok": False, "error": f"update failed: {exc}"}
        LOGGER.warning(
            "credentials rotated via web (user=%s) — dropped %d active tunnel writer(s)",
            user, dropped,
        )
        return {"ok": True, "username": user, "dropped": dropped}

    if action == "check_upstream":
        if plane is None:
            return {"ok": False, "error": "control plane not ready"}
        try:
            result = plane.check_upstream()
            if asyncio.iscoroutine(result):
                result = await result
        except Exception as exc:
            LOGGER.exception("upstream health check failed")
            return {"ok": False, "error": f"upstream check failed: {exc}"}
        if isinstance(result, dict):
            return result
        return {"ok": False, "error": "invalid upstream check response"}

    return {"ok": False, "error": f"unknown action: {action}"}
