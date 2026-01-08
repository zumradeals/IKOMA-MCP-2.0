"""Cycle pur du Runner Runtime (BUILD-6)."""

from datetime import datetime
from typing import List

from ...core.orders.order import Order
from ...core.orders.refusal import Refusal
from ...core.orders.silence import Silence
from ...core.state.transitions import ALLOWED_ENGINE_TRANSITIONS
from ...core.types.trace import Trace
from ..preflight.contracts import ActeIVExpression, PreflightStatus
from .contracts import RunnerRuntimeInput, RunnerRuntimeReport
from .decision import RunnerDecision, RunnerDecisionReason


def build_runner_cycle(*, runtime_input: RunnerRuntimeInput, created_at: datetime) -> RunnerRuntimeReport:
    """Produit un report complet pour un cycle, sans effet de bord."""

    reasons: List[RunnerDecisionReason] = []
    expression_kind = ActeIVExpression.SILENCE

    if not runtime_input.authority_check.has_authority(runtime_input.authority_level):
        reasons.append(RunnerDecisionReason.OUT_OF_AUTHORITY)
        expression_kind = ActeIVExpression.REFUS

    if not runtime_input.evidence or _preflight_insufficient(runtime_input):
        reasons.append(RunnerDecisionReason.INSUFFICIENT_PRIMARY_EVIDENCE)
        expression_kind = runtime_input.insufficient_evidence_expression

    if runtime_input.engine_transition:
        if runtime_input.engine_transition not in ALLOWED_ENGINE_TRANSITIONS:
            reasons.append(RunnerDecisionReason.CRITICAL_DIVERGENCE)
            expression_kind = ActeIVExpression.REFUS
        else:
            reasons.append(RunnerDecisionReason.TRANSITION_ALLOWED)

    if not reasons:
        reasons.append(RunnerDecisionReason.OBSERVED)

    if RunnerDecisionReason.OUT_OF_AUTHORITY in reasons:
        expression_kind = ActeIVExpression.REFUS

    if RunnerDecisionReason.CRITICAL_DIVERGENCE in reasons:
        expression_kind = ActeIVExpression.REFUS

    expression = _build_expression(runtime_input, expression_kind, created_at, reasons)

    decision = RunnerDecision(
        summary=f"expression={expression_kind.value}",
        reasons=reasons,
    )

    traces = list(runtime_input.context.traces)
    traces.append(
        Trace(
            timestamp=created_at,
            actor="runner",
            metadata={
                "acte_parent": "ACTE_IV",
                "expression": expression_kind.value,
                "reasons": ",".join(reason.value for reason in reasons),
            },
        )
    )

    return RunnerRuntimeReport(
        context=runtime_input.context,
        decision=decision,
        expression=expression,
        traces=traces,
        preflight_reports=runtime_input.preflight_reports,
        health_reports=runtime_input.health_reports,
        created_at=created_at,
    )


def _preflight_insufficient(runtime_input: RunnerRuntimeInput) -> bool:
    return any(
        report.status == PreflightStatus.INSUFFICIENT_EVIDENCE
        for report in runtime_input.preflight_reports
    )


def _build_expression(
    runtime_input: RunnerRuntimeInput,
    expression_kind: ActeIVExpression,
    created_at: datetime,
    reasons: List[RunnerDecisionReason],
):
    reason_text = ", ".join(reason.value for reason in reasons)
    if expression_kind == ActeIVExpression.ORDER:
        return Order(
            identifier=runtime_input.order_identifier,
            scope=runtime_input.order_scope,
            created_at=created_at,
            metadata={"reason": reason_text},
        )
    if expression_kind == ActeIVExpression.REFUS:
        return Refusal(
            reason=reason_text,
            created_at=created_at,
            metadata={"reason": reason_text},
        )
    return Silence(
        reason=reason_text,
        created_at=created_at,
        metadata={"reason": reason_text},
    )
