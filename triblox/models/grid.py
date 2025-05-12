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
from typing import Dict, Tuple


mosaic = (
    Mosaic()
    .add(Tile(0, 0))
    .add(Tile(1, 0))
    .add(Tile(1, 1))
    .add(Tile(0, 1))
    .add(Tile(-1, 1))
    .add(Tile(-1, 0))

    .add(Tile(2, 1))
    .add(Tile(3, 1))
    .add(Tile(4, 1))
    .add(Tile(2, 2))
    .add(Tile(3, 2))
    .add(Tile(4, 2))

    .add(Tile(0, 2))
    .add(Tile(1, 2))
    .add(Tile(-1, 2))
    .add(Tile(1, 3))
    .add(Tile(0, 3))
    .add(Tile(-1, 3))

    .add(Tile(2, 3))
    .add(Tile(3, 3))

    .add(Tile(2, 0))
    .add(Tile(3, 0))

    .add(Tile(-2, 1))
    .add(Tile(-2, 2))

)

base = Base(mosaic)
grid_solid = GridSolid(mosaic)
fine_grid_void = FineGridVoid(mosaic)

custom_grid_void = (
    CustomGridVoid()
    .add(
        Mosaic()
        .add(Tile(0, 0))
        .add(Tile(1, 0))
        .add(Tile(-1, 0))
        .add(Tile(-1, 1))
        .add(Tile(0, 1))
        .add(Tile(1, 1))
    )
    .add(
        Mosaic()
        .add(Tile(2, 1))
        .add(Tile(3, 1))
        .add(Tile(4, 1))
        .add(Tile(2, 2))
        .add(Tile(3, 2))
        .add(Tile(4, 2))
    )
    .add(
        Mosaic()
        .add(Tile(0, 2))
        .add(Tile(1, 2))
        .add(Tile(-1, 2))
        .add(Tile(-1, 3))
        .add(Tile(0, 3))
        .add(Tile(1, 3))
    )
    .add(
        Mosaic()
        .add(Tile(2, 0))
        .add(Tile(3, 0))
    )
    .add(
        Mosaic()
        .add(Tile(-2, 1))
        .add(Tile(-2, 2))
    )
    .add(
        Mosaic()
        .add(Tile(2, 3))
        .add(Tile(3, 3))
    )
)

result = (
    Workplane("XY")
    .union(grid_solid.get())
#     .cut(custom_grid_void.get())
    .cut(fine_grid_void.get())
#     .union(base.get())
)

show_object(result)
exporters.export(result, 'grid.stl')

