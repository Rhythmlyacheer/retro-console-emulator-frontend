"""FrontendApp: owns the Qt loop, the job queue, and the worker pool."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

from retro_frontend.config.schema import FrontendConfig
from retro_frontend.core.job import Job, JobState
from retro_frontend.core.pipeline import Pipeline
from retro_frontend.handlers.cli_ingest import CliIngest
from retro_frontend.handlers.dragdrop_ingest import DragDropIngest
from retro_frontend.handlers.rom_ingest import RomIngest
from retro_frontend.services.core_registry import CoreRegistry
from retro_frontend.services.session_store import SessionStore
from retro_frontend.utils.queue import BoundedJobQueue

log = logging.getLogger(__name__)


@dataclass
class FrontendApp:
    config: FrontendConfig
    registry: CoreRegistry = field(init=False)
    sessions: SessionStore = field(init=False)
    queue: BoundedJobQueue = field(init=False)
    pipeline: Pipeline = field(init=False)

    def __post_init__(self) -> None:
        self.registry = CoreRegistry.from_config(self.config.cores_path)
        self.sessions = SessionStore(self.config.paths.state_dir)
        self.queue = BoundedJobQueue(maxsize=64)
        self.pipeline = Pipeline(
            handlers=[CliIngest(), DragDropIngest(), RomIngest(self.registry)],
            registry=self.registry,
            sessions=self.sessions,
        )

    def run(self, argv: list[str]) -> int:
        for raw in argv:
            job = Job(source=raw, state=JobState.PENDING)
            self.queue.put(job)
        log.info("queued %d job(s) at boot", len(argv))
        # Qt window loop hands control to services.window_host in the real build.
        return self.pipeline.drain(self.queue)