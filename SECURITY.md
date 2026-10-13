# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 2026.x  | yes       |
| 2025.x  | security fixes only |

## What this project does and does not do

This frontend loads **user-supplied libretro cores** as native DLLs.
Core binaries execute with the same privileges as the frontend process.
We do not ship cores in this repository — you source them yourself and
are responsible for their provenance.

## Reporting a vulnerability

Email `security@retro-frontend.example` with a repro. Do not open a
public issue for memory-safety bugs in the ctypes bridge — those are
exploitable and we'll coordinate disclosure.

In scope:
- Out-of-bounds reads/writes in `core/libretro_bridge.py`
- Path traversal in `handlers/rom_ingest.py` (zip/slip handling)
- Save-state deserialization in `services/state_serializer.py`
- IPC command injection in `services/ipc_server.py`

Out of scope:
- Crashes caused by a malicious or broken third-party core DLL
- Cheats/Game Genie codes the user applies themselves

## Hardening notes

- Cores are loaded with `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS` where possible.
- The IPC server binds to `127.0.0.1` only and requires a per-session token.
- Save-state blobs are length-prefixed and checksummed before load.