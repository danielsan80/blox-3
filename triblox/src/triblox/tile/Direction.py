import sys

sys.path.append("src/")

from dataclasses import dataclass
from enum import Enum


class DirectionValue(Enum):
    UP = "up"
    DOWN = "down"


@dataclass(frozen=True)
class Direction:
    value: DirectionValue

    @classmethod
    def up(cls) -> "Direction":
        return cls(DirectionValue.UP)

    @classmethod
    def down(cls) -> "Direction":
        return cls(DirectionValue.DOWN)

    def is_up(self) -> bool:
        return self.value == DirectionValue.UP

    def is_down(self) -> bool:
        return self.value == DirectionValue.DOWN
