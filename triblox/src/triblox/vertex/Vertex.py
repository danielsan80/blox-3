import sys

sys.path.append("src/")

from dataclasses import dataclass, field
from typing import Dict, Tuple

from triblox.helper.util import sin60
from triblox.point.Point import Point
from triblox.tile.Tile import Tile
from triblox.tile.VertexPos import VertexPos
from triblox.vertex.VertexHex import VertexHex
from triblox.vertex.VertexHexKey import VertexHexKey
from triblox.vertex.VertexOffset import VertexOffset


@dataclass(frozen=True)
class Vertex:
    tile: Tile
    pos: VertexPos
    hex: VertexHex = field(init=False)
    _placed_map: Dict[VertexHexKey, bool] = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "hex", VertexHex(self.tile, self.pos))

        placedMap = {
            VertexHexKey.MAIN: True,
            VertexHexKey.LEFT_NEAR: False,
            VertexHexKey.LEFT_FAR: False,
            VertexHexKey.OPPOSITE: False,
            VertexHexKey.RIGHT_FAR: False,
            VertexHexKey.RIGHT_NEAR: False,
        }

        object.__setattr__(self, "_placed_map", placedMap)

    def mark_placed(self, key: VertexHexKey):
        placedMap = self._placed_map.copy()
        placedMap[key] = True

        obj = Vertex(self.tile, self.pos)
        object.__setattr__(obj, "_placed_map", placedMap)
        return obj

    def is_main_placed(self) -> bool:
        return self._placed_map[VertexHexKey.MAIN]

    def is_left_near_placed(self) -> bool:
        return self._placed_map[VertexHexKey.LEFT_NEAR]

    def is_left_far_placed(self) -> bool:
        return self._placed_map[VertexHexKey.LEFT_FAR]

    def is_right_near_placed(self) -> bool:
        return self._placed_map[VertexHexKey.RIGHT_NEAR]

    def is_right_far_placed(self) -> bool:
        return self._placed_map[VertexHexKey.RIGHT_FAR]

    def is_opposite_placed(self) -> bool:
        return self._placed_map[VertexHexKey.OPPOSITE]

    def is_all_placed(self) -> bool:
        return all(self._placed_map.values())

    def offset(self) -> VertexOffset:
        if not self.is_left_near_placed() and not self.is_right_near_placed():
            return VertexOffset.CENTER
        if self.is_left_near_placed() and not self.is_right_near_placed():
            return VertexOffset.LEFT
        if not self.is_left_near_placed() and self.is_right_near_placed():
            return VertexOffset.RIGHT
        if self.is_all_placed():
            return VertexOffset.NONE
        return VertexOffset.SPLIT

    def point(self) -> Point:
        return self.tile.vertices.get(self.pos)

    def moved_points(self, value: float) -> Tuple[Point]:
        point = self.tile.vertices.get(self.pos)
        if self.offset() == VertexOffset.CENTER:
            destination = self.tile.incenter
            return [point.move(destination, value * 2)]
        if self.offset() == VertexOffset.LEFT:
            destination = self.tile.vertices.left(self.pos)
            return [point.move(destination, value / sin60)]
        if self.offset() == VertexOffset.RIGHT:
            destination = self.tile.vertices.right(self.pos)
            return [point.move(destination, value / sin60)]
        if self.offset() == VertexOffset.SPLIT:
            destination1 = self.tile.vertices.right(self.pos)
            destination2 = self.tile.vertices.left(self.pos)
            return [
                point.move(destination1, value / sin60),
                point.move(destination2, value / sin60),
            ]
        if self.offset() == VertexOffset.NONE:
            return [point]
