import sys

sys.path.append("src/")

from dataclasses import dataclass, field
from typing import Dict, Tuple

from triblox.vertex.VertexHexKey import VertexHexKey
from triblox.tile.VertexPos import VertexPos
from triblox.tile.Direction import DirectionValue
from triblox.tile.Tile import Tile


@dataclass(frozen=True)
class VertexHex:
    tile: Tile
    vertexPos: VertexPos
    tiles: Dict[VertexHexKey, Tile] = field(init=False)

    def _offsets(i: int) -> Tuple[Tuple[int, int], ...]:
        offsets = [[0, 0], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0]]

        main = offsets[i].copy()

        for j in range(6):
            offsets[j][0] -= main[0]
            offsets[j][1] -= main[1]

        offsets = offsets[i:] + offsets[:i]

        return offsets

    def __post_init__(self):
        map = {
            (DirectionValue.UP, VertexPos.C): 0,
            (DirectionValue.DOWN, VertexPos.A): 1,
            (DirectionValue.UP, VertexPos.B): 2,
            (DirectionValue.DOWN, VertexPos.C): 3,
            (DirectionValue.UP, VertexPos.A): 4,
            (DirectionValue.DOWN, VertexPos.B): 5,
        }

        i = map.get((self.tile.direction.value, self.vertexPos))
        offset = VertexHex._offsets(i)

        tiles = {
            VertexHexKey.MAIN: self.tile.move(offset[0][0], offset[0][1]),
            VertexHexKey.LEFT_NEAR: self.tile.move(offset[1][0], offset[1][1]),
            VertexHexKey.LEFT_FAR: self.tile.move(offset[2][0], offset[2][1]),
            VertexHexKey.OPPOSITE: self.tile.move(offset[3][0], offset[3][1]),
            VertexHexKey.RIGHT_FAR: self.tile.move(offset[4][0], offset[4][1]),
            VertexHexKey.RIGHT_NEAR: self.tile.move(offset[5][0], offset[5][1]),
        }

        object.__setattr__(self, "tiles", tiles)

    @property
    def main(self) -> Tile:
        return self.tiles[VertexHexKey.MAIN]

    @property
    def leftNear(self) -> Tile:
        return self.tiles[VertexHexKey.LEFT_NEAR]

    @property
    def leftFar(self) -> Tile:
        return self.tiles[VertexHexKey.LEFT_FAR]

    @property
    def rightNear(self) -> Tile:
        return self.tiles[VertexHexKey.RIGHT_NEAR]

    @property
    def rightFar(self) -> Tile:
        return self.tiles[VertexHexKey.RIGHT_FAR]

    @property
    def opposite(self) -> Tile:
        return self.tiles[VertexHexKey.OPPOSITE]
