"""Capteur read-only de fichiers et artefacts."""

import hashlib
from pathlib import Path
from typing import Mapping

from ..core.evidence.primary import EvidencePrimary
from ..core.evidence.secondary import EvidenceSecondary
from ..core.types.fact import Fact
from .models import Observation
from .tracing import build_trace


def _checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def observe_file(path: str, with_checksum: bool = False) -> Observation:
    """Observe la présence d'un fichier et un checksum optionnel."""

    file_path = Path(path)
    exists = file_path.exists()
    status = "present" if exists else "absent"
    attributes: Mapping[str, str] = {
        "path": str(file_path),
        "status": status,
    }

    facts = [Fact(description="file.status", attributes=attributes)]
    primary = [EvidencePrimary(description=f"file {file_path} {status}")]
    secondary: list[EvidenceSecondary] = []

    if exists and with_checksum:
        checksum = _checksum(file_path)
        facts.append(
            Fact(
                description="file.checksum",
                attributes={"path": str(file_path), "sha256": checksum},
            )
        )
        secondary.append(
            EvidenceSecondary(description=f"checksum sha256 {file_path}")
        )

    trace = build_trace(
        actor="observability.files",
        metadata={"path": str(file_path), "status": status},
    )

    return Observation(
        facts=facts,
        primary_evidence=primary,
        secondary_evidence=secondary,
        traces=[trace],
    )
