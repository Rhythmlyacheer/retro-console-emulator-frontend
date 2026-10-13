"""ProcessorChain: resolve core, load ROM, run the emulation session."""
from __future__ import annotations

import logging

from retro_frontend.core.job import Job, JobState
from retro_frontend.core.stages import CoreResolveStage, LoadStage, RunStage
from retro_frontend.services.core_registry import CoreRegistry
from retro_frontend.services.session_store import SessionStore

log = logging.getLogger(__name__)


class ProcessorChain:
    def __init__(self, registry: CoreRegistry, sessions: SessionStore) -> None:
        self._stages = [
            CoreResolveStage(registry),
            LoadStage(),
            RunStage(sessions),
        ]

    def process(self, job: Job) -> Job:
        for stage in self._stages:
            job = stage.apply(job)
            if job.state is JobState.FAILED:
                log.error("stage %s failed job %s: %s", stage.name, job.id, job.error)
                break
        return job