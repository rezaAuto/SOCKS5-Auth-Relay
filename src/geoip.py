from __future__ import annotations

import asyncio
import ipaddress
import json
import logging
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Final

LOGGER = logging.getLogger("socks5_auth_relay")

GEO_CACHE: dict[str, dict[str, str]] = {}

_QUEUE: "asyncio.Queue[str] | None" = None
_WORKER_TASK: "asyncio.Task[None] | None" = None
_ENABLED: bool = False

_MAX_CACHE: Final[int] = 4096
_TIMEOUT: Final[float] = 3.0
_API_URL: Final[str] = "http://ip-api.com/json/{q}?fields=status,country,countryCode"


def set_enabled(flag: bool) -> None:
    global _ENABLED
    _ENABLED = bool(flag)


def is_enabled() -> bool:
    return _ENABLED


def enqueue_lookup(host: str) -> None:
    if not _ENABLED:
        return
    h = (host or "").strip().strip(".").lower()
    if not h or h in GEO_CACHE:
        return
    try:
        ip = ipaddress.ip_address(h)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
            GEO_CACHE[h] = {"cc": "", "country": "local"}
            return
    except ValueError:
        pass
    q = _QUEUE
    if q is None:
        return
    try:
        q.put_nowait(h)
    except asyncio.QueueFull:
        pass


def _fetch_blocking(host: str) -> dict[str, str]:
    url = _API_URL.format(q=urllib.parse.quote(host, safe=""))
    req = urllib.request.Request(url, headers={"User-Agent": "socks5-relay/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            raw = resp.read(4096)
        data = json.loads(raw.decode("utf-8", "replace"))
    except (urllib.error.URLError, socket.timeout, ValueError, OSError) as exc:
        LOGGER.debug("geoip lookup failed for %s: %s", host, exc)
        return {"cc": "", "country": ""}
    if data.get("status") != "success":
        return {"cc": "", "country": ""}
    return {
        "cc": str(data.get("countryCode") or "").upper()[:2],
        "country": str(data.get("country") or ""),
    }


async def _worker_loop() -> None:
    assert _QUEUE is not None
    in_flight: set[str] = set()
    while True:
        host = await _QUEUE.get()
        try:
            if host in GEO_CACHE or host in in_flight:
                continue
            if not _ENABLED:
                continue
            in_flight.add(host)
            try:
                result = await asyncio.to_thread(_fetch_blocking, host)
            except Exception as exc:
                LOGGER.debug("geoip worker error for %s: %s", host, exc)
                result = {"cc": "", "country": ""}
            if len(GEO_CACHE) >= _MAX_CACHE:
                for k in list(GEO_CACHE.keys())[: _MAX_CACHE // 10]:
                    GEO_CACHE.pop(k, None)
            GEO_CACHE[host] = result
            in_flight.discard(host)
        except asyncio.CancelledError:
            raise
        finally:
            _QUEUE.task_done()


def start_worker() -> None:
    global _QUEUE, _WORKER_TASK
    if _WORKER_TASK is not None and not _WORKER_TASK.done():
        return
    _QUEUE = asyncio.Queue(maxsize=256)
    _WORKER_TASK = asyncio.create_task(_worker_loop(), name="geoip-worker")
