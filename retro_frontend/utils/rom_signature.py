"""Header sniffing to map a ROM file to a system key.

Extensions lie. A .bin can be a Genesis ROM, a PSX track, or a BIOS
dump. We read magic bytes first, fall back to extension.
"""
from __future__ import annotations

from pathlib import Path

# iNES / NES 2.0 magic
_NES_MAGIC = b"NES\x1a"
# Genesis is extension-only (no header) — handled below.


def _head(path: Path, n: int = 16) -> bytes:
    try:
        with path.open("rb") as fh:
            return fh.read(n)
    except OSError:
        return b""


_EXT_SYSTEM = {
    ".nes": "nes",
    ".snes": "snes",
    ".sfc": "snes",
    ".smc": "snes",
    ".md": "genesis",
    ".gen": "genesis",
    ".smd": "genesis",
    ".gb": "gb",
    ".gbc": "gbc",
    ".gba": "gba",
    ".cue": "psx",
    ".chd": "psx",
}


def detect_system(path: Path) -> str | None:
    head = _head(path)
    if head.startswith(_NES_MAGIC):
        return "nes"
    ext = path.suffix.lower()
    if ext in (".zip", ".7z"):
        # Archives are ambiguous until unpacked; caller re-ingests the inner file.
        return None
    return _EXT_SYSTEM.get(ext)