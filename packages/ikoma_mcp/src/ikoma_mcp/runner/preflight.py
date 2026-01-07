"""Contrats de preflight basés sur les preuves BUILD-2B."""

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from ..core.evidence.primary import EvidencePrimary
from ..core.evidence.secondary import EvidenceSecondary
from ..core.types.trace import Trace


@dataclass(frozen=True)
class PreflightCheck:
    """Contrat read-only de preflight."""

    name: str
    primary_evidence: Sequence[EvidencePrimary]
    secondary_evidence: Sequence[EvidenceSecondary]
    traces: Sequence[Trace]
    created_at: datetime
    acte_parent: str = "ACTE_II"
