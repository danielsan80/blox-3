import sys
sys.path.append('../../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import h, clr


tile = Tile(0,0)


triangle = (
    cq.Sketch().polygon([
        tile.vertices.a.to_tuple(),
        tile.vertices.b.to_tuple(),
        tile.vertices.c.to_tuple(),
    ])
)

base = (
    cq.Sketch().polygon([
        tile.vertices.a.move(tile.incenter, clr*2).to_tuple(),
        tile.vertices.b.move(tile.incenter, clr*2).to_tuple(),
        tile.vertices.c.move(tile.incenter, clr*2).to_tuple(),
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