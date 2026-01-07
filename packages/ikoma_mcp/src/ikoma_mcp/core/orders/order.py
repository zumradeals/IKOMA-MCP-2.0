"""Ordre consommable après exécution."""

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class Order:
    """Expression explicite d'une volonté d'action."""

    acte_parent: str = "ACTE_IV"
    identifier: str
    scope: str
    created_at: datetime
    consumed_at: datetime | None
    metadata: Mapping[str, str]
