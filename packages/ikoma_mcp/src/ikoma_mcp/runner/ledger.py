"""Ledger append-only (jsonlines) pour le Runner runtime."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Mapping, Optional, Sequence

from ..core.evidence.set import EvidenceSet
from ..core.orders.order import Order
from ..core.orders.refusal import Refusal
from ..core.orders.silence import Silence
from ..core.orders.registry import AuthorityExpression
from ..core.types.decision import Decision
from ..core.types.fact import Fact
from ..core.types.trace import Trace


@dataclass(frozen=True)
class LedgerEntry:
    """Entrée append-only du ledger runtime."""

    acte_parent: str
    created_at: datetime
    facts: Sequence[Fact]
    evidence: Sequence[EvidenceSet]
    decision: Decision
    traces: Sequence[Trace]
    expression: Optional[AuthorityExpression] = None

    def to_record(self) -> Mapping[str, object]:
        """Serialize l'entrée en dict JSON-safe."""

        return {
            "acte_parent": self.acte_parent,
            "created_at": self.created_at.isoformat(),
            "facts": [_serialize_fact(fact) for fact in self.facts],
            "evidence": [_serialize_evidence_set(item) for item in self.evidence],
            "decision": _serialize_decision(self.decision),
            "traces": [_serialize_trace(trace) for trace in self.traces],
            "expression": _serialize_expression(self.expression),
        }


class LedgerWriter:
    """Writer append-only pour ledger runtime."""

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def append(self, entry: LedgerEntry) -> None:
        """Append une entrée au format jsonlines."""

        record = entry.to_record()
        payload = json.dumps(record, ensure_ascii=False)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(payload + "\n")


def _serialize_fact(fact: Fact) -> Mapping[str, object]:
    return {"description": fact.description, "attributes": dict(fact.attributes)}


def _serialize_evidence_set(evidence: EvidenceSet) -> Mapping[str, object]:
    return {
        "primary": {"description": evidence.primary.description},
        "secondary": [{"description": item.description} for item in evidence.secondary],
    }


def _serialize_decision(decision: Decision) -> Mapping[str, object]:
    return {
        "summary": decision.summary,
        "facts": [_serialize_fact(fact) for fact in decision.facts],
    }


def _serialize_trace(trace: Trace) -> Mapping[str, object]:
    return {
        "timestamp": trace.timestamp.isoformat(),
        "actor": trace.actor,
        "metadata": dict(trace.metadata),
    }


def _serialize_expression(
    expression: Optional[AuthorityExpression],
) -> Optional[Mapping[str, object]]:
    if expression is None:
        return None
    if isinstance(expression, Order):
        return {
            "type": "order",
            "acte_parent": expression.acte_parent,
            "identifier": expression.identifier,
            "scope": expression.scope,
            "created_at": expression.created_at.isoformat(),
            "consumed_at": expression.consumed_at.isoformat() if expression.consumed_at else None,
            "metadata": dict(expression.metadata or {}),
        }
    if isinstance(expression, Refusal):
        return {
            "type": "refusal",
            "acte_parent": expression.acte_parent,
            "reason": expression.reason,
            "created_at": expression.created_at.isoformat(),
            "metadata": dict(expression.metadata or {}),
        }
    if isinstance(expression, Silence):
        return {
            "type": "silence",
            "acte_parent": expression.acte_parent,
            "reason": expression.reason,
            "created_at": expression.created_at.isoformat(),
            "metadata": dict(expression.metadata or {}),
        }
    raise TypeError(f"Unsupported expression type: {type(expression)!r}")
