import sys
sys.path.append('../../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import h, clr, ext


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

base_ext = (
    cq.Sketch().polygon([
        tile.vertices.a.move(tile.incenter, clr*2+ext*2).toTuple(),
        tile.vertices.b.move(tile.incenter, clr*2+ext*2).toTuple(),
        tile.vertices.c.move(tile.incenter, clr*2+ext*2).toTuple(),
    ])
)

wp1 = cq.Workplane("XY").placeSketch(base)

wp2 = cq.Workplane("XY").transformed(offset=(0, 0, -ext)).placeSketch(base_ext)

result = wp1.add(wp2).loft(combine=True)

show_object(result)