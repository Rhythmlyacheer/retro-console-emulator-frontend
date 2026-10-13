"""BoundedJobQueue: tiny thread-safe FIFO with a hard cap."""
from __future__ import annotations

import queue

from retro_frontend.core.job import Job


class BoundedJobQueue:
    def __init__(self, maxsize: int = 64) -> None:
        self._q: queue.Queue[Job] = queue.Queue(maxsize=maxsize)

    def put(self, job: Job) -> None:
        self._q.put_nowait(job)

    def get(self) -> Job:
        return self._q.get_nowait()

    def empty(self) -> bool:
        return self._q.empty()

    def __len__(self) -> int:
        return self._q.qsize()