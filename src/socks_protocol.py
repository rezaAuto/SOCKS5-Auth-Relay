from __future__ import annotations

import asyncio
import socket
import struct
import time
from dataclasses import dataclass
from enum import IntEnum
from typing import Final

from controls import CONTROLS, BANDWIDTH_BUCKET
from stats import ClientStats, HostStats, STATS
from whitelist import _parse_ip_literal

SOCKS_VERSION: Final[int] = 5
BUFFER_SIZE: Final[int] = 256 * 1024


class AuthMethod(IntEnum):
    NO_AUTH = 0x00
    USERNAME_PASSWORD = 0x02
    NO_ACCEPTABLE = 0xFF


class Command(IntEnum):
    CONNECT = 0x01


class AddressType(IntEnum):
    IPV4 = 0x01
    DOMAIN = 0x03
    IPV6 = 0x04


class ReplyCode(IntEnum):
    SUCCEEDED = 0x00
    GENERAL_FAILURE = 0x01
    CONNECTION_NOT_ALLOWED = 0x02
    NETWORK_UNREACHABLE = 0x03
    HOST_UNREACHABLE = 0x04
    CONNECTION_REFUSED = 0x05
    TTL_EXPIRED = 0x06
    COMMAND_NOT_SUPPORTED = 0x07
    ADDRESS_TYPE_NOT_SUPPORTED = 0x08


@dataclass(frozen=True)
class UpstreamProxy:
    host: str
    port: int


@dataclass(frozen=True)
class LocalAuth:
    username: str
    password: str


@dataclass(frozen=True)
class SocksRequest:
    raw: bytes
    destination: str
    port: int


class SocksProtocolError(Exception):
    """Raised when a client or upstream proxy violates SOCKS5 framing."""


class SilentClientDisconnect(Exception):
    """Client closed the TCP connection before sending any SOCKS bytes (noise, not an error)."""


class SocksRequestError(Exception):
    def __init__(self, reply_code: ReplyCode, message: str) -> None:
        super().__init__(message)
        self.reply_code = reply_code


async def read_exact(reader: asyncio.StreamReader, size: int) -> bytes:
    try:
        return await reader.readexactly(size)
    except asyncio.IncompleteReadError as exc:
        if not exc.partial:
            raise SilentClientDisconnect() from exc
        raise SocksProtocolError("connection closed before SOCKS frame was complete") from exc


def build_failure_reply(reply_code: ReplyCode) -> bytes:
    return b"\x05" + bytes([int(reply_code), 0x00, AddressType.IPV4]) + socket.inet_aton("0.0.0.0") + struct.pack("!H", 0)


def map_os_error_to_reply(error: OSError) -> ReplyCode:
    if error.errno in {10061, 111}:
        return ReplyCode.CONNECTION_REFUSED
    if error.errno in {10051, 101}:
        return ReplyCode.NETWORK_UNREACHABLE
    if error.errno in {10065, 113}:
        return ReplyCode.HOST_UNREACHABLE
    if error.errno in {10060, 110}:
        return ReplyCode.TTL_EXPIRED
    return ReplyCode.GENERAL_FAILURE


async def read_address_field(reader: asyncio.StreamReader, atyp: int) -> tuple[bytes, str]:
    if atyp == AddressType.IPV4:
        packed = await read_exact(reader, 4)
        return packed, socket.inet_ntop(socket.AF_INET, packed)

    if atyp == AddressType.DOMAIN:
        length = (await read_exact(reader, 1))[0]
        raw_host = await read_exact(reader, length)
        return bytes([length]) + raw_host, raw_host.decode("idna")

    if atyp == AddressType.IPV6:
        packed = await read_exact(reader, 16)
        return packed, socket.inet_ntop(socket.AF_INET6, packed)

    raise SocksRequestError(ReplyCode.ADDRESS_TYPE_NOT_SUPPORTED, f"unsupported address type: 0x{atyp:02x}")


