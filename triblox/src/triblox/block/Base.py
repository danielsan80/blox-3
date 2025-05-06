import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.config import clr, ext
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
        base_up = Sketch().polygon(
            [
                placed_tile.vertices.a.point()
                .move(placed_tile.tile.incenter, clr * 2)
                .to_tuple(),
                placed_tile.vertices.b.point()
                .move(placed_tile.tile.incenter, clr * 2)
                .to_tuple(),
                placed_tile.vertices.c.point()
                .move(placed_tile.tile.incenter, clr * 2)
                .to_tuple(),
            ]
        )

        base_down = Sketch().polygon(
            [
                placed_tile.vertices.a.point()
                .move(placed_tile.tile.incenter, clr * 2 + ext * sin30 * 2)
                .to_tuple(),
                placed_tile.vertices.b.point()
                .move(placed_tile.tile.incenter, clr * 2 + ext * sin30 * 2)
                .to_tuple(),
                placed_tile.vertices.c.point()
                .move(placed_tile.tile.incenter, clr * 2 + ext * sin30 * 2)
                .to_tuple(),
            ]
        )

        wp_up = Workplane("XY").placeSketch(base_up)

        wp_down = (
            Workplane("XY").transformed(offset=(0, 0, -ext)).placeSketch(base_down)
        )

        return wp_up.add(wp_down).loft(combine=True)
