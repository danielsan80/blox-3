import sys
sys.path.append('../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import clr, taper_h, h_clr
from triblox.block.functions import h
from triblox.mosaic.Mosaic import Mosaic
from triblox.helper.util import sin30
from dataclasses import dataclass
from triblox.block.Base import Base
from triblox.block.Prism import Prism
from triblox.block.TopVoid import TopVoid
from triblox.block.PrismVoid import PrismVoid
from triblox.block.BaseVoid import BaseVoid
from triblox.block.BaseHoleVoid import BaseHoleVoid
from triblox.block.BaseHoleOnEdgesVoid import BaseHoleOnEdgesVoid
from triblox.mosaic.MosaicBuilder import MosaicBuilder

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
prism_void = PrismVoid(mosaic, hn)
base_void = BaseVoid(mosaic)
base_hole_void = BaseHoleVoid(mosaic)
# base_hole_on_edges_void = BaseHoleOnEdgesVoid(mosaic)

result = (
    Workplane("XY")
    .union(base.get())
    .union(prism.get())
    .cut(top_void.get())
    .cut(prism_void.get())
    .cut(base_void.get())
    .cut(base_hole_void.get())
#     .cut(base_hole_on_edges_void.get())
#     .union(base.get().translate((0, 0, h(hn))))
#     .union(top_void.get().translate((0, 0, 0.1)))
)


show_object(result)
# exporters.export(result, "block.stl")