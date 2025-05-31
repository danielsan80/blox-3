import sys

sys.path.append("src/")

from dataclasses import dataclass
from typing import Tuple

from triblox.config import fix
from triblox.geometry.Point import Point
from triblox.vertex.Vertex import Vertex


@dataclass(frozen=True)
class PlacedVertices:
    a: Vertex
    b: Vertex
    c: Vertex

    def to_list(self) -> list[Vertex]:
        return [self.a, self.b, self.c]

    def offset_points(self, value: float, to6: bool = False) -> Tuple[Point]:
        if to6:
            return self._offset_points_to6(value)

        points = []
        points += self.a.offset_points(value)
        points += self.b.offset_points(value)
        points += self.c.offset_points(value)

        return tuple(points)

    def original_points(self, to6: bool = False) -> Tuple[Point]:
        if to6:
            return self._original_points_to6()
        points = []
        points += self.a.original_points()
        points += self.b.original_points()
        points += self.c.original_points()

        return tuple(points)

    def centered_points(self, value: float, to6: bool = False) -> Tuple[Point]:
        if to6:
            return self._centered_points_to6(value)
        points = []
        points += self.a.centered_points(value)
        points += self.b.centered_points(value)
        points += self.c.centered_points(value)

        return tuple(points)

    def _offset_points_to6(self, value: float) -> Tuple[Point]:
        all_points = []
        vertices = self.to_list()

        for i in range(3):
            vertex = vertices[i]
            points = vertex.offset_points(value)
            if len(points) == 1:
                next_vertex = vertices[(i + 1) % 3]
                next_point = next_vertex.offset_points(value)[0]
                points += [points[0].move(next_point, fix)]

            all_points += points

        return tuple(all_points)

    def _original_points_to6(self) -> Tuple[Point]:
        all_points = []
        vertices = self.to_list()

        for i in range(3):
            vertex = vertices[i]
            points = vertex.original_points()
            if len(points) == 1:
                next_vertex = vertices[(i + 1) % 3]
                next_point = next_vertex.original_points()[0]
                points += [points[0].move(next_point, fix)]

            all_points += points

        return tuple(all_points)

    def _centered_points_to6(self, value: float) -> Tuple[Point]:
        all_points = []
        vertices = self.to_list()

        for i in range(3):
            vertex = vertices[i]
            points = vertex.centered_points(value)
            if len(points) == 1:
                next_vertex = vertices[(i + 1) % 3]
                next_point = next_vertex.centered_points(value)[0]
                points += [points[0].move(next_point, fix)]

            all_points += points

        return tuple(all_points)
