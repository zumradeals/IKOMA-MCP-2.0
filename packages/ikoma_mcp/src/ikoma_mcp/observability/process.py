"""Capteur read-only de processus (PID)."""

from pathlib import Path
from typing import Mapping

from ..core.evidence.primary import EvidencePrimary
from ..core.types.fact import Fact
from .models import Observation
from .tracing import build_trace


def _read_process_state(pid: int) -> str | None:
    stat_path = Path(f"/proc/{pid}/stat")
    if not stat_path.exists():
        return None
    content = stat_path.read_text(encoding="utf-8").strip()
    parts = content.split()
    if len(parts) < 3:
        return None
    return parts[2]


def observe_pid(pid: int) -> Observation:
    """Observe la présence/absence d'un PID en lecture seule."""

    proc_path = Path(f"/proc/{pid}")
    state = _read_process_state(pid)
    status = "present" if proc_path.exists() else "absent"
    attributes: Mapping[str, str] = {
        "pid": str(pid),
        "status": status,
        "state": state or "unknown",
    }
    fact = Fact(description="process.status", attributes=attributes)
    evidence = EvidencePrimary(description=f"process {pid} {status}")
    trace = build_trace(
        actor="observability.process",
        metadata={"pid": str(pid), "status": status},
    )
    return Observation(
        facts=[fact],
        primary_evidence=[evidence],
        secondary_evidence=[],
        traces=[trace],
    )
