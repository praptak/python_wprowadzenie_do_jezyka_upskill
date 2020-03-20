from dataclasses import dataclass
from typing import List

from lottery.participants import Participant


@dataclass(frozen=True, eq=True, repr=False, order=True)
class Prize:
    prize_id: int
    name: str
    amount: int


@dataclass(frozen=True, eq=True, repr=False, order=True)
class Prizes:
    name: str
    prizes: List[Prize]


@dataclass(frozen=False, eq=True, repr=False, order=True)
class Winner:
    participant: Participant
    prize: Prize
