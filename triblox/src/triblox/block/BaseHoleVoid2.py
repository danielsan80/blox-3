import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.config import clr, ext, h_clr, h_cut, wall_w, base_hole_margin
from triblox.helper.util import normalize_float, sin30
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

        triangle = Sketch().polygon(
            [
                placed_tile.vertices.a.point()
                .move(placed_tile.tile.incenter, clr*2 + wall_w*2 + base_hole_margin*2 )
                .to_tuple(),
                placed_tile.vertices.b.point()
                .move(placed_tile.tile.incenter, clr*2 + wall_w*2 + base_hole_margin*2)
                .to_tuple(),
                placed_tile.vertices.c.point()
                .move(placed_tile.tile.incenter, clr*2 + wall_w*2 + base_hole_margin*2)
                .to_tuple(),
            ]
        )

        result = (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(wall_w)
            .translate((0, 0, -ext))
        )

        return result

