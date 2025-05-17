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
from triblox.bowl.Bowl import Bowl

hn = 1

mosaic_bottom = (
    Mosaic()
    .add(Tile(0, 0))
    .add(Tile(1, 0))
    .add(Tile(1, 1))
    .add(Tile(0, 1))
    .add(Tile(-1, 1))
    .add(Tile(-1, 0))
)

mosaic_top = (
    mosaic_bottom
    .add(Tile(0, -1))
    .add(Tile(1, -1))
    .add(Tile(2, -1))
    .add(Tile(2, 0))
    .add(Tile(3, 0))
    .add(Tile(3, 1))
    .add(Tile(2, 1))
    .add(Tile(2, 2))
    .add(Tile(1, 2))
    .add(Tile(0, 2))
    .add(Tile(-1, 2))
    .add(Tile(-2, 2))
    .add(Tile(-2, 1))
    .add(Tile(-3, 1))
    .add(Tile(-3, 0))
#     .add(Tile(-2, 0))
    .add(Tile(-1, -1))
    .add(Tile(-2, -1))

)



# base = Base(mosaic_bottom)
bowl = Bowl(mosaic_bottom, mosaic_top,hn)

result = (
    Workplane("XY")
#     .union(base.get())
    .union(bowl.get())
)


show_object(result)
exporters.export(result, "bowl.stl")