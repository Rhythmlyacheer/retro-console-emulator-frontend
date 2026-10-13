"""Entry point: boot the frontend, wire the pipeline, hand control to Qt."""
from __future__ import annotations

import logging
import sys

from retro_frontend.app import FrontendApp
from retro_frontend.config.loader import load_config


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main(argv: list[str] | None = None) -> int:
    _configure_logging()
    cfg = load_config()
    app = FrontendApp(cfg)
    return app.run(argv if argv is not None else sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())