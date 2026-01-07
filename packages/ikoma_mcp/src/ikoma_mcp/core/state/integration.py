"""États des intégrations externes."""

from enum import Enum


class IntegrationState(str, Enum):
    """États fondamentaux des intégrations externes."""

    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    UNSTABLE = "UNSTABLE"
    UNKNOWN = "UNKNOWN"
