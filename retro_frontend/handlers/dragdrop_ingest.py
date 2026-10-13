"""DragDropIngest: claim dropped files/URIs from the Qt window."""
from __future__ import annotations

from retro_frontend.core.job import Job, JobState
from retro_frontend.handlers.base import IngestHandler


class DragDropIngest(IngestHandler):
    name = "dragdrop-ingest"

    def accepts(self, job: Job) -> bool:
        return job.source.startswith("file://")

    def ingest(self, job: Job) -> None:
        from urllib.parse import unquote, urlparse

        parsed = urlparse(job.source)
        job.source = unquote(parsed.path.lstrip("/"))
        job.meta["origin"] = "dragdrop"
        job.state = JobState.INGESTED