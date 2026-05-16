from __future__ import annotations

import argparse
import asyncio
import base64
import ipaddress
import logging
import os
import socket
import sys
import time
from typing import Final

try:
    import resource
except ImportError:  # Windows has no `resource` module.
    resource = None

from utils import (
    close_writer,
    detect_current_user_ip,
    prompt_required_value,
    set_tcp_nodelay as _set_tcp_nodelay,
)

LOGGER = logging.getLogger("socks5_auth_relay")
SOCKS_HANDSHAKE_TIMEOUT: Final[float] = 10.0


from stats import HostStats, STATS, ClientStats
from settings import load_settings
from controls import (
    CONTROLS,
    ControlPlane,
    set_control_plane,
    stats_sampler_loop,
)
from web import start_web_dashboard, set_panel_ip_acl, set_web_auth
from socks_protocol import (
    BUFFER_SIZE,
    SOCKS_VERSION,
    LocalAuth,
    ReplyCode,
    SilentClientDisconnect,
    SocksProtocolError,
    SocksRequestError,
    UpstreamProxy,
    authenticate_client,
    build_failure_reply,
    build_socks_request_from_hostport,
    map_os_error_to_reply,
    open_direct_tunnel,
    open_upstream_tunnel,
    read_client_request,
    relay_stream,
)


def _raise_fd_limit() -> None:
    if resource is None:
        LOGGER.debug("RLIMIT_NOFILE tweak skipped: resource module not available on this platform")
        return
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        if soft < hard:
            resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
            LOGGER.info("Raised RLIMIT_NOFILE: %d -> %d", soft, hard)
        else:
            LOGGER.debug("RLIMIT_NOFILE already at hard cap: %d", hard)
    except Exception as exc:
        LOGGER.warning("Could not raise RLIMIT_NOFILE: %s", exc)


def _is_loopback_bind_host(host: str) -> bool:
    h = (host or "").strip().strip("[]").lower()
    if h == "localhost":
        return True
    if h in {"", "0.0.0.0", "::"}:
        return False
    try:
        return ipaddress.ip_address(h).is_loopback
    except ValueError:
        return False


def _looks_like_default_secret(value: str) -> bool:
    return (value or "").strip().lower() in {
        "",
        "admin",
        "change-me",
        "changeme",
        "password",
        "123456",
        "12345678",
    }


