import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.config import clr, h_clr, h_grid_fix, taper_h
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class GridSolid:
    mosaic: Mosaic

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_base_solid(placed_tile))
        #             result = result.cut(self._tile_base_void(placed_tile))

        return result

    def _tile_base_solid(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.offset_points(clr)
        points = [point.to_tuple() for point in points]

        triangle = Sketch().polygon(points)
        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(taper_h - h_clr + h_grid_fix)
            .translate((0, 0, -taper_h))
        )


#     def _tile_base_void(self, placed_tile: PlacedTile) -> Workplane:
#         points = placed_tile.vertices.original_points()
#         points = [point.to_tuple() for point in points]
#         up = Sketch().polygon(points)
#
#         points = placed_tile.vertices.centered_points(taper_h * sin30)
#         points = [point.to_tuple() for point in points]
#         down = Sketch().polygon(points)
#
#         wp_up = Workplane("XY").placeSketch(up)
#
#         wp_down = Workplane("XY").transformed(offset=(0, 0, -taper_h)).placeSketch(down)
#
#         return wp_up.add(wp_down).loft(combine=True)
