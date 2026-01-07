"""Observations read-only alignées sur les Actes II et III."""

from dataclasses import dataclass
from typing import Sequence

from ..core.evidence.primary import EvidencePrimary
from ..core.evidence.secondary import EvidenceSecondary
from ..core.types.fact import Fact
from ..core.types.trace import Trace


@dataclass(frozen=True)
class Observation:
    """Résultat d'observation read-only."""

    facts: Sequence[Fact]
    primary_evidence: Sequence[EvidencePrimary]
    secondary_evidence: Sequence[EvidenceSecondary]
    traces: Sequence[Trace]
