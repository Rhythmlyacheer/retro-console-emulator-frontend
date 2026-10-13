"""IngestHandler ABC: accepts(job) -> ingest(job)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from retro_frontend.core.job import Job


class IngestHandler(ABC):
    name: str = "handler"

    @abstractmethod
    def accepts(self, job: Job) -> bool: ...

    @abstractmethod
    def ingest(self, job: Job) -> None: ...