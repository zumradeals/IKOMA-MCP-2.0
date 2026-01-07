"""Wiring strict Runner → Deployer → Ledger (BUILD-7)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional, Sequence

from ..core.orders.order import Order
from ..core.orders.refusal import Refusal
from ..core.orders.silence import Silence
from ..core.orders.registry import AuthorityExpression
from ..core.types.decision import Decision
from ..core.types.fact import Fact
from ..core.types.trace import Trace
from ..deployer.result import ApplyResult, DeployOutcome
from ..runner.emit import emit_refusal, emit_silence
from ..runner.ledger import LedgerEntry

ApplyCallable = Callable[[Order], ApplyResult]


def _now() -> datetime:
    return datetime.utcnow()


@dataclass(frozen=True)
class WiringResult:
    """Résultat de câblage pour un cycle Runner ↔ Deployer."""

    expression: AuthorityExpression
    apply_result: Optional[ApplyResult]
    ledger_entry: LedgerEntry


def _link_trace(
    acte_parent: str,
    event: str,
    timestamp: datetime,
    metadata: Optional[dict[str, str]] = None,
) -> Trace:
    trace_metadata = {"acte_parent": acte_parent, "event": event}
    if metadata:
        trace_metadata.update(metadata)
    return Trace(timestamp=timestamp, actor="link", metadata=trace_metadata)


def _link_fact(description: str, attributes: dict[str, str]) -> Fact:
    return Fact(description=description, attributes=attributes)


def _extract_errors(traces: Sequence[Trace]) -> Optional[str]:
    for trace in traces:
        errors = trace.metadata.get("errors")
        if errors:
            return errors
    return None


def _decision(summary: str, facts: Sequence[Fact]) -> Decision:
    return Decision(summary=summary, facts=facts)


def wire_step(
    order: Optional[Order],
    apply: ApplyCallable,
    acte_parent: str = "ACTE_IV",
) -> WiringResult:
    """Câblage minimal: ordre → apply_result → ledger."""

    timestamp = _now()
    if order is None:
        silence = emit_silence(reason="no_order", acte_parent=acte_parent)
        facts = [
            _link_fact(
                description="link.silence",
                attributes={"acte_parent": acte_parent, "reason": silence.reason},
            )
        ]
        traces = [_link_trace(acte_parent, "silence", timestamp)]
        entry = LedgerEntry(
            acte_parent=acte_parent,
            created_at=timestamp,
            facts=facts,
            evidence=[],
            decision=_decision("link.silence", facts),
            traces=traces,
            expression=silence,
        )
        return WiringResult(expression=silence, apply_result=None, ledger_entry=entry)

    acte_parent = order.acte_parent
    if order.consumed_at is not None:
        refusal = emit_refusal(
            reason="order_already_consumed",
            acte_parent=acte_parent,
            metadata={"order_id": order.identifier},
        )
        facts = [
            _link_fact(
                description="link.refusal",
                attributes={
                    "acte_parent": acte_parent,
                    "order_id": order.identifier,
                    "reason": refusal.reason,
                },
            )
        ]
        traces = [_link_trace(acte_parent, "refusal", timestamp)]
        entry = LedgerEntry(
            acte_parent=acte_parent,
            created_at=timestamp,
            facts=facts,
            evidence=[],
            decision=_decision("link.refusal", facts),
            traces=traces,
            expression=refusal,
        )
        return WiringResult(expression=refusal, apply_result=None, ledger_entry=entry)

    apply_result = apply(order)
    errors = _extract_errors(apply_result.traces)
    if apply_result.outcome is DeployOutcome.APPLIED:
        expression: AuthorityExpression = apply_result.order
        facts = list(apply_result.facts) + [
            _link_fact(
                description="link.applied",
                attributes={
                    "acte_parent": acte_parent,
                    "order_id": order.identifier,
                    "outcome": apply_result.outcome.value,
                },
            )
        ]
        traces = list(apply_result.traces) + [
            _link_trace(
                acte_parent,
                "result",
                timestamp,
                metadata={"order_id": order.identifier, "outcome": apply_result.outcome.value},
            )
        ]
        summary = "link.applied"
    else:
        refusal_reason = f"deployer_{apply_result.outcome.value.lower()}"
        if errors:
            refusal_reason = f"{refusal_reason}:{errors}"
        refusal = emit_refusal(
            reason=refusal_reason,
            acte_parent=acte_parent,
            metadata={
                "order_id": order.identifier,
                "outcome": apply_result.outcome.value,
                "errors": errors or "",
            },
        )
        expression = refusal
        facts = list(apply_result.facts) + [
            _link_fact(
                description="link.refusal",
                attributes={
                    "acte_parent": acte_parent,
                    "order_id": order.identifier,
                    "outcome": apply_result.outcome.value,
                    "errors": errors or "",
                },
            )
        ]
        traces = list(apply_result.traces) + [
            _link_trace(
                acte_parent,
                "refusal",
                timestamp,
                metadata={
                    "order_id": order.identifier,
                    "outcome": apply_result.outcome.value,
                    "errors": errors or "",
                },
            )
        ]
        summary = "link.refusal"

    entry = LedgerEntry(
        acte_parent=acte_parent,
        created_at=timestamp,
        facts=facts,
        evidence=[],
        decision=_decision(summary, facts),
        traces=traces,
        expression=expression,
    )
    return WiringResult(
        expression=expression,
        apply_result=apply_result,
        ledger_entry=entry,
    )
