"""Deployer runtime entrypoint."""

from __future__ import annotations

import logging
import os
import signal
import time


DEFAULT_INTERVAL_SECONDS = 15


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [deployer] %(message)s")
    interval = int(os.getenv("IKOMA_DEPLOYER_INTERVAL", str(DEFAULT_INTERVAL_SECONDS)))

    stop = False

    def _handle_stop(signum: int, frame: object) -> None:
        nonlocal stop
        logging.info("Stopping deployer (signal=%s)", signum)
        stop = True

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    logging.info("Deployer started")
    while not stop:
        logging.info("Deployer heartbeat")
        time.sleep(interval)

    logging.info("Deployer stopped")


if __name__ == "__main__":
    main()
