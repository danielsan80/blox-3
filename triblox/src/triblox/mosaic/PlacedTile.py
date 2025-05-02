import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.tile.Tile import Tile


@dataclass(frozen=True)
class PlacedTile:
    tile: Tile

    def vertexHexes(self) -> VertexHexes:
        a = VertexHex(self.tile)
