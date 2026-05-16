from __future__ import annotations

import asyncio
import getpass
import os
import socket
import subprocess
import sys


async def close_writer(writer: asyncio.StreamWriter | None) -> None:
    if writer is None or writer.is_closing():
        return

    writer.close()
    try:
        await writer.wait_closed()
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass


def set_tcp_nodelay(sock: socket.socket | None) -> None:
    if sock is None:
        return
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    except (OSError, AttributeError):
        pass


def prompt_required_value(prompt: str, *, secret: bool = False, strip: bool = False) -> str:
    while True:
        try:
            value = getpass.getpass(prompt) if secret else input(prompt)
        except EOFError as exc:
            raise SystemExit(
                "Input stream is closed. Pass the value with command-line arguments instead."
            ) from exc
        except KeyboardInterrupt as exc:
            print(file=sys.stderr)
            raise SystemExit("Cancelled by user.") from exc

        if strip:
            value = value.strip()

        if value:
            return value

        print("Value must not be empty. Please try again.", file=sys.stderr)


def detect_current_user_ip() -> str:
    if ssh_client:
        parts = ssh_client.split()
        if parts:
            return parts[0]
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if ip and ip != "0.0.0.0":
                return ip
    except OSError:
        pass

    if sys.platform != "win32":
        try:
            result = subprocess.run(
                ["who"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split("\n")
                for line in reversed(lines):
                    if "(" in line and ")" in line:
                        try:
                            ip = line.split("(")[-1].split(")")[0]
                            if ip and ip != ":0":
                                return ip
                        except (IndexError, ValueError):
                            pass
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
    
    return "127.0.0.1"
