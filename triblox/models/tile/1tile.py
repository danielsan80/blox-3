import sys
sys.path.append('../../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.Tile.Tile import Tile
from triblox.config import h, clr


tile = Tile(0,0)


triangle = (
    cq.Sketch().polygon([
        tile.vertices.a.toTuple(),
        tile.vertices.b.toTuple(),
        tile.vertices.c.toTuple(),
    ])
)

base = (
    cq.Sketch().polygon([
        tile.vertices.a.move(tile.incenter, clr*2).toTuple(),
        tile.vertices.b.move(tile.incenter, clr*2).toTuple(),
        tile.vertices.c.move(tile.incenter, clr*2).toTuple(),
    ])
)

result = (
    cq.Workplane("XY")
    .placeSketch(triangle)
    .extrude(1)
    .moveTo(0,0)
    .placeSketch(base)
    .extrude(h)
    .clean()
)

show_object(result)