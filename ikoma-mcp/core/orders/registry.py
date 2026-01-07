"""Registre déclaratif des expressions d'autorité."""

from dataclasses import dataclass
from typing import Sequence, Union

from .order import Order
from .refusal import Refusal
from .silence import Silence

AuthorityExpression = Union[Order, Refusal, Silence]


@dataclass(frozen=True)
class OrderRegistry:
    """Registre sans exécution, purement déclaratif."""

    expressions: Sequence[AuthorityExpression]
