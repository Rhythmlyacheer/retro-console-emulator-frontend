"""CoreRegistry: map systems -> libretro core DLLs from cores.toml."""
from __future__ import annotations

import logging
import tomllib
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class CoreEntry:
    name: str
    dll: str
    systems: tuple[str, ...]
    accuracy: str = "cycle"
    requires_bios: bool = False


class CoreRegistry:
    def __init__(self, entries: list[CoreEntry]) -> None:
        self._by_system: dict[str, CoreEntry] = {}
        for entry in entries:
            for system in entry.systems:
                if system in self._by_system:
                    log.warning("system %s claimed twice; keeping %s", system, entry.name)
                    continue
                self._by_system[system] = entry

    @classmethod
    def from_config(cls, cores_path: Path) -> "CoreRegistry":
        if not cores_path.is_file():
            log.warning("no cores.toml at %s; registry empty", cores_path)
            return cls([])
        with cores_path.open("rb") as fh:
            raw = tomllib.load(fh)
        entries = [
            CoreEntry(
                name=spec["name"],
                dll=spec["dll"],
                systems=tuple(spec["systems"]),
                accuracy=spec.get("accuracy", "cycle"),
                requires_bios=spec.get("requires_bios", False),
            )
            for spec in raw.get("cores", {}).values()
        ]
        return cls(entries)

    def for_system(self, system: str) -> CoreEntry | None:
        return self._by_system.get(system)

    @property
    def systems(self) -> list[str]:
        return sorted(self._by_system)