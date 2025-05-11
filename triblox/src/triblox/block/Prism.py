import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.config import clr
from triblox.helper.util import normalize_float
from triblox.mosaic.Mosaic import Mosaic


@dataclass(frozen=True)
class Prism:
    mosaic: Mosaic
    h: float

    def __post_init__(self):
        if self.h <= 0:
            raise ValueError("Height must be greater than 0")
        object.__setattr__(self, "h", normalize_float(self.h))

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_prism(placed_tile))

        return result

    def _tile_prism(self, placed_tile) -> Workplane:
        points = placed_tile.vertices.offset_points(clr)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)

        return Workplane("XY").placeSketch(triangle).extrude(h(self.h))
