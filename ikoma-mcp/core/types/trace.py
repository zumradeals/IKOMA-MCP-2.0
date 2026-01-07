"""Trace: empreinte irréversible d'un acte."""

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


@dataclass(frozen=True)
class Trace:
    """Trace horodatée sans interprétation."""

    timestamp: datetime
    actor: str
    metadata: Mapping[str, str]
