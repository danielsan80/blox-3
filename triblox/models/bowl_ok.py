import sys
sys.path.append('../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import clr, taper_h, h_clr, wall_w
from triblox.block.functions import h
from triblox.mosaic.Mosaic import Mosaic
from triblox.helper.util import sin30
from dataclasses import dataclass
from triblox.block.Base import Base
from triblox.block.BaseVoid import BaseVoid
from triblox.block.Prism import Prism
from triblox.block.TopVoid import TopVoid
from triblox.block.PrismVoid import PrismVoid
from triblox.block.BaseVoid import BaseVoid
from triblox.block.BaseHoleVoid import BaseHoleVoid
from triblox.bowl.Bowl import Bowl
from triblox.bowl.BowlVoid import BowlVoid
from triblox.duct.Duct import Duct


hu = 1
top_prism_hu = 0.5
thick = 3

duct_enter = Tile(0, 0).vertices.c
duct_exit = Tile(0,-3).vertices.c
duct_d = 8
duct_offset = -0.5

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
    .add(Tile(-2, 0))
    .add(Tile(-1, -1))
    .add(Tile(-2, -1))

)

base = Base(mosaic_bottom)
# base_void = BaseVoid(mosaic_bottom)
bowl = Bowl(mosaic_bottom, mosaic_top,hu)
bowl_void = BowlVoid(mosaic_bottom=mosaic_bottom, mosaic_top=mosaic_top,hu=hu,wall_thick=thick, bottom_thick=thick)
prism = Prism(mosaic_top,top_prism_hu)
prism_void = PrismVoid(mosaic=mosaic_top, hu=top_prism_hu, wall_thick=thick, bottom_thick=0)
top_void = TopVoid(mosaic_top, top_prism_hu)
duct = Duct(
    duct_enter,
    h(hu*2),
    duct_exit,
    h(hu)+h(top_prism_hu)+duct_offset,
    duct_d,
)


result = (
    Workplane("XY")
    .union(base.get())
    .union(bowl.get())
    .cut(bowl_void.get())
    .union(
        Workplane("XY")
        .union(prism.get())
        .cut(prism_void.get())
        .cut(top_void.get())
        .translate((0, 0, h(hu)))
    )
    .cut(duct.get())
#     .cut(base_void.get())
)


show_object(result)
exporters.export(result, "bowl.stl")