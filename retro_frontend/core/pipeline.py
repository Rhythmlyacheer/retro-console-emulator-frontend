"""Pipeline: drive jobs through ingest handlers, processors, output drivers."""
from __future__ import annotations

import logging
from collections.abc import Sequence

from retro_frontend.core.job import Job, JobState
from retro_frontend.core.processor import ProcessorChain
from retro_frontend.handlers.base import IngestHandler
from retro_frontend.services.core_registry import CoreRegistry
from retro_frontend.services.session_store import SessionStore
from retro_frontend.utils.queue import BoundedJobQueue

log = logging.getLogger(__name__)


class Pipeline:
    """Ordered ingest handlers + a processor chain. Handlers are tried in
    order; the first that claims a job stamps it and moves on."""

    def __init__(
        self,
        handlers: Sequence[IngestHandler],
        registry: CoreRegistry,
        sessions: SessionStore,
    ) -> None:
        self._handlers = list(handlers)
        self._chain = ProcessorChain(registry=registry, sessions=sessions)

    def run_one(self, job: Job) -> Job:
        for handler in self._handlers:
            if handler.accepts(job):
                handler.ingest(job)
                break
        else:
            job.fail("no ingest handler accepted source")
            return job
        if job.state is JobState.INGESTED:
            self._chain.process(job)
        return job

    def drain(self, queue: BoundedJobQueue) -> int:
        failures = 0
        while not queue.empty():
            job = queue.get()
            self.run_one(job)
            if job.state is JobState.FAILED:
                failures += 1
                log.warning("job %s failed: %s", job.id, job.error)
        return failures