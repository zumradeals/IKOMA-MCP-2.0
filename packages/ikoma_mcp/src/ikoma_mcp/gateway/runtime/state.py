"""États d'exposition du Gateway Runtime (BUILD-8)."""

from enum import Enum


class GatewayExposureState(str, Enum):
    """États d'exposition déclaratifs, sans exécution réseau."""

    OPEN = "OPEN"
    CLOSED = "CLOSED"
    UNKNOWN = "UNKNOWN"