async def authenticate_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    credentials: LocalAuth,
) -> None:
    header = await read_exact(reader, 2)
    version, method_count = header
    if version != SOCKS_VERSION:
        raise SocksProtocolError(f"unsupported SOCKS version from client: {version}")

    methods = await read_exact(reader, method_count)

    if not CONTROLS.auth_required and AuthMethod.NO_AUTH in methods:
        writer.write(bytes([SOCKS_VERSION, AuthMethod.NO_AUTH]))
        await writer.drain()
        return

    if AuthMethod.USERNAME_PASSWORD not in methods:
        writer.write(bytes([SOCKS_VERSION, AuthMethod.NO_ACCEPTABLE]))
        await writer.drain()
        raise SocksProtocolError("client does not support username/password authentication")

    writer.write(bytes([SOCKS_VERSION, AuthMethod.USERNAME_PASSWORD]))
    await writer.drain()

    auth_version = (await read_exact(reader, 1))[0]
    if auth_version != 0x01:
        writer.write(b"\x01\x01")
        await writer.drain()
        raise SocksProtocolError(f"unsupported auth sub-negotiation version: {auth_version}")

    user_length = (await read_exact(reader, 1))[0]
    username = (await read_exact(reader, user_length)).decode("utf-8", errors="strict")
    password_length = (await read_exact(reader, 1))[0]
    password = (await read_exact(reader, password_length)).decode("utf-8", errors="strict")

    if username != credentials.username or password != credentials.password:
        writer.write(b"\x01\x01")
        await writer.drain()
        raise SocksProtocolError("invalid username/password from client")

    writer.write(b"\x01\x00")
    await writer.drain()


async def read_client_request(reader: asyncio.StreamReader) -> SocksRequest:
    header = await read_exact(reader, 4)
    version, command, _reserved, atyp = header

    if version != SOCKS_VERSION:
        raise SocksProtocolError(f"unexpected SOCKS request version: {version}")

    if command != Command.CONNECT:
        raise SocksRequestError(ReplyCode.COMMAND_NOT_SUPPORTED, f"unsupported SOCKS command: 0x{command:02x}")

    address_field, destination = await read_address_field(reader, atyp)
    port_bytes = await read_exact(reader, 2)
    port = struct.unpack("!H", port_bytes)[0]

    raw_request = bytes([SOCKS_VERSION, command, 0x00, atyp]) + address_field + port_bytes
    return SocksRequest(raw=raw_request, destination=destination, port=port)


async def read_server_reply(reader: asyncio.StreamReader) -> tuple[int, bytes]:
    header = await read_exact(reader, 4)
    version, reply_code, _reserved, atyp = header
    if version != SOCKS_VERSION:
        raise SocksProtocolError(f"unexpected SOCKS reply version: {version}")

    address_field, _ = await read_address_field(reader, atyp)
    port_bytes = await read_exact(reader, 2)
    return reply_code, header + address_field + port_bytes


async def open_upstream_tunnel(
    upstream: UpstreamProxy,
    request: SocksRequest,
) -> tuple[asyncio.StreamReader, asyncio.StreamWriter, bytes]:
    upstream_reader, upstream_writer = await asyncio.open_connection(upstream.host, upstream.port)

    upstream_writer.write(bytes([SOCKS_VERSION, 0x01, AuthMethod.NO_AUTH]))
    await upstream_writer.drain()

    method_reply = await read_exact(upstream_reader, 2)
    if method_reply != bytes([SOCKS_VERSION, AuthMethod.NO_AUTH]):
        raise SocksRequestError(ReplyCode.CONNECTION_NOT_ALLOWED, "upstream proxy rejected no-auth method")

    upstream_writer.write(request.raw)
    await upstream_writer.drain()

    reply_code, raw_reply = await read_server_reply(upstream_reader)
    if reply_code != ReplyCode.SUCCEEDED:
        raise SocksRequestError(ReplyCode(reply_code), f"upstream proxy refused destination with code 0x{reply_code:02x}")

    return upstream_reader, upstream_writer, raw_reply


