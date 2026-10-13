"""Job: the unit that flows through ingest -> process -> output."""
from __future__ import annotations

import enum
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path


class JobState(enum.StrEnum):
    PENDING = "pending"
    INGESTED = "ingested"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass(slots=True)
class Job:
    source: str
    state: JobState = JobState.PENDING
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    rom_path: Path | None = None
    core_name: str | None = None
    system: str | None = None
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    meta: dict[str, str] = field(default_factory=dict)

    def fail(self, reason: str) -> None:
        self.state = JobState.FAILED
        self.error = reason

    @property
    def age_ms(self) -> float:
        return (time.time() - self.created_at) * 1000.0