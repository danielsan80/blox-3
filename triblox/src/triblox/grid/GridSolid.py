import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.config import clr, ext, h_clr, h_grid_fix
from triblox.helper.util import sin30
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
        points = []
        points += placed_tile.vertices.a.moved_points(clr)
        points += placed_tile.vertices.b.moved_points(clr)
        points += placed_tile.vertices.c.moved_points(clr)

        points = [point.to_tuple() for point in points]

        triangle = Sketch().polygon(points)
        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(ext - h_clr + h_grid_fix)
            .translate((0, 0, -ext))
        )

    def _tile_base_void(self, placed_tile: PlacedTile) -> Workplane:
        points = []
        points += [placed_tile.vertices.a.point()]
        points += [placed_tile.vertices.b.point()]
        points += [placed_tile.vertices.c.point()]

        points = [point.to_tuple() for point in points]

        up = Sketch().polygon(points)

        points = [
            placed_tile.vertices.a.point().move(
                placed_tile.tile.incenter, ext * sin30 * 2
            ),
            placed_tile.vertices.b.point().move(
                placed_tile.tile.incenter, ext * sin30 * 2
            ),
            placed_tile.vertices.c.point().move(
                placed_tile.tile.incenter, ext * sin30 * 2
            ),
        ]

        points = [point.to_tuple() for point in points]

        down = Sketch().polygon(points)

        wp_up = Workplane("XY").placeSketch(up)

        wp_down = Workplane("XY").transformed(offset=(0, 0, -ext)).placeSketch(down)

        return wp_up.add(wp_down).loft(combine=True)
