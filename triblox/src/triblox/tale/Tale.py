import sys
sys.path.append('src/')

from math import sin
from triblox.config import side
from triblox.point.Point import Point
from triblox.tale.Direction import Direction
from triblox.tale.Vertices import Vertices
from triblox.tale.Coord import Coord
from triblox.helper.util import sin60

from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Tale:
    x: int
    y: int

    def __post_init__(self):
        self.coord

    @property
    def coord(self) -> Coord:
        return Coord(self.x, self.y)

    @property
    def direction(self) -> Direction:
        if (self.x + self.y) % 2 == 0:
            return Direction.up()
        else:
            return Direction.down()

    @property
    def vertices(self) -> Vertices:
        if self.direction.isUp():
            a = Point(self.x / 2 * side, self.y * sin60 * side)
            b = Point(a.x + side, a.y)
            c = Point(a.x + side / 2, (self.y + 1) * sin60 * side)

        elif self.direction.isDown():
            a = Point((0.5 + (self.x + 1) / 2) * side, (self.y + 1) * sin60 * side)
            b = Point(a.x - side, a.y)
            c = Point(a.x - side / 2, self.y * sin60 * side)
        else:
            raise ValueError("This should never happen")

        return Vertices(a, b, c)

    @property
    def incenter(self) -> Point:
        vertices = self.vertices
        return Point(
            (vertices.a.x + vertices.b.x + vertices.c.x) / 3,
            (vertices.a.y + vertices.b.y + vertices.c.y) / 3
        )

