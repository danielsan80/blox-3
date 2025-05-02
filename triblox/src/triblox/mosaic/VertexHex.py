import sys

sys.path.append("src/")

from triblox.tile.Tile import Tile

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict
from triblox.tile.VertexPos import VertexPos


class VertexHexKey(Enum):
    MAIN = "main"
    LEFT_NEAR = "left_near"
    LEFT_FAR = "left_far"
    RIGHT_NEAR = "right_near"
    RIGHT_FAR = "right_far"
    OPPOSITE = "opposite"

@dataclass(frozen=True)
class VertexHex:
    tile: Tile
    refVertexPos: VertexPos
    _tiles: Dict[VertexHexKey, Tile] = field(init=False)

    def __post_init__(self):
        if self.refVertexPos == VertexPos.A:
            if self.tile.isUp():
                tiles = {
                    VertexHexKey.MAIN: self.tile,
                    VertexHexKey.LEFT_NEAR: self.tile.down(),
                    VertexHexKey.LEFT_FAR: self.tile.down().left(),
                    VertexHexKey.RIGHT_NEAR: self.tile.left(),
                    VertexHexKey.RIGHT_FAR: self.tile.left().left(),
                    VertexHexKey.OPPOSITE: self.tile.left().left().down()
                }
                object.__setattr__(self, "_tiles", tiles)
                return
            if self.tile.isDown():
                tiles = {
                    VertexHexKey.MAIN: self.tile,
                    VertexHexKey.LEFT_NEAR: self.tile.up(),
                    VertexHexKey.LEFT_FAR: self.tile.up().right(),
                    VertexHexKey.RIGHT_NEAR: self.tile.right(),
                    VertexHexKey.RIGHT_FAR: self.tile.right().right(),
                    VertexHexKey.OPPOSITE: self.tile.right().right().up()
                }
                object.__setattr__(self, "_tiles", tiles)
                return
        if self.refVertexPos == VertexPos.B:
            if self.tile.isUp():
                tiles = {
                    VertexHexKey.MAIN: self.tile,
                    VertexHexKey.LEFT_NEAR: self.tile.right(),
                    VertexHexKey.LEFT_FAR: self.tile.right().right(),
                    VertexHexKey.RIGHT_NEAR: self.tile.down(),
                    VertexHexKey.RIGHT_FAR: self.tile.down().right(),
                    VertexHexKey.OPPOSITE: self.tile.down().right().right()
                }
                object.__setattr__(self, "_tiles", tiles)
                return
            if self.tile.isDown():
                tiles = {
                    VertexHexKey.MAIN: self.tile,
                    VertexHexKey.LEFT_NEAR: self.tile.left(),
                    VertexHexKey.LEFT_FAR: self.tile.left().left(),
                    VertexHexKey.RIGHT_NEAR: self.tile.up(),
                    VertexHexKey.RIGHT_FAR: self.tile.up().left(),
                    VertexHexKey.OPPOSITE: self.tile.up().left().left()
                }
                object.__setattr__(self, "_tiles", tiles)
                return
        if self.refVertexPos == VertexPos.C:
            if self.tile.isUp():
                tiles = {
                    VertexHexKey.MAIN: self.tile,
                    VertexHexKey.LEFT_NEAR: self.tile.left(),
                    VertexHexKey.LEFT_FAR: self.tile.left().up(),
                    VertexHexKey.RIGHT_NEAR: self.tile.right(),
                    VertexHexKey.RIGHT_FAR: self.tile.right().up(),
                    VertexHexKey.OPPOSITE: self.tile.up()
                }
                object.__setattr__(self, "_tiles", tiles)
                return
            if self.tile.isDown():
                tiles = {
                    VertexHexKey.MAIN: self.tile,
                    VertexHexKey.LEFT_NEAR: self.tile.right(),
                    VertexHexKey.LEFT_FAR: self.tile.right().down(),
                    VertexHexKey.RIGHT_NEAR: self.tile.left(),
                    VertexHexKey.RIGHT_FAR: self.tile.left().down(),
                    VertexHexKey.OPPOSITE: self.tile.down()
                }
                object.__setattr__(self, "_tiles", tiles)
                return

    @property
    def main(self) -> Tile:
        return self._tiles[VertexHexKey.MAIN]

    @property
    def leftNear(self) -> Tile:
        return self._tiles[VertexHexKey.LEFT_NEAR]

    @property
    def leftFar(self) -> Tile:
        return self._tiles[VertexHexKey.LEFT_FAR]

    @property
    def rightNear(self) -> Tile:
        return self._tiles[VertexHexKey.RIGHT_NEAR]

    @property
    def rightFar(self) -> Tile:
        return self._tiles[VertexHexKey.RIGHT_FAR]

    @property
    def opposite(self) -> Tile:
        return self._tiles[VertexHexKey.OPPOSITE]