async def open_direct_tunnel(
    request: SocksRequest,
) -> tuple[asyncio.StreamReader, asyncio.StreamWriter, bytes]:
    try:
        reader, writer = await asyncio.open_connection(request.destination, request.port)
    except OSError as exc:
        raise SocksRequestError(map_os_error_to_reply(exc), f"direct connect failed: {exc}") from exc

    sockname = writer.get_extra_info("sockname") or ("0.0.0.0", 0)
    try:
        packed = socket.inet_aton(sockname[0])
    except (OSError, TypeError):
        packed = socket.inet_aton("0.0.0.0")
    port_val = sockname[1] if isinstance(sockname[1], int) else 0
    reply = (
        bytes([SOCKS_VERSION, int(ReplyCode.SUCCEEDED), 0x00, int(AddressType.IPV4)])
        + packed
        + struct.pack("!H", port_val)
    )
    return reader, writer, reply


def build_socks_request_from_hostport(host: str, port: int) -> SocksRequest:
    ip = _parse_ip_literal(host)
    if ip is not None and ip.version == 4:
        atyp = AddressType.IPV4
        addr_field = ip.packed
    elif ip is not None and ip.version == 6:
        atyp = AddressType.IPV6
        addr_field = ip.packed
    else:
        atyp = AddressType.DOMAIN
        try:
            hb = host.encode("idna")
        except UnicodeError:
            hb = host.encode("ascii", "ignore")
        if len(hb) > 255:
            raise SocksRequestError(
                ReplyCode.ADDRESS_TYPE_NOT_SUPPORTED,
                "hostname too long for SOCKS5",
            )
        addr_field = bytes([len(hb)]) + hb
    port_bytes = struct.pack("!H", int(port) & 0xFFFF)
    raw = bytes([SOCKS_VERSION, int(Command.CONNECT), 0x00, int(atyp)]) + addr_field + port_bytes
    return SocksRequest(raw=raw, destination=host, port=int(port))


async def relay_stream(
    source: asyncio.StreamReader,
    destination: asyncio.StreamWriter,
    direction: str = "up",
    host_stats: "HostStats | None" = None,
    client_stats: "ClientStats | None" = None,
) -> None:
    try:
        is_upstream = direction == "up"
        batched_bytes = 0
        batched_host_bytes = 0
        batched_client_bytes = 0
        last_update_ts = time.monotonic()
        update_interval = 0.1

        def _flush_stats(now: float) -> None:
            nonlocal batched_bytes, batched_host_bytes, batched_client_bytes
            if batched_bytes <= 0 and batched_host_bytes <= 0 and batched_client_bytes <= 0:
                return

            if is_upstream:
                STATS.bytes_up += batched_bytes
                if host_stats is not None:
                    host_stats.bytes_up += batched_host_bytes
                    host_stats.last_ts = now
                if client_stats is not None:
                    client_stats.bytes_up += batched_client_bytes
                    client_stats.last_activity_ts = now
            else:
                STATS.bytes_down += batched_bytes
                if host_stats is not None:
                    host_stats.bytes_down += batched_host_bytes
                    host_stats.last_ts = now
                if client_stats is not None:
                    client_stats.bytes_down += batched_client_bytes
                    client_stats.last_activity_ts = now

            batched_bytes = 0
            batched_host_bytes = 0
            batched_client_bytes = 0
        
        while True:
            data = await source.read(BUFFER_SIZE)
            if not data:
                _flush_stats(time.monotonic())

                if destination.can_write_eof() and not destination.is_closing():
                    try:
                        destination.write_eof()
                    except (OSError, RuntimeError):
                        pass
                break

            n = len(data)
            batched_bytes += n
            batched_host_bytes += n if host_stats is not None else 0
            batched_client_bytes += n if client_stats is not None else 0

            now = time.monotonic()
            if now - last_update_ts >= update_interval:
                _flush_stats(now)
                last_update_ts = now

            if not CONTROLS.proxy_enabled or CONTROLS.limit_exceeded():
                break

            await BANDWIDTH_BUCKET.consume(n)

            destination.write(data)
            await destination.drain()
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
