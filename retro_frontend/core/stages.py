"""Concrete processor stages. Each stage is a pure-ish Job -> Job transform."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod

from retro_frontend.core.job import Job, JobState
from retro_frontend.services.core_registry import CoreRegistry
from retro_frontend.services.session_store import SessionStore

log = logging.getLogger(__name__)


class Stage(ABC):
    name: str = "stage"

    @abstractmethod
    def apply(self, job: Job) -> Job: ...


class CoreResolveStage(Stage):
    name = "core-resolve"

    def __init__(self, registry: CoreRegistry) -> None:
        self._registry = registry

    def apply(self, job: Job) -> Job:
        if job.system is None:
            job.fail("no system detected during ingest")
            return job
        core = self._registry.for_system(job.system)
        if core is None:
            job.fail(f"no core registered for system={job.system!r}")
            return job
        job.core_name = core.name
        return job


class LoadStage(Stage):
    name = "load"

    def apply(self, job: Job) -> Job:
        if job.rom_path is None or not job.rom_path.is_file():
            job.fail("rom path missing or unreadable")
            return job
        job.state = JobState.RUNNING
        return job


class RunStage(Stage):
    name = "run"

    def __init__(self, sessions: SessionStore) -> None:
        self._sessions = sessions

    def apply(self, job: Job) -> Job:
        # The real build hands the job to services.window_host which owns
        # the ctypes retro_run() loop. Here we record the session and finish.
        self._sessions.record(job)
        job.state = JobState.DONE
        return job