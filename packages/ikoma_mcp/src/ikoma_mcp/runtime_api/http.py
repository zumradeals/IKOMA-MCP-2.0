"""HTTP transport for the BUILD-9 runtime API."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Mapping
from urllib.parse import urlparse

from .provider import DefaultRuntimeApiProvider, RuntimeApiProvider
from .serialization import (
    serialize_deployer_last,
    serialize_gateway_exposure,
    serialize_runner_cycle,
    serialize_runtime_report,
)


class RuntimeApiHandler(BaseHTTPRequestHandler):
    """HTTP handler exposing read-only runtime reports."""

    provider: RuntimeApiProvider = DefaultRuntimeApiProvider()
    openapi_schema: Mapping[str, object] | None = None

    def do_GET(self) -> None:  # noqa: N802 - enforced by BaseHTTPRequestHandler
        path = urlparse(self.path).path
        if path == "/v1/runtime/status":
            payload = serialize_runtime_report(self.provider.get_runtime_status())
            self._send_json(payload)
            return
        if path == "/v1/runner/cycle":
            payload = serialize_runner_cycle(self.provider.get_runner_cycle())
            self._send_json(payload)
            return
        if path == "/v1/deployer/last":
            payload = serialize_deployer_last(self.provider.get_deployer_last())
            self._send_json(payload)
            return
        if path == "/v1/gateway/exposure":
            payload = serialize_gateway_exposure(self.provider.get_gateway_exposure())
            self._send_json(payload)
            return
        if path == "/v1/openapi.json" and self.openapi_schema is not None:
            self._send_json(self.openapi_schema)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return

    def _send_json(self, payload: Mapping[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def create_runtime_api_server(
    host: str,
    port: int,
    provider: RuntimeApiProvider | None = None,
    *,
    openapi_schema: Mapping[str, object] | None = None,
) -> HTTPServer:
    """Create a passive HTTP server exposing runtime reports."""

    provider_instance = provider or DefaultRuntimeApiProvider()

    class Handler(RuntimeApiHandler):
        pass

    Handler.provider = provider_instance
    Handler.openapi_schema = openapi_schema
    return HTTPServer((host, port), Handler)
