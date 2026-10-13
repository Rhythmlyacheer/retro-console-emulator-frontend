"""GameMeta: scraped/curated metadata for a ROM."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class GameMeta:
    title: str
    system: str
    year: int | None = None
    publisher: str | None = None
    players: int = 1
    genres: list[str] = field(default_factory=list)

    def matches(self, term: str) -> bool:
        needle = term.casefold()
        haystack = " ".join([self.title, self.publisher or "", *self.genres]).casefold()
        return needle in haystack