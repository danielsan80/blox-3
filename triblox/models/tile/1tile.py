import sys
sys.path.append('../../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import h, clr
from triblox.mosaic.Mosaic import Mosaic

tile = Tile(0, 0)

mosaic = Mosaic()

mosaic = (
    mosaic
    .add(Tile(0, 0))
    .add(Tile(1, 0))
    .add(Tile(1, 1))
    .add(Tile(0, 1))
    .add(Tile(-1, 1))
#     .add(Tile(-1, 0))
)

triangles = []
bases = []

result = (
    cq.Workplane("XY")
)

i=0
for placed_tile in mosaic.placed_tiles.values():

    base = (
        cq.Sketch().polygon([
            placed_tile.vertices.a.point().to_tuple(),
            placed_tile.vertices.b.point().to_tuple(),
            placed_tile.vertices.c.point().to_tuple(),
        ])
    )

    result = result.union(
        cq.Workplane("XY")
        .placeSketch(base)
        .extrude(1)
    )

    points = []
    points += placed_tile.vertices.a.moved_points(1)
    points += placed_tile.vertices.b.moved_points(1)
    points += placed_tile.vertices.c.moved_points(1)

    points = [point.to_tuple() for point in points]

    triangle = (
        cq.Sketch().polygon(points)
    )

    i -=0.2
    result = result.union(
        cq.Workplane("XY")
        .placeSketch(triangle)
        .extrude(h+i)
    )

show_object(result)
