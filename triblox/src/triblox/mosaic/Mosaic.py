import sys

sys.path.append("src/")

from dataclasses import dataclass, field
from typing import Dict

from triblox.mosaic.PlacedTile import PlacedTile
from triblox.mosaic.PlacedVertices import PlacedVertices
from triblox.tile.Coord import Coord
from triblox.tile.Tile import Tile
from triblox.tile.VertexPos import VertexPos
from triblox.vertex.Vertex import Vertex


@dataclass(frozen=True)
class Mosaic:
    tiles: Dict[str, Tile] = field(default_factory=dict)

    def add(self, tile: Tile) -> "Mosaic":
        if self.contains(tile):
            raise ValueError(f"The mosaic already contains the tile {tile}")

        if not self.is_empty() and not self.is_adjacent(tile):
            raise ValueError(
                f"The tile {tile} is not adjacent to any tile in the mosaic"
            )

        key = str(tile.coord)
        tiles = self.tiles.copy()
        tiles[key] = tile
        return Mosaic(tiles=tiles)

    def contains(self, tile: Tile) -> bool:
        return str(tile.coord) in self.tiles

    def is_adjacent(self, tile: Tile) -> bool:
        if self.is_empty():
            raise ValueError("The mosaic is empty")

        if self.contains(tile):
            raise ValueError(f"The tile {tile} is already in the mosaic")

        return any(
            existing_tile.is_adjacent(tile) for existing_tile in self.tiles.values()
        )

    def is_empty(self) -> bool:
        return len(self.tiles) == 0

    def placed_tile(self, x: int, y: int) -> PlacedTile:
        tile = self.tiles.get(str(Coord(x, y)))
        if tile is None:
            raise ValueError(f"The tile at ({x}, {y}) is not in the mosaic")

        placed_vertices = PlacedVertices(
            self._placed_vertex(tile, VertexPos.A),
            self._placed_vertex(tile, VertexPos.B),
            self._placed_vertex(tile, VertexPos.C),
        )

        placed_tile = PlacedTile(tile, placed_vertices)
        return placed_tile

    @property
    def placed_tiles(self) -> Dict[str, PlacedTile]:
        placed_tiles = dict()
        for tile in self.tiles.values():
            placed_tile = self.placed_tile(tile.coord.x, tile.coord.y)
            placed_tiles[str(tile.coord)] = placed_tile

        return placed_tiles

    def _placed_vertex(self, tile: Tile, vertex_pos: VertexPos) -> Vertex:
        vertex = Vertex(tile, vertex_pos)

        for key, tile in vertex.hex.tiles.items():
            if self.contains(tile):
                vertex = vertex.mark_placed(key)

        return vertex

    def move(self, x: int, y: int) -> "Mosaic":
        mosaic = Mosaic()
        first = True
        for tile in self.tiles.values():
            if first and not tile.direction == tile.move(x, y).direction:
                raise ValueError("You cannot change the tiles direction")

            first = False
            mosaic = mosaic.add(tile.move(x, y))

        return mosaic

    def merge(self, other: "Mosaic") -> "Mosaic":
        mosaic = self

        for tile in other.tiles.values():
            if not mosaic.contains(tile):
                mosaic = mosaic.add(tile)

        return mosaic
