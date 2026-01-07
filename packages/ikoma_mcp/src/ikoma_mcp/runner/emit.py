"""Émission déclarative (Order / Refusal / Silence)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Optional, Sequence

from ..core.orders.order import Order
from ..core.orders.refusal import Refusal
from ..core.orders.registry import AuthorityExpression, OrderRegistry
from ..core.orders.silence import Silence


def _now() -> datetime:
    return datetime.utcnow()


def emit_order(
    identifier: str,
    scope: str,
    metadata: Optional[Mapping[str, str]] = None,
    acte_parent: str = "ACTE_IV",
) -> Order:
    """Émet un ordre déclaratif sans exécution."""

    return Order(
        acte_parent=acte_parent,
        identifier=identifier,
        scope=scope,
        created_at=_now(),
        metadata=metadata or {},
    )


def emit_refusal(
    reason: str,
    metadata: Optional[Mapping[str, str]] = None,
    acte_parent: str = "ACTE_IV",
) -> Refusal:
    """Émet un refus déclaratif sans exécution."""

    return Refusal(
        acte_parent=acte_parent,
        reason=reason,
        created_at=_now(),
        metadata=metadata or {},
    )


def emit_silence(
    reason: str,
    metadata: Optional[Mapping[str, str]] = None,
    acte_parent: str = "ACTE_IV",
) -> Silence:
    """Émet un silence déclaratif sans exécution."""

    return Silence(
        acte_parent=acte_parent,
        reason=reason,
        created_at=_now(),
        metadata=metadata or {},
    )


@dataclass(frozen=True)
class EmittedRegistry:
    """Registre déclaratif d'émissions."""

    expressions: Sequence[AuthorityExpression]
    created_at: datetime = field(default_factory=_now)
    acte_parent: str = "ACTE_IV"

    def as_registry(self) -> OrderRegistry:
        """Convertion vers le registre d'ordres."""

        return OrderRegistry(
            acte_parent=self.acte_parent,
            expressions=self.expressions,
            created_at=self.created_at,
        )
