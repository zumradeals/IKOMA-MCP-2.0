"""Rapport contractuel du runtime passif (BUILD-5)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from ..core.orders.registry import AuthorityExpression
from ..core.types.trace import Trace
from ..runner.health.contracts import HealthReport
from ..runner.preflight.contracts import PreflightReport
from .context import RuntimeContext


@dataclass(frozen=True)
class RuntimeReport:
    """Rapport read-only du runtime passif."""

    context: RuntimeContext
    preflight_reports: Sequence[PreflightReport]
    health_reports: Sequence[HealthReport]
    expression: AuthorityExpression
    traces: Sequence[Trace]
    created_at: datetime
    acte_parent: str = "ACTE_IV"


def build_runtime_report(
    *,
    context: RuntimeContext,
    preflight_reports: Sequence[PreflightReport],
    health_reports: Sequence[HealthReport],
    expression: AuthorityExpression,
    traces: Sequence[Trace],
    created_at: datetime,
    acte_parent: str = "ACTE_IV",
) -> RuntimeReport:
    """Construit un rapport runtime read-only, sans logique métier."""

    return RuntimeReport(
        context=context,
        preflight_reports=preflight_reports,
        health_reports=health_reports,
        expression=expression,
        traces=traces,
        created_at=created_at,
        acte_parent=acte_parent,
    )
