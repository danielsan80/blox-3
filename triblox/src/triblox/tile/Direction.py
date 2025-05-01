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

    def isUp(self) -> bool:
        return self.value == DirectionValue.UP

    def isDown(self) -> bool:
        return self.value == DirectionValue.DOWN
