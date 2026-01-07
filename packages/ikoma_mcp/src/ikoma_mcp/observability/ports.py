"""Capteur read-only d'écoute de ports locaux."""

from pathlib import Path
from typing import Iterable, Mapping

from ..core.evidence.primary import EvidencePrimary
from ..core.types.fact import Fact
from .models import Observation
from .tracing import build_trace

_LISTEN_STATE = "0A"


def _parse_proc_net_tcp(path: Path) -> set[int]:
    if not path.exists():
        return set()
    lines = path.read_text(encoding="utf-8").splitlines()
    listening_ports: set[int] = set()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 4:
            continue
        local_address = parts[1]
        state = parts[3]
        if state != _LISTEN_STATE:
            continue
        _, port_hex = local_address.split(":")
        try:
            port = int(port_hex, 16)
        except ValueError:
            continue
        listening_ports.add(port)
    return listening_ports


def _collect_listening_ports() -> set[int]:
    ports = set()
    ports.update(_parse_proc_net_tcp(Path("/proc/net/tcp")))
    ports.update(_parse_proc_net_tcp(Path("/proc/net/tcp6")))
    return ports


def observe_ports(ports: Iterable[int]) -> Observation:
    """Observe la présence d'écoute locale pour une liste de ports."""

    listening_ports = _collect_listening_ports()
    facts: list[Fact] = []
    evidence: list[EvidencePrimary] = []
    traces = []

    for port in ports:
        status = "listening" if port in listening_ports else "absent"
        attributes: Mapping[str, str] = {
            "port": str(port),
            "status": status,
        }
        facts.append(Fact(description="port.listen", attributes=attributes))
        evidence.append(EvidencePrimary(description=f"port {port} {status}"))
        traces.append(
            build_trace(
                actor="observability.ports",
                metadata={"port": str(port), "status": status},
            )
        )

    return Observation(
        facts=facts,
        primary_evidence=evidence,
        secondary_evidence=[],
        traces=traces,
    )
