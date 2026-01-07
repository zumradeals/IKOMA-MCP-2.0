"""États du moteur (MCP)."""

from enum import Enum


class EngineState(str, Enum):
    """États fondamentaux du moteur."""

    UP = "UP"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
