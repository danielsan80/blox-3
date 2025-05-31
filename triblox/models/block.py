import sys
sys.path.append('../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import clr, taper_h, h_clr, side, fix
from triblox.block.functions import h
from triblox.mosaic.Mosaic import Mosaic
from triblox.helper.util import sin30, sin60, sin45
from dataclasses import dataclass
from triblox.block.Base import Base
from triblox.block.Prism import Prism
from triblox.block.TopVoid import TopVoid
from triblox.block.PrismVoid import PrismVoid
from triblox.block.BaseVoid import BaseVoid
from triblox.block.BaseHoleVoid import BaseHoleVoid
from triblox.block.BaseHoleOnEdgesVoid import BaseHoleOnEdgesVoid
from triblox.mosaic.MosaicBuilder import MosaicBuilder
import time

start = time.perf_counter()

hn = 3.0

mosaic = (
    MosaicBuilder()
    .origin()
    .line_hor(3)
    .line_asc(3)
    .line_desc(-3)
    .line_hor(-3)
    .line_asc(-3)
    .line_desc(2)
    .move(1,1)
    .hex()
    .build()
)

base = Base(mosaic)
prism = Prism(mosaic,hn)
top_void = TopVoid(mosaic, hn)
# prism_void = PrismVoid(mosaic, hn)
# base_void = BaseVoid(mosaic)
# base_hole_void = BaseHoleVoid(mosaic)
# base_hole_on_edges_void = BaseHoleOnEdgesVoid(mosaic)



enter = Tile(1,1).vertices.c
exit = Tile(1,0).vertices.c
enter_z = h(hn)
exit_z = h(0.5)
enter_l = enter_z - exit_z
exit_l = enter.y-exit.y

curve_l = min(enter_l, exit_l)/2
channel_d = 6

# circle = (
#     Workplane("XY")
#     .transformed(offset=(enter.x, enter.y, h(hn)))
#     .circle(1.5)
# )

# vectors = [
#     Vector(enter.x, enter.y, h(hn)),
#     Vector(enter.x, enter.y, h(hn/5*4)),
#     Vector(enter.x, enter.y, h(hn/5*3)),
#     Vector(exit2.x, exit2.y, h(hn/4*1)),
#     Vector(exit.x, exit.y, h(hn/4*1)),
# ]

# path = (
#     Workplane("XY")
#     .spline(vectors)
# )

# channel = circle.sweep(path, multisection=False)

# points = [
#     (enter.x, enter.y, h(hn)),
#     (enter.x, enter.y, h(hn / 4 * 3)),
#     (exit2.x, exit2.y, h(hn / 4 * 1)),
#     (exit.x, exit.y, h(hn / 4 * 1)),
# ]

enter_section = (
    Workplane("XY")
    .transformed(offset=(enter.x, enter.y, enter_z))
    .circle(channel_d/2)
    .extrude(-enter_l+curve_l)
)

exit_section = (
    Workplane("XY")
    .circle(channel_d/2)
    .extrude(exit_l-curve_l)
    .rotate((0, 0, 0), (1, 0, 0), -90)
    .translate((exit.x, 0, exit_z))
)

vectors = [
    Vector(enter.x, enter.y, enter_z - enter_l + curve_l),
    Vector(enter.x, enter.y, enter_z - enter_l + curve_l-fix),
    Vector(enter.x, enter.y-curve_l+sin45*curve_l, enter_z - enter_l + curve_l- sin45*curve_l),
    Vector(exit.x, exit.y+exit_l-curve_l+fix, exit_z),
    Vector(exit.x, exit.y+exit_l-curve_l, exit_z),
]

path = (
    Workplane("XY")
    .spline(vectors)
)


curve_section = (
    Workplane("XY")
    .transformed(offset=(enter.x, enter.y, enter_z - enter_l + curve_l))
    .circle(channel_d/2)
    .sweep(path, multisection=False)
)

channel = (
    Workplane("XY")
    .union(enter_section)
    .union(exit_section)
    .union(curve_section)

#     .union(channel)
)

# for vector in vectors:
#     result = result.union(
#         Workplane("XY")
#         .transformed(offset=(vector.x, vector.y, vector.z))
#         .sphere(1.8)
#     )



result = (
    Workplane("XY")
    .union(base.get())
    .union(prism.get())
    .cut(top_void.get())
    .cut(channel)
#     .cut(prism_void.get())
#     .cut(base_void.get())
#     .cut(base_hole_void.get())
#     .cut(base_hole_on_edges_void.get())
#     .union(base.get().translate((0, 0, h(hn))))
#     .union(top_void.get().translate((0, 0, 0.1)))
)


show_object(result)
exporters.export(result, "block.stl")


end = time.perf_counter()
print(f"Execution Time: {end - start:.3f} seconds")