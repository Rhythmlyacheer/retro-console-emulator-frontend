"""Resolve per-user data directories for saves, states, and config."""
from __future__ import annotations

from pathlib import Path

import platformdirs

_APP = "retro-frontend"


def data_dir() -> Path:
    return Path(platformdirs.user_data_dir(_APP))


def state_dir() -> Path:
    return data_dir() / "states"


def token_path() -> Path:
    return data_dir() / "ipc.token"