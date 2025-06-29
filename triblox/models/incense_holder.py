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
from math import radians, cos, sin
from triblox.washer.WasherVoid import WasherVoid
from triblox.spout.Spout import Spout

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

duct_enter = Tile(1, 1).vertices.c
duct_exit = Tile(1,-2).vertices.c
duct_d = 7

washer_h_cork = 4
washer_h_steel = 2
washer_d = 25.5

spout_margin = 0.5

duct = Duct(
    duct_enter,
    h(hn)-washer_h_steel-washer_h_cork,
    duct_exit,
    h(1)+duct_d/2+spout_margin,
    duct_d,
)


spout = Spout(
    duct_d=duct_d,
    top_h=duct_d/2
)

washer_void = WasherVoid(
    h=hn,
    washer_center=duct_enter,
    washer_h=washer_h_cork+washer_h_steel,
    washer_d=washer_d
)

result = (
    Workplane("XY")
    .union(base.get())
    .union(prism.get())
    .cut(top_void.get())
    .union(spout.get())
    .cut(duct.get())
    .cut(washer_void.get())
)


show_object(result)
exporters.export(result, "incense_holder.stl")


end = time.perf_counter()
print(f"Execution Time: {end - start:.3f} seconds")