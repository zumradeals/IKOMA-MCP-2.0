"""Traçabilité read-only des observations."""

from datetime import datetime, timezone
from typing import Mapping

from ..core.types.trace import Trace


def build_trace(actor: str, metadata: Mapping[str, str]) -> Trace:
    """Construit une trace horodatée sans interprétation."""

    return Trace(timestamp=datetime.now(timezone.utc), actor=actor, metadata=metadata)
