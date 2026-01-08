"""Rapport d'exposition du Gateway Runtime (BUILD-8)."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping, Sequence

from ...core.orders.order import Order
from ...core.orders.refusal import Refusal
from ...core.orders.registry import AuthorityExpression
from ...core.orders.silence import Silence
from ...core.types.fact import Fact
from ...core.types.trace import Trace
from ...runner.preflight.contracts import ActeIVExpression
from .context import GatewayContext
from .request import GatewayRequest
from .state import GatewayExposureState


class GatewayReportStatus(str, Enum):
    """Statut contractuel d'exposition, sans interprétation."""

    CONFIRMED = "confirmed"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    INCOHERENT = "incoherent"


@dataclass(frozen=True)
class GatewayReport:
    """Rapport d'exposition passif, sans action réseau."""

    context: GatewayContext
    request: GatewayRequest
    status: GatewayReportStatus
    expression: AuthorityExpression
    facts: Sequence[Fact]
    traces: Sequence[Trace]
    created_at: datetime
    acte_parent: str = "ACTE_IV"


@dataclass(frozen=True)
class GatewayActeIVMapping:
    """Table explicite de mapping vers ACTE IV."""

    status: GatewayReportStatus
    allowed_expressions: tuple[ActeIVExpression, ...]
    default_expression: ActeIVExpression
    note: str


GATEWAY_ACTE_IV_MAPPING: Mapping[GatewayReportStatus, GatewayActeIVMapping] = {
    GatewayReportStatus.CONFIRMED: GatewayActeIVMapping(
        status=GatewayReportStatus.CONFIRMED,
        allowed_expressions=(ActeIVExpression.ORDER,),
        default_expression=ActeIVExpression.ORDER,
        note="Exposition confirmée + ordre valide ⇒ Order consommé.",
    ),
    GatewayReportStatus.INSUFFICIENT_EVIDENCE: GatewayActeIVMapping(
        status=GatewayReportStatus.INSUFFICIENT_EVIDENCE,
        allowed_expressions=(ActeIVExpression.SILENCE,),
        default_expression=ActeIVExpression.SILENCE,
        note="Preuve manquante ⇒ Silence.",
    ),
    GatewayReportStatus.INCOHERENT: GatewayActeIVMapping(
        status=GatewayReportStatus.INCOHERENT,
        allowed_expressions=(ActeIVExpression.REFUS,),
        default_expression=ActeIVExpression.REFUS,
        note="Incohérence / ordre invalide ⇒ Refus traçable.",
    ),
}


def build_gateway_report(*, request: GatewayRequest, created_at: datetime) -> GatewayReport:
    """Produit un rapport d'exposition purement déclaratif."""

    status = _derive_status(request)
    mapping = GATEWAY_ACTE_IV_MAPPING[status]
    expression = _build_expression(request, mapping.default_expression, created_at)

    facts = list(request.context.facts)
    facts.append(
        Fact(
            description="gateway.exposure.status",
            attributes={
                "target": request.context.target,
                "exposure_state": request.context.exposure_state.value,
                "status": status.value,
            },
        )
    )

    traces = list(request.context.traces)
    traces.append(
        Trace(
            timestamp=created_at,
            actor="gateway",
            metadata={
                "acte_parent": "ACTE_IV",
                "status": status.value,
                "expression": mapping.default_expression.value,
                "target": request.context.target,
            },
        )
    )

    return GatewayReport(
        context=request.context,
        request=request,
        status=status,
        expression=expression,
        facts=facts,
        traces=traces,
        created_at=created_at,
    )


def _derive_status(request: GatewayRequest) -> GatewayReportStatus:
    context = request.context
    if not context.proof_present:
        if context.exposure_state is GatewayExposureState.UNKNOWN:
            return GatewayReportStatus.INSUFFICIENT_EVIDENCE
        return GatewayReportStatus.INCOHERENT
    if request.order is None:
        return GatewayReportStatus.INCOHERENT
    if not request.order.identifier or not request.order.scope:
        return GatewayReportStatus.INCOHERENT
    if context.exposure_state is GatewayExposureState.UNKNOWN:
        return GatewayReportStatus.INSUFFICIENT_EVIDENCE
    return GatewayReportStatus.CONFIRMED


def _build_expression(
    request: GatewayRequest,
    expression_kind: ActeIVExpression,
    created_at: datetime,
) -> AuthorityExpression:
    if expression_kind is ActeIVExpression.ORDER:
        order = request.order
        if order is None:
            return Refusal(
                reason="ordre manquant",
                created_at=created_at,
                metadata={"reason": "ordre manquant"},
            )
        return Order(
            identifier=order.identifier,
            scope=order.scope,
            created_at=order.created_at,
            acte_parent=order.acte_parent,
            consumed_at=created_at,
            metadata=order.metadata,
        )
    if expression_kind is ActeIVExpression.REFUS:
        return Refusal(
            reason="ordre invalide ou incohérent",
            created_at=created_at,
            metadata={"reason": "ordre invalide ou incohérent"},
        )
    return Silence(
        reason="preuve manquante",
        created_at=created_at,
        metadata={"reason": "preuve manquante"},
    )
