import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.config import base_hole_margin, clr, taper_h, stub_h, wall_w
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class BaseHoleVoid:
    mosaic: Mosaic

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_base_hole_void(placed_tile))
        return result

    def _tile_base_hole_void(self, placed_tile: PlacedTile) -> Workplane:

        points = placed_tile.vertices.centered_points(clr + wall_w + base_hole_margin)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)

        result = (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(wall_w)
            .translate((0, 0, -taper_h-stub_h))
        )

        return result
