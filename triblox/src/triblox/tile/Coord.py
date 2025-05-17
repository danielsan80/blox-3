import sys

sys.path.append("src/")

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __str__(self):
        return f"{self.x},{self.y}"

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)
