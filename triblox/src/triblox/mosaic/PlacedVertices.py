import sys

sys.path.append("src/")

from dataclasses import dataclass
from typing import Tuple

from triblox.geometry.Point import Point
from triblox.vertex.Vertex import Vertex


@dataclass(frozen=True)
class PlacedVertices:
    a: Vertex
    b: Vertex
    c: Vertex

    def offset_points(self, value: float) -> Tuple[Point]:
        points = []
        points += self.a.offset_points(value)
        points += self.b.offset_points(value)
        points += self.c.offset_points(value)

        return points

    def original_points(self) -> Tuple[Point]:
        points = []
        points += self.a.original_points()
        points += self.b.original_points()
        points += self.c.original_points()

        return points

    def centered_points(self, value: float) -> Tuple[Point]:
        points = []
        points += self.a.centered_points(value)
        points += self.b.centered_points(value)
        points += self.c.centered_points(value)

        return points