class AuthenticatedSocksRelay:
    def __init__(self, upstream: UpstreamProxy, credentials: LocalAuth) -> None:
        self.upstream = upstream
        self.credentials = credentials
        self._tasks: set[asyncio.Task[None]] = set()
        self._live_writers: set[asyncio.StreamWriter] = set()
        self._admitted_active: int = 0
        self._per_client_active: dict[str, int] = {}

    def drop_all_tunnels(self) -> int:
        n = 0
        for w in list(self._live_writers):
            try:
                if not w.is_closing():
                    w.close()
                    n += 1
            except Exception:
                pass
        self._live_writers.clear()
        return n

    def update_credentials(self, username: str, password: str) -> int:
        self.credentials = LocalAuth(username=username, password=password)
        return self.drop_all_tunnels()

    async def check_upstream_public_ip(self) -> dict:
        probes: tuple[tuple[str, str], ...] = (
            ("api.ipify.org", "/?format=text"),
            ("ifconfig.me", "/ip"),
        )
        started = time.monotonic()
        last_error = ""

        for host, path in probes:
            upstream_writer: asyncio.StreamWriter | None = None
            try:
                req = build_socks_request_from_hostport(host, 80)
                upstream_reader, upstream_writer, _ = await asyncio.wait_for(
                    open_upstream_tunnel(self.upstream, req),
                    timeout=6.0,
                )
                _set_tcp_nodelay(upstream_writer.get_extra_info("socket"))

                http_req = (
                    f"GET {path} HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    "User-Agent: socks5-relay/1.0\r\n"
                    "Accept: text/plain\r\n"
                    "Connection: close\r\n\r\n"
                ).encode("ascii", "replace")
                upstream_writer.write(http_req)
                await upstream_writer.drain()

                raw = await asyncio.wait_for(upstream_reader.read(8192), timeout=6.0)
                if not raw:
                    raise SocksProtocolError("empty response from IP API")

                _head, _sep, body = raw.partition(b"\r\n\r\n")
                text = body.decode("utf-8", "replace").strip().splitlines()[0].strip()
                try:
                    ip = str(ipaddress.ip_address(text))
                except ValueError as exc:
                    raise SocksProtocolError(f"invalid IP payload: {text!r}") from exc

                return {
                    "ok": True,
                    "upstream_ok": True,
                    "public_ip": ip,
                    "api": host,
                    "latency_ms": round((time.monotonic() - started) * 1000, 1),
                }
            except Exception as exc:
                last_error = str(exc)
            finally:
                await close_writer(upstream_writer)

        return {
            "ok": False,
            "upstream_ok": False,
            "error": f"all upstream checks failed: {last_error or 'unknown error'}",
            "latency_ms": round((time.monotonic() - started) * 1000, 1),
        }

    async def dispatch(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter) -> None:
        task = asyncio.current_task()
        if task is not None:
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
        await self.handle_client(client_reader, client_writer)

    async def handle_client(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter) -> None:
        peername = client_writer.get_extra_info("peername")
        upstream_writer: asyncio.StreamWriter | None = None
        tunnel_established = False
        bypass = False
        host_key: str | None = None
        host_stats: HostStats | None = None
        client_stats: ClientStats | None = None
        client_ip: str = ""
        global_counted = False
        client_counted = False

        _set_tcp_nodelay(client_writer.get_extra_info("socket"))

        try:
            if isinstance(peername, (tuple, list)) and peername:
                client_ip = str(peername[0])
            total_cap = CONTROLS.max_conn_total
            per_cap = CONTROLS.max_conn_per_client

            admitted_now = self._admitted_active
            if total_cap > 0 and admitted_now >= total_cap:
                CONTROLS.conn_refused += 1
                LOGGER.info(
                    "connection refused (global cap %d reached: admitted=%d established=%d) from %s",
                    total_cap,
                    admitted_now,
                    STATS.active,
                    peername,
                )
                return
            if per_cap > 0 and client_ip:
                per_now = self._per_client_active.get(client_ip, 0)
                if per_now >= per_cap:
                    CONTROLS.conn_refused += 1
                    LOGGER.info(
                        "connection refused (per-client cap %d reached: ip=%s active=%d) from %s",
                        per_cap,
                        client_ip,
                        per_now,
                        peername,
                    )
                    return

            self._admitted_active = admitted_now + 1
            global_counted = True
            if client_ip:
                self._per_client_active[client_ip] = self._per_client_active.get(client_ip, 0) + 1
                client_counted = True

            await asyncio.wait_for(
                authenticate_client(client_reader, client_writer, self.credentials),
                timeout=SOCKS_HANDSHAKE_TIMEOUT,
            )
            request = await asyncio.wait_for(
                read_client_request(client_reader),
                timeout=SOCKS_HANDSHAKE_TIMEOUT,
            )
            LOGGER.debug("client %s requested %s:%d", peername, request.destination, request.port)

            if not CONTROLS.proxy_enabled:
                raise SocksRequestError(
                    ReplyCode.CONNECTION_NOT_ALLOWED,
                    "proxy is paused by operator",
                )
            if CONTROLS.limit_exceeded():
                raise SocksRequestError(
                    ReplyCode.CONNECTION_NOT_ALLOWED,
                    "traffic limit reached",
                )
            if CONTROLS.is_blocked(request.destination):
                raise SocksRequestError(
                    ReplyCode.CONNECTION_NOT_ALLOWED,
                    f"destination not on whitelist (strict): {request.destination}",
                )

            bypass = CONTROLS.should_bypass(request.destination)
            if bypass:
                upstream_reader, upstream_writer, upstream_reply = await open_direct_tunnel(request)
            else:
                upstream_reader, upstream_writer, upstream_reply = await open_upstream_tunnel(self.upstream, request)
            _set_tcp_nodelay(upstream_writer.get_extra_info("socket"))
            client_writer.write(upstream_reply)
            await client_writer.drain()

            tunnel_established = True
            STATS.active += 1
            STATS.total += 1
            STATS.tcp_connections += 1
            if STATS.active > STATS.peak_active:
                STATS.peak_active = STATS.active
            if bypass:
                CONTROLS.bypassed += 1
                CONTROLS.bypassed_active += 1
            host_key = f"{request.destination}:{request.port}"
            host_stats = STATS.hosts[host_key]
            host_stats.active += 1
            host_stats.total += 1
            if client_ip:
                client_stats = STATS.clients.get(client_ip)
                if client_stats is None:
                    client_stats = ClientStats(ip=client_ip)
                    STATS.clients[client_ip] = client_stats
                client_stats.active_tunnels += 1
                client_stats.total_tunnels += 1
                client_stats.last_activity_ts = time.monotonic()
            try:
                import geoip as _geoip
                _geoip.enqueue_lookup(request.destination)
                if client_ip:
                    _geoip.enqueue_lookup(client_ip)
            except Exception:
                pass
            self._live_writers.add(client_writer)
            self._live_writers.add(upstream_writer)
            c2u = asyncio.create_task(
                relay_stream(client_reader, upstream_writer, "up", host_stats, client_stats)
            )
            u2c = asyncio.create_task(
                relay_stream(upstream_reader, client_writer, "down", host_stats, client_stats)
            )
            done, pending = await asyncio.wait({c2u, u2c}, return_when=asyncio.FIRST_COMPLETED)

            for task in pending:
                if task is c2u:
                    await close_writer(upstream_writer)
                elif task is u2c:
                    await close_writer(client_writer)

            if pending:
                try:
                    await asyncio.wait_for(asyncio.shield(asyncio.gather(*pending, return_exceptions=True)), timeout=1.0)
                except asyncio.TimeoutError:
                    for task in pending:
                        task.cancel()
                    for task in pending:
                        try:
                            await task
                        except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError, OSError):
                            pass

            for task in done:
                try:
                    task.result()
                except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError, OSError):
                    pass
                except Exception:
                    LOGGER.debug("relay task error for %s", peername, exc_info=True)

        except SilentClientDisconnect:
            LOGGER.debug("client %s disconnected before sending any SOCKS data", peername)
        except asyncio.TimeoutError:
            STATS.errors += 1
            LOGGER.debug("SOCKS handshake timed out for %s", peername)
        except SocksRequestError as exc:
            STATS.errors += 1
            if exc.reply_code in (
                ReplyCode.GENERAL_FAILURE,
                ReplyCode.CONNECTION_NOT_ALLOWED,
                ReplyCode.CONNECTION_REFUSED,
                ReplyCode.HOST_UNREACHABLE,
                ReplyCode.NETWORK_UNREACHABLE,
                ReplyCode.TTL_EXPIRED,
                ReplyCode.COMMAND_NOT_SUPPORTED,
                ReplyCode.ADDRESS_TYPE_NOT_SUPPORTED,
            ):
                STATS.refused += 1
                LOGGER.debug("SOCKS request error for %s: %s", peername, exc)
            else:
                LOGGER.warning("SOCKS request error for %s: %s", peername, exc)
            if not client_writer.is_closing():
                try:
                    client_writer.write(build_failure_reply(exc.reply_code))
                    await client_writer.drain()
                except OSError:
                    pass
        except SocksProtocolError as exc:
            msg = str(exc)
            benign_protocol_errors = (
                "invalid username/password",
                "does not support username/password authentication",
                "unsupported auth sub-negotiation version",
                "unsupported SOCKS version",
                "unexpected SOCKS request version",
            )
            if any(s in msg for s in benign_protocol_errors):
                STATS.errors += 1
                STATS.auth_fail += 1
                LOGGER.debug("SOCKS handshake rejected for %s: %s", peername, exc)
            else:
                STATS.errors += 1
                LOGGER.warning("SOCKS protocol error for %s: %s", peername, exc)
        except OSError as exc:
            benign_winerr = {64, 121, 1236, 10053, 10054}
            benign_errno = {104, 32}
            winerr = getattr(exc, "winerror", None)
            is_benign_reset = winerr in benign_winerr or exc.errno in benign_errno

            if not tunnel_established and is_benign_reset:
                LOGGER.debug("client %s disconnected during handshake: %s", peername, exc)
            elif is_benign_reset:
                STATS.errors += 1
                STATS.reset += 1
                LOGGER.debug("peer reset for %s: %s", peername, exc)
            else:
                STATS.errors += 1
                reply_code = map_os_error_to_reply(exc)
                LOGGER.warning("network error for %s: %s", peername, exc)
                if not client_writer.is_closing():
                    try:
                        client_writer.write(build_failure_reply(reply_code))
                        await client_writer.drain()
                    except OSError:
                        pass
        except Exception:
            STATS.errors += 1
            LOGGER.exception("unexpected error while handling %s", peername)
            if not client_writer.is_closing():
                try:
                    client_writer.write(build_failure_reply(ReplyCode.GENERAL_FAILURE))
                    await client_writer.drain()
                except OSError:
                    pass
        finally:
            if tunnel_established:
                STATS.active = max(0, STATS.active - 1)
                if bypass:
                    CONTROLS.bypassed_active = max(0, CONTROLS.bypassed_active - 1)
                if host_stats is not None:
                    host_stats.active = max(0, host_stats.active - 1)

            if global_counted:
                self._admitted_active = max(0, self._admitted_active - 1)

            if client_counted and client_ip:
                if client_stats is not None:
                    client_stats.active_tunnels = max(0, client_stats.active_tunnels - 1)
                    client_stats.last_activity_ts = time.monotonic()
                left = self._per_client_active.get(client_ip, 0) - 1
                if left <= 0:
                    self._per_client_active.pop(client_ip, None)
                else:
                    self._per_client_active[client_ip] = left
            self._live_writers.discard(client_writer)
            if upstream_writer is not None:
                self._live_writers.discard(upstream_writer)
            await close_writer(upstream_writer)
            await close_writer(client_writer)

    _HTTP_METHODS = frozenset({
        b"GET", b"POST", b"PUT", b"DELETE", b"HEAD", b"OPTIONS",
        b"PATCH", b"TRACE", b"CONNECT",
    })

    @staticmethod
    def _http_resp(status: str, body: bytes = b"", extra_headers: str = "") -> bytes:
        hdr = (
            f"HTTP/1.1 {status}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            f"{extra_headers}\r\n"
        ).encode("ascii", "replace")
        return hdr + body

    def _http_check_auth(self, value: str) -> bool:
        if not value.lower().startswith("basic "):
            return False
        try:
            decoded = base64.b64decode(value[6:].strip(), validate=False).decode("utf-8", "replace")
        except Exception:
            return False
        u, sep, p = decoded.partition(":")
        return bool(sep) and u == self.credentials.username and p == self.credentials.password

    @staticmethod
    def _parse_authority(authority: str) -> tuple[str, int]:
        authority = authority.strip()
        if authority.startswith("["):
            close = authority.find("]")
            if close == -1:
                raise ValueError("malformed IPv6 authority")
            host = authority[1:close]
            rest = authority[close + 1:]
            port = int(rest[1:]) if rest.startswith(":") else 80
            return host, port
        if ":" in authority:
            host, _, port_s = authority.rpartition(":")
            return host, int(port_s)
        return authority, 80

    async def handle_http_client(
        self,
        client_reader: asyncio.StreamReader,
        client_writer: asyncio.StreamWriter,
    ) -> None:
        peername = client_writer.get_extra_info("peername")
        _set_tcp_nodelay(client_writer.get_extra_info("socket"))

        try:
            while True:
                keep_alive = await self._serve_one_http_request(
                    client_reader, client_writer, peername
                )
                if not keep_alive:
                    break
        except SilentClientDisconnect:
            LOGGER.debug("HTTP client %s disconnected before sending data", peername)
        except SocksProtocolError as exc:
            STATS.errors += 1
            LOGGER.debug("HTTP framing error for %s: %s", peername, exc)
        except (ConnectionResetError, BrokenPipeError, OSError) as exc:
            LOGGER.debug("HTTP proxy network error for %s: %s", peername, exc)
        except Exception:
            STATS.errors += 1
            LOGGER.exception("unexpected error in HTTP proxy for %s", peername)
        finally:
            self._live_writers.discard(client_writer)
            await close_writer(client_writer)

    async def _serve_one_http_request(
        self,
        client_reader: asyncio.StreamReader,
        client_writer: asyncio.StreamWriter,
        peername,
    ) -> bool:
        upstream_writer: asyncio.StreamWriter | None = None
        tunnel_established = False
        bypass = False
        host_key: str | None = None
        host_stats: "HostStats | None" = None
        client_writer_tracked = False

        try:
            buf = bytearray()
            first_read = True
            while b"\r\n\r\n" not in buf:
                try:
                    if first_read:
                        chunk = await asyncio.wait_for(
                            client_reader.read(4096), timeout=60.0
                        )
                        first_read = False
                    else:
                        chunk = await asyncio.wait_for(
                            client_reader.read(4096), timeout=15.0
                        )
                except asyncio.TimeoutError:
                    if not buf:
                        raise SilentClientDisconnect()
                    raise SocksProtocolError("HTTP request header timeout")
                if not chunk:
                    if not buf:
                        raise SilentClientDisconnect()
                    raise SocksProtocolError("HTTP request incomplete")
                buf.extend(chunk)
                if len(buf) > 64 * 1024:
                    client_writer.write(self._http_resp("413 Request Header Fields Too Large"))
                    await client_writer.drain()
                    return False

            head, _, leftover = bytes(buf).partition(b"\r\n\r\n")
            lines = head.split(b"\r\n")
            if not lines:
                raise SocksProtocolError("empty HTTP request")

            try:
                method_b, target_b, version_b = lines[0].split(b" ", 2)
            except ValueError:
                client_writer.write(self._http_resp("400 Bad Request"))
                await client_writer.drain()
                return False

            method = method_b.upper()
            if method not in self._HTTP_METHODS:
                client_writer.write(self._http_resp("400 Bad Request"))
                await client_writer.drain()
                return False

            headers: dict[str, str] = {}
            for ln in lines[1:]:
                if b":" in ln:
                    k, _, v = ln.partition(b":")
                    headers[k.strip().lower().decode("ascii", "replace")] = v.strip().decode("iso-8859-1", "replace")

            proxy_conn = headers.get("proxy-connection", "").lower()
            conn_hdr = headers.get("connection", "").lower()
            http_version = version_b.strip().upper()
            is_http11 = http_version == b"HTTP/1.1"
            explicit_close = ("close" in proxy_conn) or ("close" in conn_hdr)
            explicit_keep = ("keep-alive" in proxy_conn) or ("keep-alive" in conn_hdr)
            client_keep_alive = (is_http11 and not explicit_close) or explicit_keep

            proxy_auth = headers.get("proxy-authorization", "")
            if not self._http_check_auth(proxy_auth):
                STATS.errors += 1
                STATS.auth_fail += 1
                client_writer.write(self._http_resp(
                    "407 Proxy Authentication Required",
                    extra_headers='Proxy-Authenticate: Basic realm="relay"\r\n',
                ))
                await client_writer.drain()
                LOGGER.debug("HTTP proxy auth failed for %s", peername)
                return False

            if not CONTROLS.proxy_enabled:
                STATS.errors += 1
                STATS.refused += 1
                client_writer.write(self._http_resp("503 Service Unavailable",
                    b"proxy is paused by operator\n"))
                await client_writer.drain()
                return False
            if CONTROLS.limit_exceeded():
                STATS.errors += 1
                STATS.refused += 1
                client_writer.write(self._http_resp("509 Bandwidth Limit Exceeded",
                    b"traffic limit reached\n"))
                await client_writer.drain()
                return False

            initial_upstream_payload = b""
            if method == b"CONNECT":
                try:
                    host, port = self._parse_authority(target_b.decode("ascii", "replace"))
                except (ValueError, UnicodeDecodeError):
                    client_writer.write(self._http_resp("400 Bad Request"))
                    await client_writer.drain()
                    return False
            else:
                target = target_b.decode("iso-8859-1", "replace")
                if target.lower().startswith("http://") or target.lower().startswith("https://"):
                    scheme, _, after = target.partition("://")
                    slash = after.find("/")
                    if slash == -1:
                        authority, path = after, "/"
                    else:
                        authority, path = after[:slash], after[slash:]
                    try:
                        host, port = self._parse_authority(authority)
                    except ValueError:
                        client_writer.write(self._http_resp("400 Bad Request"))
                        await client_writer.drain()
                        return False
                    if "://" in target and ":" not in authority:
                        port = 443 if scheme.lower() == "https" else 80
                else:
                    host_hdr = headers.get("host", "")
                    if not host_hdr:
                        client_writer.write(self._http_resp("400 Bad Request",
                            b"missing Host header for non-absolute request\n"))
                        await client_writer.drain()
                        return False
                    try:
                        host, port = self._parse_authority(host_hdr)
                    except ValueError:
                        client_writer.write(self._http_resp("400 Bad Request"))
                        await client_writer.drain()
                        return False
                    path = target
                rebuilt_lines = [
                    method.decode("ascii", "replace") + " " + path + " " + version_b.decode("ascii", "replace"),
                ]
                hop_by_hop = {
                    "proxy-authorization", "proxy-connection", "connection",
                    "keep-alive", "te", "trailer", "transfer-encoding", "upgrade",
                }
                for ln in lines[1:]:
                    if b":" not in ln:
                        continue
                    k, _, v = ln.partition(b":")
                    name = k.strip().lower().decode("ascii", "replace")
                    if name in hop_by_hop:
                        continue
                    rebuilt_lines.append(
                        k.strip().decode("iso-8859-1", "replace") + ": "
                        + v.strip().decode("iso-8859-1", "replace")
                    )
                rebuilt_lines.append("Connection: close")
                initial_upstream_payload = (
                    ("\r\n".join(rebuilt_lines) + "\r\n\r\n").encode("iso-8859-1", "replace")
                    + leftover
                )

            LOGGER.debug("HTTP proxy %s -> %s:%d (%s)", peername, host, port, method.decode())

            if CONTROLS.is_blocked(host):
                STATS.errors += 1
                STATS.refused += 1
                client_writer.write(self._http_resp("403 Forbidden",
                    f"destination not on whitelist (strict): {host}\n".encode("utf-8", "replace")))
                await client_writer.drain()
                return False

            bypass = CONTROLS.should_bypass(host)
            try:
                req = build_socks_request_from_hostport(host, port)
            except SocksRequestError:
                client_writer.write(self._http_resp("400 Bad Request"))
                await client_writer.drain()
                return False

            try:
                if bypass:
                    upstream_reader, upstream_writer, _ = await open_direct_tunnel(req)
                else:
                    upstream_reader, upstream_writer, _ = await open_upstream_tunnel(self.upstream, req)
            except SocksRequestError as exc:
                STATS.errors += 1
                STATS.refused += 1
                LOGGER.debug("HTTP proxy upstream refused %s: %s", host, exc)
                client_writer.write(self._http_resp("502 Bad Gateway",
                    f"upstream refused: {exc}\n".encode("utf-8", "replace")))
                await client_writer.drain()
                return client_keep_alive
            _set_tcp_nodelay(upstream_writer.get_extra_info("socket"))

            if method == b"CONNECT":
                client_writer.write(b"HTTP/1.1 200 Connection Established\r\nProxy-Agent: socks5-relay\r\n\r\n")
                await client_writer.drain()
            else:
                upstream_writer.write(initial_upstream_payload)
                await upstream_writer.drain()

            tunnel_established = True
            STATS.active += 1
            STATS.total += 1
            if STATS.active > STATS.peak_active:
                STATS.peak_active = STATS.active
            if bypass:
                CONTROLS.bypassed += 1
                CONTROLS.bypassed_active += 1
            host_key = f"{host}:{port}"
            host_stats = STATS.hosts[host_key]
            host_stats.active += 1
            host_stats.total += 1

            self._live_writers.add(client_writer)
            client_writer_tracked = True
            self._live_writers.add(upstream_writer)

            if method == b"CONNECT":
                c2u = asyncio.create_task(relay_stream(client_reader, upstream_writer, "up", host_stats))
                u2c = asyncio.create_task(relay_stream(upstream_reader, client_writer, "down", host_stats))
                done, pending = await asyncio.wait({c2u, u2c}, return_when=asyncio.FIRST_COMPLETED)

                for task in pending:
                    if task is c2u:
                        await close_writer(upstream_writer)
                    elif task is u2c:
                        await close_writer(client_writer)

                if pending:
                    try:
                        await asyncio.wait_for(
                            asyncio.shield(asyncio.gather(*pending, return_exceptions=True)),
                            timeout=1.0,
                        )
                    except asyncio.TimeoutError:
                        for task in pending:
                            task.cancel()
                        for task in pending:
                            try:
                                await task
                            except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError, OSError):
                                pass

                for task in done:
                    try:
                        task.result()
                    except (asyncio.CancelledError, ConnectionResetError, BrokenPipeError, OSError):
                        pass
                    except Exception:
                        LOGGER.debug("CONNECT relay task error for %s", peername, exc_info=True)

                return False

            try:
                while True:
                    data = await upstream_reader.read(65536)
                    if not data:
                        break
                    n = len(data)
                    STATS.bytes_down += n
                    if host_stats is not None:
                        host_stats.bytes_down += n
                        host_stats.last_ts = time.monotonic()
                    if not CONTROLS.proxy_enabled or CONTROLS.limit_exceeded():
                        client_keep_alive = False
                        break
                    client_writer.write(data)
                    await client_writer.drain()
            except (ConnectionResetError, BrokenPipeError, OSError):
                return False
            return client_keep_alive

        finally:
            if tunnel_established:
                STATS.active = max(0, STATS.active - 1)
                if bypass:
                    CONTROLS.bypassed_active = max(0, CONTROLS.bypassed_active - 1)
                if host_stats is not None:
                    host_stats.active = max(0, host_stats.active - 1)
            if upstream_writer is not None:
                self._live_writers.discard(upstream_writer)
                await close_writer(upstream_writer)
            if client_writer_tracked:
                self._live_writers.discard(client_writer)


