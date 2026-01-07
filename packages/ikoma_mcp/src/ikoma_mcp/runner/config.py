"""Configuration déclarative du Runtime Runner (BUILD-5)."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class RuntimeConfig:
    """Configuration minimale du Runner runtime."""

    acte_parent: str = "ACTE_V"
    interval_seconds: float = 1.0
    ledger_path: Optional[Path] = None
