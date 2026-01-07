"""Composition d'évidences sans score."""

from dataclasses import dataclass
from typing import Sequence

from .primary import EvidencePrimary
from .secondary import EvidenceSecondary


@dataclass(frozen=True)
class EvidenceSet:
    """Ensemble d'évidences (primaire + secondaires)."""

    primary: EvidencePrimary
    secondary: Sequence[EvidenceSecondary]
