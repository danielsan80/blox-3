import sys
sys.path.append('../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import clr, taper_h, h_clr, side, fix, stub_h
from triblox.block.functions import h
from triblox.mosaic.Mosaic import Mosaic
from triblox.helper.util import sin30, sin60, sin45
from dataclasses import dataclass
from triblox.block.Base import Base
from triblox.block.Prism import Prism
from triblox.block.TopVoid import TopVoid
from triblox.block.PrismVoid import PrismVoid
from triblox.block.BaseVoid import BaseVoid
from triblox.duct.Duct import Duct
from triblox.bowl.Bowl import Bowl
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
duct = Duct(
    Tile(1,1).vertices.c,
    h(hn),
    Tile(1,-2).vertices.c,
    h(1)+7/2+0.5,
    7,
)


spout_bottom = (
    Mosaic()
    .add(Tile(0, 0))
    .add(Tile(1, 0))
    .add(Tile(2, 0))
    .add(Tile(3, 0))
    .add(Tile(-1, 0))
)
spout_top = (
    spout_bottom
    .add(Tile(0, -1))
    .add(Tile(1, -1))
    .add(Tile(2, -1))
)

spout = Bowl(
    spout_bottom,
    spout_top,
    1
)
spout_border = Prism(spout_top, 3.5/h(1))

enter = Tile(1, 1).vertices.c
washer_void = (
    Workplane("XY")
    .circle(21/2)
    .extrude(2)
    .translate((enter.x, enter.y, h(hn) - clr -taper_h - stub_h - 2))
)





result = (
    Workplane("XY")
#     .union(duct.get())
    .union(base.get())
    .union(prism.get())
    .cut(top_void.get())
    .union(spout.get())
    .union(spout_border.get().translate((0, 0, h(1))))
    .cut(duct.get())
    .cut(washer_void)
#     .cut(prism_void.get())
#     .cut(base_void.get())
#     .cut(base_hole_void.get())
#     .cut(base_hole_on_edges_void.get())
#     .union(base.get().translate((0, 0, h(hn))))
#     .union(top_void.get().translate((0, 0, 0.1)))
)


show_object(result)
# exporters.export(result, "block.stl")
exporters.export(result, "incense_holder.stl")


end = time.perf_counter()
print(f"Execution Time: {end - start:.3f} seconds")