"""États du runtime passif (BUILD-5)."""

from enum import Enum


class RuntimeState(str, Enum):
    """États contractuels du runtime passif."""

    INIT = "INIT"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    STOPPED = "STOPPED"