def parse_args() -> argparse.Namespace:
    settings = load_settings()

    parser = argparse.ArgumentParser(
        description="Expose a local authenticated SOCKS5 proxy that forwards through an upstream SOCKS5 proxy.",
    )
    parser.add_argument("--listen-host", default=settings.proxy_ip_listen, help=f"Local IP to bind (default: {settings.proxy_ip_listen})")
    parser.add_argument("--listen-port", type=int, default=settings.proxy_port, help=f"Local port to bind (default: {settings.proxy_port})")
    parser.add_argument("--upstream-host", default=settings.upstream_proxy, help="Upstream SOCKS5 host")
    parser.add_argument("--upstream-port", type=int, default=settings.upstream_port, help="Upstream SOCKS5 port")
    parser.add_argument("--username", help="Username required by local clients (omit to use settings.json)")
    parser.add_argument("--password", help="Password required by local clients (omit to use settings.json)")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity",
    )
    parser.add_argument(
        "--web-host",
        default=settings.site_ip_listen,
        help=f"Host for the web dashboard (default: {settings.site_ip_listen})",
    )
    parser.add_argument(
        "--web-port",
        type=int,
        default=settings.site_port,
        help="Port for the web dashboard (0 disables the web UI)",
    )
    parser.add_argument(
        "--bandwidth-kbps",
        type=int,
        default=settings.bandwidth_limit_kbps,
        help="Global bandwidth cap in KB/s across all tunnels (0 = unlimited)",
    )
    args = parser.parse_args()

    if args.username is None:
        args.username = os.environ.get("SOCKS5_USERNAME") or settings.default_socks_user or None
    if args.username is None:
        args.username = prompt_required_value("Local SOCKS5 username: ", strip=True)
    elif not args.username.strip():
        parser.error("username must not be empty")

    if args.password is None:
        args.password = os.environ.get("SOCKS5_PASSWORD") or settings.default_socks_password or None
    if args.password is None:
        args.password = prompt_required_value("Local SOCKS5 password: ", secret=True)
    elif not args.password:
        parser.error("password must not be empty")

    args.login_need = bool(settings.login_need)
    args.login_user = settings.login_user or ""
    args.login_password = settings.login_password or ""
    args.max_conn_total = int(settings.max_conn_total)
    args.max_conn_per_client = int(settings.max_conn_per_client)
    args.geoip_enabled = bool(settings.geoip_enabled)
    args.auth_required = bool(settings.auth_required)
    args.panel_ip_restricted = bool(settings.panel_ip_restricted)
    args.allowed_panel_ips = list(settings.allowed_panel_ips or [])
    return args


