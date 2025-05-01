import sys

sys.path.append("src/")

from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __str__(self):
        return f"{self.x},{self.y}"
