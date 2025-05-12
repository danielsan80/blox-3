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
from triblox.block.BaseHoleVoid2 import BaseHoleVoid2

hn = 1.5

mosaic = (
    Mosaic()
    .add(Tile(0, 0))
    .add(Tile(1, 0))
    .add(Tile(1, 1))
    .add(Tile(0, 1))
    .add(Tile(-1, 1))
    .add(Tile(-1, 0))
)

base = Base(mosaic)
prism = Prism(mosaic,hn)
topVoid = TopVoid(mosaic, hn)
prismVoid = PrismVoid(mosaic, hn)
baseVoid = BaseVoid(mosaic)
# baseHoleVoid = BaseHoleVoid(mosaic)
# baseHoleVoid2 = BaseHoleVoid2(mosaic)

result = (
    Workplane("XY")
    .union(base.get())
    .union(prism.get())
    .cut(topVoid.get())
    .cut(prismVoid.get())
    .cut(baseVoid.get())
#     .cut(baseHoleVoid.get())
#     .cut(baseHoleVoid2.get())
#     .union(base.get().translate((0, 0, h(hn))))
#     .union(topVoid.get().translate((0, 0, 0.1)))
)


show_object(result)
exporters.export(result, "block.stl")