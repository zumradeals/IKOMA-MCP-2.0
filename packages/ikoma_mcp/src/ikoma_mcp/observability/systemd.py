"""Capteur read-only d'état systemd (lecture de runtime)."""

from pathlib import Path
from typing import Mapping

from ..core.evidence.secondary import EvidenceSecondary
from ..core.types.fact import Fact
from .models import Observation
from .tracing import build_trace


def observe_unit(unit_name: str) -> Observation:
    """Observe un unit systemd via son état en runtime (présence de fichier)."""

    runtime_path = Path("/run/systemd/system") / unit_name
    status = "loaded" if runtime_path.exists() else "absent"
    attributes: Mapping[str, str] = {
        "unit": unit_name,
        "status": status,
    }
    fact = Fact(description="systemd.unit", attributes=attributes)
    evidence = EvidenceSecondary(description=f"systemd unit {unit_name} {status}")
    trace = build_trace(
        actor="observability.systemd",
        metadata={"unit": unit_name, "status": status},
    )

    return Observation(
        facts=[fact],
        primary_evidence=[],
        secondary_evidence=[evidence],
        traces=[trace],
    )