async def run_server(args: argparse.Namespace) -> None:
    relay = AuthenticatedSocksRelay(
        upstream=UpstreamProxy(host=args.upstream_host, port=args.upstream_port),
        credentials=LocalAuth(username=args.username, password=args.password),
    )

    CONTROLS.listen_host = args.listen_host
    CONTROLS.listen_port = args.listen_port
    try:
        CONTROLS.bandwidth_limit_bps = max(0, int(getattr(args, "bandwidth_kbps", 0)) * 1024)
    except (TypeError, ValueError):
        CONTROLS.bandwidth_limit_bps = 0
    CONTROLS.max_conn_total = max(0, int(getattr(args, "max_conn_total", 0) or 0))
    CONTROLS.max_conn_per_client = max(0, int(getattr(args, "max_conn_per_client", 0) or 0))
    CONTROLS.geoip_enabled = bool(getattr(args, "geoip_enabled", False))
    CONTROLS.auth_required = bool(getattr(args, "auth_required", True))
    try:
        import geoip as _geoip
        _geoip.set_enabled(CONTROLS.geoip_enabled)
        _geoip.start_worker()
    except Exception:
        LOGGER.debug("geoip worker failed to start", exc_info=True)

    current: dict[str, asyncio.base_events.Server | None] = {"server": None}

    async def _bind_socks(port: int) -> None:
        new_server = await asyncio.start_server(
            relay.dispatch,
            host=args.listen_host,
            port=port,
            family=socket.AF_INET,
            start_serving=True,
            backlog=512,
        )
        old = current["server"]
        current["server"] = new_server
        CONTROLS.listen_port = port
        bound = ", ".join(str(s.getsockname()) for s in (new_server.sockets or []))
        LOGGER.info("SOCKS5 + HTTP relay listening on %s", bound)
        if old is not None:
            old.close()
            try:
                await old.wait_closed()
            except Exception:
                pass

    def _hard_kill() -> None:
        os._exit(1)

    set_control_plane(ControlPlane(
        rebind_socks=_bind_socks,
        trigger_kill=_hard_kill,
        drop_tunnels=relay.drop_all_tunnels,
        update_credentials=relay.update_credentials,
        get_username=lambda: relay.credentials.username,
        get_password=lambda: relay.credentials.password,
        check_upstream=relay.check_upstream_public_ip,
    ))

    await _bind_socks(args.listen_port)
    LOGGER.info("Upstream SOCKS5 proxy: %s:%d", args.upstream_host, args.upstream_port)

    dashboard_login_enabled = bool(getattr(args, "login_need", False))
    dashboard_user = getattr(args, "login_user", "") or ""
    dashboard_password = getattr(args, "login_password", "") or ""

    set_web_auth(
        enabled=dashboard_login_enabled,
        username=dashboard_user,
        password=dashboard_password,
    )

    panel_restricted = bool(getattr(args, "panel_ip_restricted", False))
    allowed_ips = {
        str(ip).strip()
        for ip in (getattr(args, "allowed_panel_ips", []) or [])
        if str(ip).strip()
    }
    if panel_restricted:
        if not allowed_ips:
            detected_ip = detect_current_user_ip().strip()
            if detected_ip:
                allowed_ips.add(detected_ip)
        allowed_ips.add("127.0.0.1")
        allowed_ips.add("::1")
    set_panel_ip_acl(panel_restricted, sorted(allowed_ips))

    web_server: asyncio.base_events.Server | None = None
    if getattr(args, "web_port", 0):
        dashboard_is_public = not _is_loopback_bind_host(args.web_host)
        if dashboard_is_public and not dashboard_login_enabled and not panel_restricted:
            LOGGER.error(
                "Web dashboard disabled - refusing to expose %s:%d without login or IP ACL",
                args.web_host,
                args.web_port,
            )
        else:
            if (dashboard_is_public and dashboard_login_enabled and not panel_restricted
                    and (_looks_like_default_secret(dashboard_user)
                         or _looks_like_default_secret(dashboard_password))):
                LOGGER.warning(
                    "Web dashboard is exposed without IP ACL and uses weak/default login credentials"
                )
            try:
                web_server = await start_web_dashboard(
                    host=args.web_host,
                    port=args.web_port,
                    listen_addr=f"{args.listen_host}:{args.listen_port}",
                    upstream_addr=f"{args.upstream_host}:{args.upstream_port}",
                )
            except OSError as exc:
                LOGGER.warning(
                    "Web dashboard disabled — cannot bind %s:%d (%s)",
                    args.web_host, args.web_port, exc,
                )
                web_server = None

    sampler_task = asyncio.create_task(stats_sampler_loop())

    try:
        await asyncio.Event().wait()
    finally:
        sampler_task.cancel()
        try:
            await sampler_task
        except (asyncio.CancelledError, Exception):
            pass
        if current["server"] is not None:
            current["server"].close()
            try:
                await current["server"].wait_closed()
            except Exception:
                pass
        if web_server is not None:
            web_server.close()
            try:
                await web_server.wait_closed()
            except Exception:
                pass
        set_control_plane(None)


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))


def main() -> None:
    args = parse_args()
    configure_logging(args.log_level)
    _raise_fd_limit()

    try:
        asyncio.run(run_server(args))
    except KeyboardInterrupt:
        LOGGER.info("Relay stopped by user")
    except OSError as exc:
        if exc.errno == 10048:
            LOGGER.error(
                "Cannot bind local SOCKS5 relay to %s:%d because that address is already in use. Stop the other program using this port, or run again with --listen-port <new_port>.",
                args.listen_host,
                args.listen_port,
            )
            raise SystemExit(1) from exc

        LOGGER.error("Failed to start local SOCKS5 relay: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
