"""CliIngest: claim bare paths passed on the command line."""
from __future__ import annotations

from pathlib import Path

from retro_frontend.core.job import Job, JobState
from retro_frontend.handlers.base import IngestHandler


class CliIngest(IngestHandler):
    name = "cli-ingest"

    def accepts(self, job: Job) -> bool:
        return job.source.startswith("cli:") or Path(job.source).is_absolute()

    def ingest(self, job: Job) -> None:
        source = job.source.removeprefix("cli:")
        job.meta["origin"] = "cli"
        job.source = source
        job.state = JobState.INGESTED