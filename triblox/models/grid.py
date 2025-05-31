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

builder = MosaicBuilder()

mosaic = (
    MosaicBuilder()
    .origin()
    .hex()
    .move_up(2)
    .hex()
    .move_down()
    .move_right(3)
    .hex()
    .move_down()
    .here()
    .left()
    .move_up(3)
    .here()
    .right()
    .move_down()
    .move_left(5)
    .here()
    .down()
    .build()
)

base = Base(mosaic)
grid_solid = GridSolid(mosaic)
fine_grid_void = FineGridVoid(mosaic)

custom_grid_void = (
    CustomGridVoid()
    .add(
        MosaicBuilder()
        .origin()
        .hex()
        .build()
    )
    .add(
        MosaicBuilder()
        .move_up(2)
        .hex()
        .build()
    )
    .add(
        MosaicBuilder()
        .move_up()
        .move_right(3)
        .hex()
        .build()
    )
    .add(
        MosaicBuilder()
        .move_right(2)
        .here()
        .right()
        .build()
    )
    .add(
        MosaicBuilder()
        .move_up()
        .move_left(2)
        .here()
        .up()
        .build()
    )
    .add(
        MosaicBuilder()
        .move_up(3)
        .move_right(2)
        .here()
        .right()
        .build()
    )
)

result = (
    Workplane("XY")
    .union(grid_solid.get())
    .cut(custom_grid_void.get())
#     .cut(fine_grid_void.get())
#     .union(base.get())
)

show_object(result)
# exporters.export(result, 'grid.stl')

