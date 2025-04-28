import sys
sys.path.append('../../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import h, clr, ext, wall_w, h_fix
from triblox.helper.util import sin30


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
        tile.vertices.a.move(tile.incenter, clr*2+ext*sin30*2).toTuple(),
        tile.vertices.b.move(tile.incenter, clr*2+ext*sin30*2).toTuple(),
        tile.vertices.c.move(tile.incenter, clr*2+ext*sin30*2).toTuple(),
    ])
)

base_void = (
    cq.Sketch().polygon([
        tile.vertices.a.move(tile.incenter, clr*2).toTuple(),
        tile.vertices.b.move(tile.incenter, clr*2).toTuple(),
        tile.vertices.c.move(tile.incenter, clr*2).toTuple(),
    ])
)

base_void_ext = (
    cq.Sketch().polygon([
        tile.vertices.a.move(tile.incenter, clr*2+ext*2).toTuple(),
        tile.vertices.b.move(tile.incenter, clr*2+ext*2).toTuple(),
        tile.vertices.c.move(tile.incenter, clr*2+ext*2).toTuple(),
    ])
)


wp1 = cq.Workplane("XY").placeSketch(base)

wp2 = cq.Workplane("XY").transformed(offset=(0, 0, -ext)).placeSketch(base_ext)

floor = wp1.add(wp2).loft(combine=True)
prism = (
    cq.Workplane("XY")
    .placeSketch(base)
    .extrude(h-h_fix)
)


result = (
    cq.Workplane("XY")
    .add(floor)
    .add(prism)
    .cut(floor.translate((0,0,h)))
)

show_object(result)

exporters.export(result, "1block.stl")