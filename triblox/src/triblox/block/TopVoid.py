import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.config import clr, h_clr, h_cut, taper_h
from triblox.helper.util import normalize_float, sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class TopVoid:
    mosaic: Mosaic
    h: float

    def __post_init__(self):
        if self.h <= 0:
            raise ValueError("Height must be greater than 0")
        object.__setattr__(self, "h", normalize_float(self.h))

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_base_void(placed_tile))
            result = result.union(self._tile_top_leveling(placed_tile))

        result = result.translate((0, 0, h(self.h)))
        return result

    def _tile_base_void(self, placed_tile: PlacedTile) -> Workplane:
        clr1 = 0.00001
        points = placed_tile.vertices.offset_points(clr1)
        points = [point.to_tuple() for point in points]
        base_up = Sketch().polygon(points)

        points = placed_tile.vertices.offset_points(clr1 + (taper_h + clr) * sin30)
        points = [point.to_tuple() for point in points]
        base_down = Sketch().polygon(points)

        wp_up = Workplane("XY").placeSketch(base_up)

        wp_down = (
            Workplane("XY")
            .transformed(offset=(0, 0, -taper_h - clr))
            .placeSketch(base_down)
        )

        return wp_up.add(wp_down).loft(combine=True)

    def _tile_top_leveling(self, placed_tile) -> Workplane:
        points = placed_tile.vertices.offset_points(clr)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)
        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(h_clr + h_cut)
            .translate((0, 0, -h_clr - h_cut))
        )
