"""Ordre consommable après exécution."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping, Optional


@dataclass(frozen=True)
class Order:
    """Expression explicite d'une volonté d'action."""

    identifier: str
    scope: str
    created_at: datetime
    acte_parent: str = "ACTE_IV"
    consumed_at: Optional[datetime] = None
    metadata: Optional[Mapping[str, str]] = field(default_factory=dict)
