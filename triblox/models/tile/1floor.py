import sys
sys.path.append('../../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import h, clr, ext
from triblox.mosaic.Mosaic import Mosaic
from triblox.helper.util import sin30


tile = Tile(0,0)


mosaic = Mosaic()

mosaic = (
    mosaic
    .add(Tile(0, 0))
    .add(Tile(1, 0))
    .add(Tile(1, 1))
    .add(Tile(0, 1))
    .add(Tile(-1, 1))
    .add(Tile(-1, 0))
)

ups = []
downs = []

result = (
    cq.Workplane("XY")
)

for placed_tile in mosaic.placed_tiles.values():
    base_up = (
        cq.Sketch().polygon([
            placed_tile.vertices.a.point().move(placed_tile.tile.incenter, clr*2).to_tuple(),
            placed_tile.vertices.b.point().move(placed_tile.tile.incenter, clr*2).to_tuple(),
            placed_tile.vertices.c.point().move(placed_tile.tile.incenter, clr*2).to_tuple(),
        ])
    )

    base_down = (
        cq.Sketch().polygon([
            placed_tile.vertices.a.point().move(placed_tile.tile.incenter, clr*2+ext*sin30*2).to_tuple(),
            placed_tile.vertices.b.point().move(placed_tile.tile.incenter, clr*2+ext*sin30*2).to_tuple(),
            placed_tile.vertices.c.point().move(placed_tile.tile.incenter, clr*2+ext*sin30*2).to_tuple(),
        ])
    )


    wp_up = cq.Workplane("XY").placeSketch(base_up)

    wp_down = cq.Workplane("XY").transformed(offset=(0, 0, -ext)).placeSketch(base_down)

    result = result.union(wp_up.add(wp_down).loft(combine=True))

#
#
# triangle = (
#     cq.Sketch().polygon([
#         tile.vertices.a.to_tuple(),
#         tile.vertices.b.to_tuple(),
#         tile.vertices.c.to_tuple(),
#     ])
# )
#
# base = (
#     cq.Sketch().polygon([
#         tile.vertices.a.move(tile.incenter, clr*2).to_tuple(),
#         tile.vertices.b.move(tile.incenter, clr*2).to_tuple(),
#         tile.vertices.c.move(tile.incenter, clr*2).to_tuple(),
#     ])
# )
#
# base_ext = (
#     cq.Sketch().polygon([
#         tile.vertices.a.move(tile.incenter, clr*2+ext*2).to_tuple(),
#         tile.vertices.b.move(tile.incenter, clr*2+ext*2).to_tuple(),
#         tile.vertices.c.move(tile.incenter, clr*2+ext*2).to_tuple(),
#     ])
# )
#
# wp1 = cq.Workplane("XY").placeSketch(base)
#
# wp2 = cq.Workplane("XY").transformed(offset=(0, 0, -ext)).placeSketch(base_ext)
#
# result = wp1.add(wp2).loft(combine=True)

show_object(result)