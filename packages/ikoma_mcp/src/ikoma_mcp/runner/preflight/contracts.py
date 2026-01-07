"""Contrats de preflight (BUILD-4)."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping, Sequence, Tuple

from ...core.evidence.primary import EvidencePrimary
from ...core.evidence.secondary import EvidenceSecondary
from ...core.types.fact import Fact
from ...core.types.trace import Trace


class PreflightStatus(str, Enum):
    """Statuts contractuels du rapport de preflight."""

    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    INCOHERENT_EVIDENCE = "incoherent_evidence"
    CONDITIONS_SATISFIED = "conditions_satisfied"
    CONDITIONS_UNSATISFIED = "conditions_unsatisfied"


class ActeIVExpression(str, Enum):
    """Expressions possibles selon ACTE IV (contrat uniquement)."""

    ORDER = "order"
    REFUS = "refus"
    SILENCE = "silence"


@dataclass(frozen=True)
class PreflightContext:
    """Contexte d'entrée read-only."""

    facts: Sequence[Fact]
    primary_evidence: Sequence[EvidencePrimary]
    secondary_evidence: Sequence[EvidenceSecondary]
    traces: Sequence[Trace]


@dataclass(frozen=True)
class PreflightReport:
    """Rapport read-only de preflight."""

    facts: Sequence[Fact]
    primary_evidence: Sequence[EvidencePrimary]
    secondary_evidence: Sequence[EvidenceSecondary]
    traces: Sequence[Trace]
    status: PreflightStatus
    blocking: bool
    created_at: datetime


@dataclass(frozen=True)
class PreflightCheck:
    """Contrat read-only de preflight."""

    name: str
    context: PreflightContext
    report: PreflightReport
    created_at: datetime
    acte_parent: str = "ACTE_IV"


@dataclass(frozen=True)
class ReportActeIVMapping:
    """Contrat de mapping ACTE IV sans arbitrage autonome."""

    status: PreflightStatus
    allowed_expressions: Tuple[ActeIVExpression, ...]
    default_expression: ActeIVExpression | None
    note: str


PREFLIGHT_ACTE_IV_MAPPING: Mapping[PreflightStatus, ReportActeIVMapping] = {
    PreflightStatus.INSUFFICIENT_EVIDENCE: ReportActeIVMapping(
        status=PreflightStatus.INSUFFICIENT_EVIDENCE,
        allowed_expressions=(ActeIVExpression.REFUS, ActeIVExpression.SILENCE),
        default_expression=None,
        note="Rapport bloquant: preuve manquante, aucun ordre émis par défaut.",
    ),
    PreflightStatus.INCOHERENT_EVIDENCE: ReportActeIVMapping(
        status=PreflightStatus.INCOHERENT_EVIDENCE,
        allowed_expressions=(ActeIVExpression.REFUS,),
        default_expression=None,
        note="Preuve incohérente: aucun ordre émis par défaut.",
    ),
    PreflightStatus.CONDITIONS_UNSATISFIED: ReportActeIVMapping(
        status=PreflightStatus.CONDITIONS_UNSATISFIED,
        allowed_expressions=(ActeIVExpression.REFUS,),
        default_expression=None,
        note="Conditions non satisfaites: aucun ordre émis par défaut.",
    ),
    PreflightStatus.CONDITIONS_SATISFIED: ReportActeIVMapping(
        status=PreflightStatus.CONDITIONS_SATISFIED,
        allowed_expressions=(ActeIVExpression.ORDER, ActeIVExpression.SILENCE),
        default_expression=None,
        note="Conditions satisfaites: aucune émission par défaut.",
    ),
}


def build_preflight_report(
    *,
    facts: Sequence[Fact],
    primary_evidence: Sequence[EvidencePrimary],
    secondary_evidence: Sequence[EvidenceSecondary],
    traces: Sequence[Trace],
    status: PreflightStatus,
    blocking: bool,
    created_at: datetime,
) -> PreflightReport:
    """Produit un rapport contractuel read-only, sans logique métier."""

    return PreflightReport(
        facts=facts,
        primary_evidence=primary_evidence,
        secondary_evidence=secondary_evidence,
        traces=traces,
        status=status,
        blocking=blocking,
        created_at=created_at,
    )
