"""Silence explicite et traçable."""

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class Silence:
    """Absence volontaire d'expression."""

    acte_parent: str = "ACTE_IV"
    reason: str
    created_at: datetime
    metadata: Mapping[str, str]
