"""Contrats d'exposition read-only du Gateway."""

from dataclasses import dataclass
from typing import Sequence

from ..core.evidence.primary import EvidencePrimary
from ..core.evidence.secondary import EvidenceSecondary
from ..core.state.integration import IntegrationState


@dataclass(frozen=True)
class GatewaySnapshot:
    """Snapshot d'exposition strictement read-only."""

    target: str
    state: IntegrationState
    primary: EvidencePrimary | None
    secondary: Sequence[EvidenceSecondary]


@dataclass(frozen=True)
class GatewayExposure:
    """Surface d'exposition read-only, sans action ni ouverture réseau."""

    snapshots: Sequence[GatewaySnapshot]
