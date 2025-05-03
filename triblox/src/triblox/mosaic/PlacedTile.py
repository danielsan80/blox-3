import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.tile.Tile import Tile
from triblox.mosaic.VertexHexes import VertexHexes
from triblox.mosaic.VertexHex import VertexHex
from triblox.mosaic.VertexPos import VertexPos


@dataclass(frozen=True)
class PlacedTile:
    tile: Tile

    @property
    def vertexHexes(self) -> VertexHexes:
        a = VertexHex(self.tile, VertexPos.A)
        b = VertexHex(self.tile, VertexPos.B)
        c = VertexHex(self.tile, VertexPos.C)

        return VertexHexes(a, b, c)
