"""Read frontend.toml + cores.toml off disk into typed config objects."""
from __future__ import annotations

import tomllib
from pathlib import Path

from retro_frontend.config.schema import FrontendConfig

_DEFAULTS = Path("config")


def load_config(root: Path | None = None) -> FrontendConfig:
    base = root or _DEFAULTS
    frontend_path = base / "frontend.toml"
    cores_path = base / "cores.toml"
    if not frontend_path.is_file():
        raise FileNotFoundError(f"missing config: {frontend_path}")
    with frontend_path.open("rb") as fh:
        raw = tomllib.load(fh)
    return FrontendConfig.from_toml(raw, cores_path=cores_path)