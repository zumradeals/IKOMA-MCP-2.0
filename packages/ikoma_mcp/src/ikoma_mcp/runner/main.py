"""Runner runtime entrypoint."""

from __future__ import annotations

import logging
import os
import signal
import time
from pathlib import Path


DEFAULT_INTERVAL_SECONDS = 10
DEFAULT_CYCLE_FILE = Path("/var/lib/ikoma/runner_last_cycle_id")


def _read_last_cycle_id(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return int(path.read_text(encoding="utf-8").strip() or 0)
    except ValueError:
        return 0


def _write_cycle_id(path: Path, cycle_id: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(str(cycle_id), encoding="utf-8")
    tmp_path.replace(path)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [runner] %(message)s")
    interval = int(os.getenv("IKOMA_RUNNER_INTERVAL", str(DEFAULT_INTERVAL_SECONDS)))
    cycle_path = Path(os.getenv("IKOMA_RUNNER_CYCLE_FILE", str(DEFAULT_CYCLE_FILE)))

    stop = False

    def _handle_stop(signum: int, frame: object) -> None:
        nonlocal stop
        logging.info("Stopping runner (signal=%s)", signum)
        stop = True

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    cycle_id = _read_last_cycle_id(cycle_path)
    logging.info("Runner started with cycle_id=%s", cycle_id)

    while not stop:
        cycle_id += 1
        _write_cycle_id(cycle_path, cycle_id)
        logging.info("Runner cycle completed: %s", cycle_id)
        time.sleep(interval)

    logging.info("Runner stopped")


if __name__ == "__main__":
    main()
