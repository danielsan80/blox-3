import sys

sys.path.append("src/")

from dataclasses import dataclass, field
from typing import Dict, Tuple

from triblox.helper.util import sin60
from triblox.mosaic.VertexHex import VertexHex
from triblox.mosaic.VertexHexKey import VertexHexKey
from triblox.mosaic.VertexOffset import VertexOffset
from triblox.mosaic.VertexPos import VertexPos
from triblox.point.Point import Point
from triblox.tile.Tile import Tile


@dataclass(frozen=True)
class Vertex:
    tile: Tile
    pos: VertexPos
    hex: VertexHex = field(init=False)
    _placedMap: Dict[VertexHexKey, bool] = field(init=False)

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

        object.__setattr__(self, "_placedMap", placedMap)

    def markPlaced(self, key: VertexHexKey):
        placedMap = self._placedMap.copy()
        placedMap[key] = True

        obj = Vertex(self.tile, self.pos)
        object.__setattr__(obj, "_placedMap", placedMap)
        return obj

    def isMainPlaced(self) -> bool:
        return self._placedMap[VertexHexKey.MAIN]

    def isLeftNearPlaced(self) -> bool:
        return self._placedMap[VertexHexKey.LEFT_NEAR]

    def isLeftFarPlaced(self) -> bool:
        return self._placedMap[VertexHexKey.LEFT_FAR]

    def isRightNearPlaced(self) -> bool:
        return self._placedMap[VertexHexKey.RIGHT_NEAR]

    def isRightFarPlaced(self) -> bool:
        return self._placedMap[VertexHexKey.RIGHT_FAR]

    def isOppositePlaced(self) -> bool:
        return self._placedMap[VertexHexKey.OPPOSITE]

    def isAllPlaced(self) -> bool:
        return all(self._placedMap.values())

    def offset(self) -> VertexOffset:
        if not self.isLeftNearPlaced() and not self.isRightNearPlaced():
            return VertexOffset.CENTER
        if self.isLeftNearPlaced() and not self.isRightNearPlaced():
            return VertexOffset.LEFT
        if not self.isLeftNearPlaced() and self.isRightNearPlaced():
            return VertexOffset.RIGHT
        if self.isAllPlaced():
            return VertexOffset.NONE
        return VertexOffset.SPLIT

    def point(self) -> Point:
        return self.tile.vertices.get(self.pos)

    def movedPoints(self, value: float) -> Tuple[Point]:
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
            destination1 = self.tile.vertices.left(self.pos)
            destination2 = self.tile.vertices.right(self.pos)
            return [
                point.move(destination1, value / sin60),
                point.move(destination2, value / sin60),
            ]
        if self.offset() == VertexOffset.NONE:
            return [point]
