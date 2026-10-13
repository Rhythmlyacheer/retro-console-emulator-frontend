# Contributing to retro-console-emulator-frontend

Thanks for wanting to push pixels. This project is a Windows desktop
frontend that wraps libretro cores and presents a controller-first UI
for NES, SNES, Genesis, GB/GBC/GBA, PSX and arcade sets.

## Ground rules

- Python 3.12+ on Windows 10/11. Cores are loaded as DLLs via ctypes.
- One feature per PR. Keep diffs readable.
- Run `pytest -q` and `ruff check .` before opening a PR. CI does both.
- New cores go through `services/core_registry.py` — do not hardcode
  DLL paths anywhere else.

## Pipeline architecture

Everything is a pipeline: an **ingest handler** turns a raw input
(file path, CLI arg, drag-drop, IPC message) into a `Job`; a
**processor** stage mutates the `Job` through the emulation lifecycle;
an **output driver** writes the result (window surface, save state,
screenshot, log). If you can't slot your change into one of those
three, open an issue first.

## Adding a core

1. Drop the DLL in `cores/bin/`.
2. Add an entry to `config/cores.toml` with `name`, `dll`, `systems`.
3. Add a smoke test in `tests/test_core_registry.py`.

## Style

- `ruff` + `black`, line length 100.
- Type hints on all public functions. `mypy --strict` on `core/`.
- No global mutable state outside `services/session_store.py`.

## Commit messages

`area: short imperative summary` — e.g. `input: add XInput rumble passthrough`.