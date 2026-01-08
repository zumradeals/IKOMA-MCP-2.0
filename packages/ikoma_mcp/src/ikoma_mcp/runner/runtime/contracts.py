"""Contrats du Runner Runtime (BUILD-6)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from ...core.authority.check import AuthorityCheck
from ...core.authority.levels import AuthorityLevel
from ...core.evidence.set import EvidenceSet
from ...core.orders.registry import AuthorityExpression
from ...core.state.engine import EngineState
from ...core.types.fact import Fact
from ...core.types.trace import Trace
from ...runtime.context import RuntimeContext
from ..health.contracts import HealthReport
from ..preflight.contracts import ActeIVExpression, PreflightReport
from .decision import RunnerDecision


@dataclass(frozen=True)
class RunnerRuntimeInput:
    """Entrée read-only du Runner Runtime."""

    facts: Sequence[Fact]
    evidence: Sequence[EvidenceSet]
    context: RuntimeContext
    preflight_reports: Sequence[PreflightReport]
    health_reports: Sequence[HealthReport]
    authority_check: AuthorityCheck
    authority_level: AuthorityLevel
    engine_transition: tuple[EngineState, EngineState] | None
    insufficient_evidence_expression: ActeIVExpression
    order_identifier: str
    order_scope: str


@dataclass(frozen=True)
class RunnerRuntimeReport:
    """Rapport read-only du Runner Runtime."""

    context: RuntimeContext
    decision: RunnerDecision
    expression: AuthorityExpression
    traces: Sequence[Trace]
    preflight_reports: Sequence[PreflightReport]
    health_reports: Sequence[HealthReport]
    created_at: datetime
    acte_parent: str = "ACTE_IV"
