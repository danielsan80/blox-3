import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.tile.VertexPos import VertexPos
from triblox.point.Point import Point


@dataclass(frozen=True)
class Vertices:
    a: Point
    b: Point
    c: Point

    def _map(self) -> dict[VertexPos, Point]:
        return {VertexPos.A: self.a, VertexPos.B: self.b, VertexPos.C: self.c}

    def _left_map(self) -> dict[VertexPos, VertexPos]:
        return {
            VertexPos.A: VertexPos.B,
            VertexPos.B: VertexPos.C,
            VertexPos.C: VertexPos.A,
        }

    def _right_map(self) -> dict[VertexPos, VertexPos]:
        return {
            VertexPos.A: VertexPos.C,
            VertexPos.B: VertexPos.A,
            VertexPos.C: VertexPos.B,
        }

    def get(self, vertex_pos: VertexPos) -> Point:
        return self._map()[vertex_pos]

    def left(self, vertex_pos: VertexPos) -> Point:
        left_vertex_pos = self._left_map()[vertex_pos]
        return self.get(left_vertex_pos)

    def right(self, vertex_pos: VertexPos) -> Point:
        right_vertex_pos = self._right_map()[vertex_pos]
        return self.get(right_vertex_pos)
