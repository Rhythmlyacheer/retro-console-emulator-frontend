"""Local IPC server: single-instance handoff and remote 'launch rom' calls.

Binds 127.0.0.1 only. Every request must carry the per-session token
written to %LOCALAPPDATA%/retro-frontend/ipc.token at boot.
"""
from __future__ import annotations

import json
import logging
import secrets
import socket
import threading
from pathlib import Path

log = logging.getLogger(__name__)

_HOST = "127.0.0.1"
_PORT = 51739


class IpcServer:
    def __init__(self, token_path: Path) -> None:
        self._token = secrets.token_hex(16)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(self._token, encoding="utf-8")
        self._sock: socket.socket | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((_HOST, _PORT))
        self._sock.listen(4)
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()
        log.info("ipc listening on %s:%d", _HOST, _PORT)

    def _serve(self) -> None:
        assert self._sock is not None
        while True:
            conn, _ = self._sock.accept()
            with conn:
                payload = conn.recv(4096).decode("utf-8", "replace")
                try:
                    msg = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                if msg.get("token") != self._token:
                    log.warning("ipc: rejected request with bad token")
                    continue
                log.info("ipc: launch %s", msg.get("rom"))