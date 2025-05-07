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
class BaseVoid:
    mosaic: Mosaic

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._tile_base_void(placed_tile))
        return result

    def _tile_base_void(self, placed_tile: PlacedTile) -> Workplane:

        base_up = Sketch().polygon(
            [
                placed_tile.vertices.a.point()
                .move(placed_tile.tile.incenter, clr*2 + wall_w*2)
                .to_tuple(),
                placed_tile.vertices.b.point()
                .move(placed_tile.tile.incenter, clr*2 + wall_w*2)
                .to_tuple(),
                placed_tile.vertices.c.point()
                .move(placed_tile.tile.incenter, clr*2 + wall_w*2)
                .to_tuple(),
            ]
        )

        base_down = Sketch().polygon(
            [
                placed_tile.vertices.a.point()
                .move(placed_tile.tile.incenter, clr * 2 + wall_w*2 + ext * sin30 * 2)
                .to_tuple(),
                placed_tile.vertices.b.point()
                .move(placed_tile.tile.incenter, clr * 2 + wall_w*2 + ext * sin30 * 2)
                .to_tuple(),
                placed_tile.vertices.c.point()
                .move(placed_tile.tile.incenter, clr * 2 + wall_w*2 + ext * sin30 * 2)
                .to_tuple(),
            ]
        )

        wp_up = Workplane("XY").placeSketch(base_up)

        wp_down = (
            Workplane("XY").transformed(offset=(0, 0, -ext)).placeSketch(base_down)
        )

        return wp_up.add(wp_down).loft(combine=True).translate((0,0,wall_w))

