"""Vues dérivées d'exposition, sans heuristique."""

from dataclasses import dataclass
from typing import Sequence

from ..core.evidence.primary import EvidencePrimary
from ..core.evidence.secondary import EvidenceSecondary
from ..core.state.integration import IntegrationState
from .exposure import GatewayExposure, GatewaySnapshot


@dataclass(frozen=True)
class GatewayView:
    """Vue dérivée d'un snapshot, conforme aux preuves primaires."""

    target: str
    state: IntegrationState
    primary: EvidencePrimary | None
    secondary: Sequence[EvidenceSecondary]


def derive_gateway_view(snapshot: GatewaySnapshot) -> GatewayView:
    """Produit une vue sans heuristique ni extrapolation."""

    state = snapshot.state if snapshot.primary is not None else IntegrationState.UNKNOWN
    return GatewayView(
        target=snapshot.target,
        state=state,
        primary=snapshot.primary,
        secondary=snapshot.secondary,
    )


def derive_gateway_views(exposure: GatewayExposure) -> Sequence[GatewayView]:
    """Dérive des vues pour tous les snapshots exposés."""

    return tuple(derive_gateway_view(snapshot) for snapshot in exposure.snapshots)
