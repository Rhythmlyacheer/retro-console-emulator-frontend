"""SaveSlot: in-memory view of a save-state slot on disk."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SaveSlot:
    slot: int
    path: Path
    size_bytes: int

    @property
    def empty(self) -> bool:
        return self.size_bytes == 0

    def label(self) -> str:
        return f"slot {self.slot}" + ("" if self.empty else f" ({self.size_bytes >> 10} KiB)")