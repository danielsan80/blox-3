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

    def _leftMap(self) -> dict[VertexPos, VertexPos]:
        return {
            VertexPos.A: VertexPos.B,
            VertexPos.B: VertexPos.C,
            VertexPos.C: VertexPos.A,
        }

    def _rightMap(self) -> dict[VertexPos, VertexPos]:
        return {
            VertexPos.A: VertexPos.C,
            VertexPos.B: VertexPos.A,
            VertexPos.C: VertexPos.B,
        }

    def get(self, vertexPos: VertexPos) -> Point:
        return self._map()[vertexPos]

    def left(self, vertexPos: VertexPos) -> Point:
        leftVertexPos = self._leftMap()[vertexPos]
        return self.get(leftVertexPos)

    def right(self, vertexPos: VertexPos) -> Point:
        rightVertexPos = self._rightMap()[vertexPos]
        return self.get(rightVertexPos)
