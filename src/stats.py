from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class ClientStats:
    ip: str
    bytes_up: int = 0
    bytes_down: int = 0
    active_tunnels: int = 0
    total_tunnels: int = 0
    last_activity_ts: float = field(default_factory=time.monotonic)


@dataclass
class HostStats:
    bytes_up: int = 0
    bytes_down: int = 0
    active: int = 0
    total: int = 0
    last_ts: float = field(default_factory=time.monotonic)


@dataclass
class TrafficStats:
    bytes_up: int = 0
    bytes_down: int = 0
    active: int = 0
    peak_active: int = 0
    total: int = 0
    errors: int = 0
    auth_fail: int = 0
    refused: int = 0
    reset: int = 0
    tcp_connections: int = 0

    _last_up: int = 0
    _last_down: int = 0
    _last_ts: float = field(default_factory=time.monotonic)
    _last_total_conns: int = 0
    _last_conn_ts: float = field(default_factory=time.monotonic)

    conns_per_sec: float = 0.0

    peak_up_bps: float = 1.0
    peak_down_bps: float = 1.0
    ema_up_bps: float = 0.0
    ema_down_bps: float = 0.0
    _ema_alpha: float = 0.3

    started_at: float = field(default_factory=time.monotonic)
    spark_up: deque[float] = field(default_factory=lambda: deque(maxlen=120))
    spark_down: deque[float] = field(default_factory=lambda: deque(maxlen=120))

    hosts: defaultdict[str, HostStats] = field(
        default_factory=lambda: defaultdict(HostStats)
    )
    
    clients: dict[str, ClientStats] = field(default_factory=dict)
    
    _cached_now: float = field(default_factory=time.monotonic)

    def snapshot_speed(self) -> tuple[float, float]:
        now = time.monotonic()
        dt = max(now - self._last_ts, 1e-6)

        up_bps = max(0, self.bytes_up - self._last_up) / dt
        down_bps = max(0, self.bytes_down - self._last_down) / dt

        self._last_up = self.bytes_up
        self._last_down = self.bytes_down
        self._last_ts = now

        if up_bps > self.peak_up_bps:
            self.peak_up_bps = up_bps
        if down_bps > self.peak_down_bps:
            self.peak_down_bps = down_bps

        a = self._ema_alpha
        self.ema_up_bps = a * up_bps + (1 - a) * self.ema_up_bps
        self.ema_down_bps = a * down_bps + (1 - a) * self.ema_down_bps

        self.spark_up.append(up_bps)
        self.spark_down.append(down_bps)

        cdt = max(now - self._last_conn_ts, 1e-6)
        self.conns_per_sec = max(0, self.total - self._last_total_conns) / cdt
        self._last_total_conns = self.total
        self._last_conn_ts = now

        if self.active > self.peak_active:
            self.peak_active = self.active

        return up_bps, down_bps


STATS = TrafficStats()
