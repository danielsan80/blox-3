import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.config import base_hole_d, side, taper_h, wall_w
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class BaseHoleOnEdgesVoid:
    mosaic: Mosaic

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_base_hole_void(placed_tile))
        return result

    def _tile_base_hole_void(self, placed_tile: PlacedTile) -> Workplane:

        tile = placed_tile.tile

        adjacent_tiles = tile.adjacent_tiles.to_list()

        middle_points = []

        for adjacent_tile in adjacent_tiles:
            if not self.mosaic.contains(adjacent_tile):
                continue

            common_points = list(
                set(tile.vertices.to_list()) & set(adjacent_tile.vertices.to_list())
            )
            middle_points += [common_points[0].move(common_points[1], side / 2)]

        result = Workplane("XY")

        for middle_point in middle_points:
            hole = (
                Workplane("XY")
                .placeSketch(Sketch().circle(base_hole_d / 2))
                .extrude(taper_h + wall_w)
                .translate(middle_point.to_tuple() + (0,))
            )
            result = result.union(hole)

        return result.translate((0, 0, -taper_h))
