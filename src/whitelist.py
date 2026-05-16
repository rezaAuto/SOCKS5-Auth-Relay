from __future__ import annotations

import ipaddress
from typing import Final

WHITELIST_PRESETS: Final[dict[str, set[str]]] = {
    "telegram": {
        "telegram.org", "t.me", "telegram.me", "tdesktop.com",
        "telegram-cdn.org", "cdn-telegram.org", "telesco.pe",
    },
    "youtube": {
        "youtube.com", "youtu.be", "ytimg.com", "googlevideo.com",
        "ggpht.com", "youtube-nocookie.com", "youtubei.googleapis.com",
    },
    "github": {
        "github.com", "githubusercontent.com", "githubassets.com",
        "github.io", "ghcr.io", "codeload.github.com",
    },
    "essentials": {
        "google.com", "gstatic.com", "googleapis.com", "googleusercontent.com",
        "cloudflare.com", "cloudflare-dns.com", "cloudflareinsights.com",
        "fastly.net", "akamaihd.net", "akamaized.net", "cloudfront.net",
        "wikipedia.org", "wikimedia.org", "microsoft.com", "mozilla.org",
        "apple.com", "icloud.com", "digicert.com", "letsencrypt.org",
    },
}

# IP CIDRs per preset. Many clients (notably Telegram Desktop) resolve DNS
# locally and send the SOCKS5 destination as a raw IPv4/IPv6 literal, so a
# domain-only whitelist never matches those. These ranges are the officially
# announced Telegram/YouTube/GitHub ASNs.
_WHITELIST_CIDRS_RAW: Final[dict[str, tuple[str, ...]]] = {
    "telegram": (
        "91.105.192.0/23",
        "91.108.4.0/22",
        "91.108.8.0/21",
        "91.108.16.0/21",
        "91.108.36.0/23",
        "91.108.38.0/23",
        "91.108.56.0/22",
        "95.161.64.0/20",
        "109.239.140.0/24",
        "149.154.160.0/20",
        "185.76.151.0/24",
        "2001:67c:4e8::/48",
        "2001:b28:f23c::/48",
        "2001:b28:f23d::/48",
        "2001:b28:f23f::/48",
        "2a0a:f280::/32",
    ),
    "youtube": (
        "8.8.4.0/24", "8.8.8.0/24",
        "34.64.0.0/10", "35.184.0.0/13", "35.192.0.0/14", "35.196.0.0/15",
        "35.198.0.0/16", "35.199.0.0/17", "35.200.0.0/13", "35.208.0.0/12",
        "35.224.0.0/12", "35.240.0.0/13",
        "64.233.160.0/19", "66.102.0.0/20", "66.249.64.0/19",
        "72.14.192.0/18", "74.125.0.0/16",
        "108.177.8.0/21", "108.177.96.0/19",
        "142.250.0.0/15", "172.217.0.0/16", "172.253.0.0/16",
        "173.194.0.0/16", "209.85.128.0/17", "216.58.192.0/19", "216.239.32.0/19",
        "2404:6800::/32", "2607:f8b0::/32", "2800:3f0::/32", "2a00:1450::/32", "2c0f:fb50::/32",
    ),
    "github": (
        "140.82.112.0/20",
        "143.55.64.0/20",
        "185.199.108.0/22",
        "192.30.252.0/22",
        "2a0a:a440::/29",
        "2606:50c0::/32",
    ),
    "essentials": (
        "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
        "104.16.0.0/13", "104.24.0.0/14", "108.162.192.0/18",
        "131.0.72.0/22", "141.101.64.0/18", "162.158.0.0/15",
        "172.64.0.0/13", "173.245.48.0/20", "188.114.96.0/20",
        "190.93.240.0/20", "197.234.240.0/22", "198.41.128.0/17",
        "2400:cb00::/32", "2606:4700::/32", "2803:f800::/32",
        "2405:b500::/32", "2405:8100::/32", "2a06:98c0::/29", "2c0f:f248::/32",
    ),
}


def _compile_cidrs(
    raw: dict[str, tuple[str, ...]],
) -> dict[str, tuple[tuple[ipaddress._BaseNetwork, ...], tuple[ipaddress._BaseNetwork, ...]]]:
    out: dict[str, tuple[tuple[ipaddress._BaseNetwork, ...], tuple[ipaddress._BaseNetwork, ...]]] = {}
    for name, cidrs in raw.items():
        v4: list[ipaddress._BaseNetwork] = []
        v6: list[ipaddress._BaseNetwork] = []
        for c in cidrs:
            try:
                net = ipaddress.ip_network(c, strict=False)
            except ValueError:
                continue
            (v6 if net.version == 6 else v4).append(net)
        out[name] = (tuple(v4), tuple(v6))
    return out


WHITELIST_CIDRS: Final[dict[str, tuple[tuple[ipaddress._BaseNetwork, ...], tuple[ipaddress._BaseNetwork, ...]]]] = \
    _compile_cidrs(_WHITELIST_CIDRS_RAW)


def _parse_ip_literal(host: str) -> ipaddress._BaseAddress | None:
    h = host.strip().strip("[]")
    try:
        return ipaddress.ip_address(h)
    except ValueError:
        return None
