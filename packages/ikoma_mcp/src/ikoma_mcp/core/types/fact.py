"""Fait: observation vérifiable et non interprétée."""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Fact:
    """Fait observable, sans interprétation ni intention."""

    description: str
    attributes: Mapping[str, str]
