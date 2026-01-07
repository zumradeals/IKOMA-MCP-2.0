"""États d'un déploiement."""

from enum import Enum


class DeployState(str, Enum):
    """États fondamentaux d'un déploiement."""

    APPLIED = "APPLIED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
