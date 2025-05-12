import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.config import taper_h, stub_h
from triblox.helper.util import sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class FineGridVoid:
    mosaic: Mosaic

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._taper_void(placed_tile))
            result = result.union(self._stub_void(placed_tile))

        return result

    def _taper_void(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.original_points()
        points = [point.to_tuple() for point in points]
        up = Sketch().polygon(points)

        points = placed_tile.vertices.centered_points(taper_h * sin30)
        points = [point.to_tuple() for point in points]
        down = Sketch().polygon(points)

        wp_up = Workplane("XY").placeSketch(up)

        wp_down = Workplane("XY").transformed(offset=(0, 0, -taper_h)).placeSketch(down)

        return wp_up.add(wp_down).loft(combine=True)

    def _stub_void(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.centered_points(taper_h * sin30)
        points = [point.to_tuple() for point in points]
        down = Sketch().polygon(points)

        return (
            Workplane("XY")
            .transformed(offset=(0, 0, -taper_h-stub_h))
            .placeSketch(down)
            .extrude(stub_h)
        )
