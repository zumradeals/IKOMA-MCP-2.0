"""Gateway runtime entrypoint (read-only API)."""

from __future__ import annotations

import logging
import os
import signal
from http.server import HTTPServer

from ..runtime_api.http import create_runtime_api_server
from ..runtime_api.provider import FileBasedRuntimeApiProvider


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9000


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [gateway] %(message)s")
    host = os.getenv("IKOMA_GATEWAY_HOST", DEFAULT_HOST)
    port = int(os.getenv("IKOMA_GATEWAY_PORT", str(DEFAULT_PORT)))

    provider = FileBasedRuntimeApiProvider()
    server = create_runtime_api_server(host, port, provider=provider)
    logging.info("Gateway API listening on http://%s:%s", host, port)

    def _handle_stop(signum: int, frame: object) -> None:
        logging.info("Stopping gateway (signal=%s)", signum)
        server.shutdown()

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    try:
        server.serve_forever()
    finally:
        server.server_close()
        logging.info("Gateway stopped")


if __name__ == "__main__":
    main()
