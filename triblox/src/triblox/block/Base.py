import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.config import clr, taper_h
from triblox.helper.util import sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class Base:
    mosaic: Mosaic

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_base(placed_tile))

        return result

    def _tile_base(self, placed_tile: PlacedTile) -> Workplane:

        points = placed_tile.vertices.centered_points(clr)
        points = [point.to_tuple() for point in points]
        base_up = Sketch().polygon(points)

        points = placed_tile.vertices.centered_points(clr + taper_h * sin30)
        points = [point.to_tuple() for point in points]
        base_down = Sketch().polygon(points)

        wp_up = Workplane("XY").placeSketch(base_up)

        wp_down = (
            Workplane("XY").transformed(offset=(0, 0, -taper_h)).placeSketch(base_down)
        )

        return wp_up.add(wp_down).loft(combine=True)
