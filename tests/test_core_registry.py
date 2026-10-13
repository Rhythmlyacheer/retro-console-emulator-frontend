from __future__ import annotations

from pathlib import Path

from retro_frontend.services.core_registry import CoreEntry, CoreRegistry


def _registry() -> CoreRegistry:
    return CoreRegistry(
        [
            CoreEntry(name="Nestopia UE", dll="nestopia_libretro.dll", systems=("nes",)),
            CoreEntry(name="mGBA", dll="mgba_libretro.dll", systems=("gba",)),
        ]
    )


def test_lookup_hit() -> None:
    assert _registry().for_system("nes").name == "Nestopia UE"


def test_lookup_miss() -> None:
    assert _registry().for_system("psx") is None


def test_systems_are_sorted() -> None:
    assert _registry().systems == ["gba", "nes"]


def test_from_missing_config_is_empty(tmp_path: Path) -> None:
    assert CoreRegistry.from_config(tmp_path / "nope.toml").systems == []