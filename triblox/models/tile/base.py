import sys
sys.path.append('../../src/')

from cadquery import Workplane, Sketch, Vector, Location, exporters
from pprint import pprint

from triblox.tile.Tile import Tile
from triblox.config import h, clr, ext
from triblox.mosaic.Mosaic import Mosaic
from triblox.helper.util import sin30
from dataclasses import dataclass
# import Base
from triblox.block.Base import Base

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

show_object(base.get())