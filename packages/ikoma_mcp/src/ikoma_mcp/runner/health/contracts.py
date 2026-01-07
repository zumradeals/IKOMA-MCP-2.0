"""Contrats de health (BUILD-4)."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Sequence

from ...core.evidence.primary import EvidencePrimary
from ...core.evidence.secondary import EvidenceSecondary
from ...core.types.fact import Fact
from ...core.types.trace import Trace


class HealthObservation(str, Enum):
    """Observation d'état non confirmante."""

    OBSERVED = "observed"
    UNOBSERVED = "unobserved"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class HealthReport:
    """Rapport read-only de health."""

    facts: Sequence[Fact]
    primary_evidence: Sequence[EvidencePrimary]
    secondary_evidence: Sequence[EvidenceSecondary]
    traces: Sequence[Trace]
    observation: HealthObservation
    created_at: datetime


@dataclass(frozen=True)
class HealthProbe:
    """Contrat read-only de health."""

    name: str
    report: HealthReport
    created_at: datetime
    acte_parent: str = "ACTE_III"


def build_health_report(
    *,
    facts: Sequence[Fact],
    primary_evidence: Sequence[EvidencePrimary],
    secondary_evidence: Sequence[EvidenceSecondary],
    traces: Sequence[Trace],
    observation: HealthObservation,
    created_at: datetime,
) -> HealthReport:
    """Produit un rapport contractuel read-only, sans logique métier."""

    return HealthReport(
        facts=facts,
        primary_evidence=primary_evidence,
        secondary_evidence=secondary_evidence,
        traces=traces,
        observation=observation,
        created_at=created_at,
    )
