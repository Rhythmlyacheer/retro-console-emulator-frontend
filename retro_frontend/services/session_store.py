"""SessionStore: append-only record of launched sessions, keyed by job id."""
from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path

from retro_frontend.core.job import Job

log = logging.getLogger(__name__)


class SessionStore:
    def __init__(self, state_dir: str | Path) -> None:
        self._dir = Path(state_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._index = self._dir / "sessions.jsonl"

    def record(self, job: Job) -> None:
        line = json.dumps(
            {
                "id": job.id,
                "rom": str(job.rom_path) if job.rom_path else None,
                "core": job.core_name,
                "system": job.system,
                "state": job.state.value,
            }
        )
        with self._index.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def recent(self, limit: int = 20) -> list[dict[str, str]]:
        if not self._index.is_file():
            return []
        lines = self._index.read_text(encoding="utf-8").splitlines()
        return [json.loads(ln) for ln in lines[-limit:]]