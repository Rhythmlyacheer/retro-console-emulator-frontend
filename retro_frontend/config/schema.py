"""Typed config schema mirroring config/*.toml."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class WindowConfig:
    title: str
    width: int
    height: int
    scale_mode: str
    vsync: bool
    fullscreen: bool


@dataclass(frozen=True, slots=True)
class VideoConfig:
    shader: str
    scanline_strength: float
    bilinear: bool


@dataclass(frozen=True, slots=True)
class AudioConfig:
    driver: str
    buffer_ms: int
    sample_rate: int


@dataclass(frozen=True, slots=True)
class PathsConfig:
    rom_library: str
    save_dir: str
    state_dir: str


@dataclass(frozen=True, slots=True)
class FrontendConfig:
    window: WindowConfig
    video: VideoConfig
    audio: AudioConfig
    paths: PathsConfig
    cores_path: Path
    raw: dict[str, Any]

    @classmethod
    def from_toml(cls, raw: dict[str, Any], *, cores_path: Path) -> "FrontendConfig":
        return cls(
            window=WindowConfig(**raw["window"]),
            video=VideoConfig(**raw["video"]),
            audio=AudioConfig(**raw["audio"]),
            paths=PathsConfig(**raw["paths"]),
            cores_path=cores_path,
            raw=raw,
        )