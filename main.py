from __future__ import annotations

import os
import sys


def _ensure_src_on_path() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(here, "src")
    if os.path.isdir(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)


def main() -> None:
    _ensure_src_on_path()
    from socks5_auth_relay import main as relay_main
    relay_main()


if __name__ == "__main__":
    main()
