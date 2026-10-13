"""RomRecord: one row in the scanned library."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RomRecord:
    path: Path
    system: str
    title: str
    size_kb: int
    crc32: str | None = None

    @property
    def display(self) -> str:
        return f"{self.title} [{self.system}]"