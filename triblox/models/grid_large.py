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
from triblox.grid.GridSolid import GridSolid
from triblox.grid.FineGridVoid import FineGridVoid
from triblox.grid.CustomGridVoid import CustomGridVoid
from triblox.mosaic.MosaicBuilder import MosaicBuilder
from typing import Dict, Tuple


hex_mosaic = (
    MosaicBuilder()
    .origin()
    .hex()
    .build()
)

voids = [
    hex_mosaic,

    hex_mosaic.move(0,2),
    hex_mosaic.move(0,-2),
    hex_mosaic.move(3,1),
    hex_mosaic.move(3,-1),
    hex_mosaic.move(-3,1),
    hex_mosaic.move(-3,-1),

    hex_mosaic.move(0,4),
    hex_mosaic.move(0,-4),
    hex_mosaic.move(3,3),
    hex_mosaic.move(3,-3),
    hex_mosaic.move(-3,3),
    hex_mosaic.move(-3,-3),

    hex_mosaic.move(6,2),
    hex_mosaic.move(6,0),
    hex_mosaic.move(6,-2),
    hex_mosaic.move(-6,2),
    hex_mosaic.move(-6,0),
    hex_mosaic.move(-6,-2),

]

builder = MosaicBuilder()
for void in voids:
    builder = builder.merge_mosaic(void)
mosaic = builder.build()

base = Base(mosaic)
grid_solid = GridSolid(mosaic)
fine_grid_void = FineGridVoid(mosaic)

custom_grid_void = CustomGridVoid()
for void in voids:
    custom_grid_void = custom_grid_void.add(void)

result = (
    Workplane("XY")
    .union(grid_solid.get())
    .cut(custom_grid_void.get())
#     .cut(fine_grid_void.get())
#     .union(base.get())
)

show_object(result)
exporters.export(result, 'grid.stl')

