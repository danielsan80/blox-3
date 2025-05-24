import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.mosaic.PlacedVertices import PlacedVertices
from triblox.tile.Tile import Tile
from triblox.geometry.Point import Point


@dataclass(frozen=True)
class PlacedTile:
    tile: Tile
    vertices: PlacedVertices

    def common_points(self, other_placed_tile: "PlacedTile") -> list[Point]:
        common_points = []
        for point in self.tile.vertices.to_list():
            if point in other_placed_tile.tile.vertices.to_list():
                common_points += [point]
        return common_points
