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

    def _offsets(i: int) -> [int, int]:
        offsets = [
            [0,0],
            [-1,0],
            [-1,1],
            [0,1],
            [1,1],
            [1,0]
        ]

        main = offsets[i].copy()

        for j in range(6):
            offsets[j][0] -= main[0]
            offsets[j][1] -= main[1]

        offsets = offsets[i:] + offsets[:i]

        return offsets


    def __post_init__(self):

        if self.tile.isUp() and self.refVertexPos == VertexPos.C:
            offset = VertexHex._offsets(0)
        if self.tile.isDown() and self.refVertexPos == VertexPos.A:
            offset = VertexHex._offsets(1)
        if self.tile.isUp() and self.refVertexPos == VertexPos.B:
            offset = VertexHex._offsets(2)
        if self.tile.isDown() and self.refVertexPos == VertexPos.C:
            offset = VertexHex._offsets(3)
        if self.tile.isUp() and self.refVertexPos == VertexPos.A:
            offset = VertexHex._offsets(4)
        if self.tile.isDown() and self.refVertexPos == VertexPos.B:
            offset = VertexHex._offsets(5)

        tiles = {
            VertexHexKey.MAIN: self.tile.move(offset[0][0], offset[0][1]),
            VertexHexKey.LEFT_NEAR: self.tile.move(offset[1][0], offset[1][1]),
            VertexHexKey.LEFT_FAR: self.tile.move(offset[2][0], offset[2][1]),
            VertexHexKey.OPPOSITE: self.tile.move(offset[3][0], offset[3][1]),
            VertexHexKey.RIGHT_FAR: self.tile.move(offset[4][0], offset[4][1]),
            VertexHexKey.RIGHT_NEAR: self.tile.move(offset[5][0], offset[5][1]),
        }
        object.__setattr__(self, "_tiles", tiles)


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
