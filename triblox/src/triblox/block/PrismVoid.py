import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.config import clr, ext, h_clr, h_cut, wall_w
from triblox.helper.util import normalize_float, sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class PrismVoid:
    mosaic: Mosaic
    h: float

    def __post_init__(self):
        if self.h <= 0:
            raise ValueError("Height must be greater than 0")
        object.__setattr__(self, "h", normalize_float(self.h))

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_prism_void(placed_tile))
        return result

    def _tile_prism_void(self, placed_tile: PlacedTile) -> Workplane:
        points = []
        points += placed_tile.vertices.a.moved_points(clr+wall_w)
        points += placed_tile.vertices.b.moved_points(clr+wall_w)
        points += placed_tile.vertices.c.moved_points(clr+wall_w)

        points = [point.to_tuple() for point in points]

        triangle = Sketch().polygon(points)

        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(h(self.h)-ext-clr-wall_w)
            .translate((0, 0, wall_w))
        )
