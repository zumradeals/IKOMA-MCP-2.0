"""Refus terminal et traçable."""

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class Refusal:
    """Décision explicite de ne pas agir."""

    acte_parent: str = "ACTE_IV"
    reason: str
    created_at: datetime
    metadata: Mapping[str, str]
