import sys

sys.path.append("src/")

from dataclasses import dataclass, field
from typing import Dict

from triblox.tile.Tile import Tile


@dataclass(frozen=True)
class Mosaic:
    tiles: Dict[str, Tile] = field(default_factory=dict)

    def add(self, tile: Tile) -> "Mosaic":
        if self.contains(tile):
            raise ValueError(f"The mosaic already contains the tile {tile}")

        if not self.isEmpty() and not self.isAdjacent(tile):
            raise ValueError(
                f"The tile {tile} is not adjacent to any tile in the mosaic"
            )

        key = str(tile.coord)
        newTiles = self.tiles.copy()
        newTiles[key] = tile
        return Mosaic(tiles=newTiles)

    def contains(self, tile: Tile) -> bool:
        return str(tile.coord) in self.tiles

    def isAdjacent(self, tile: Tile) -> bool:
        if self.isEmpty():
            raise ValueError("The mosaic is empty")

        if self.contains(tile):
            raise ValueError(f"The tile {tile} is already in the mosaic")

        return any(
            existingTile.isAdjacent(tile) for existingTile in self.tiles.values()
        )

    def isEmpty(self) -> bool:
        return len(self.tiles) == 0
