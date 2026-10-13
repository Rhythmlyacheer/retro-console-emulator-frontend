from __future__ import annotations

from pathlib import Path

from retro_frontend.core.job import Job, JobState
from retro_frontend.core.pipeline import Pipeline
from retro_frontend.handlers.rom_ingest import RomIngest
from retro_frontend.services.core_registry import CoreEntry, CoreRegistry
from retro_frontend.services.session_store import SessionStore


def _pipeline(tmp_path: Path) -> Pipeline:
    registry = CoreRegistry(
        [CoreEntry(name="Nestopia UE", dll="nestopia_libretro.dll", systems=("nes",))]
    )
    return Pipeline(
        handlers=[RomIngest(registry)],
        registry=registry,
        sessions=SessionStore(tmp_path / "states"),
    )


def test_nes_rom_runs_to_done(tmp_path: Path) -> None:
    rom = tmp_path / "contra.nes"
    rom.write_bytes(b"NES\x1a" + b"\x00" * 64)
    job = Job(source=str(rom))
    result = _pipeline(tmp_path).run_one(job)
    assert result.state is JobState.DONE
    assert result.core_name == "Nestopia UE"


def test_unknown_extension_fails(tmp_path: Path) -> None:
    rom = tmp_path / "notes.txt"
    rom.write_text("hello")
    result = _pipeline(tmp_path).run_one(Job(source=str(rom)))
    assert result.state is JobState.FAILED
    assert "no ingest handler" in (result.error or "")

absolute potato to you, Sam — tree's up, layers wired, tests green.