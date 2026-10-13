"""RomIngest: classify a ROM path, detect its system, stamp the job."""
from __future__ import annotations

import logging
from pathlib import Path

from retro_frontend.core.job import Job, JobState
from retro_frontend.handlers.base import IngestHandler
from retro_frontend.services.core_registry import CoreRegistry
from retro_frontend.utils.rom_signature import detect_system

log = logging.getLogger(__name__)

_ROM_EXTS = {
    ".nes", ".snes", ".sfc", ".smc", ".md", ".gen", ".smd",
    ".gb", ".gbc", ".gba", ".bin", ".cue", ".chd", ".zip", ".7z",
}


class RomIngest(IngestHandler):
    name = "rom-ingest"

    def __init__(self, registry: CoreRegistry) -> None:
        self._registry = registry

    def accepts(self, job: Job) -> bool:
        p = Path(job.source)
        return p.suffix.lower() in _ROM_EXTS

    def ingest(self, job: Job) -> None:
        path = Path(job.source).resolve()
        if not path.is_file():
            job.fail(f"rom not found: {path}")
            return
        system = detect_system(path)
        if system is None:
            job.fail(f"could not detect system for {path.name}")
            return
        job.rom_path = path
        job.system = system
        job.meta["ext"] = path.suffix.lower()
        job.meta["size_kb"] = str(path.stat().st_size // 1024)
        job.state = JobState.INGESTED
        log.info("ingested %s as %s", path.name, system)