"""Configuration minimale du Deployer runtime (BUILD-6)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeployerConfig:
    """Configuration déclarative du Deployer."""

    acte_parent: str = "ACTE_IV"
    dry_run: bool = True
    exec_enabled: bool = False
