"""Refus terminal et traçable."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Optional


@dataclass(frozen=True)
class Refusal:
    """Décision explicite de ne pas agir."""

    acte_parent: str = "ACTE_IV"
    reason: str
    created_at: datetime
    metadata: Optional[Mapping[str, str]] = field(default_factory=dict)
