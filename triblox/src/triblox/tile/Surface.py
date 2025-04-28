import sys
sys.path.append('src/')

from math import sin
from triblox.config import side
from triblox.point.Point import Point
from triblox.tile.Direction import Direction
from triblox.tile.Vertices import Vertices
from triblox.tile.Coord import Coord
from triblox.tile.Tile import Tile
from triblox.helper.util import sin60

from dataclasses import dataclass, field
from typing import Tuple

@dataclass(frozen=True)
class Surface:
    tiles: Tuple[Tile, ...] = field(default_factory=tuple)

    def __init__(self):
        raise RuntimeError("Use Surface.create() instead of Surface()")

    @classmethod
    def create(cls) -> "Surface":
        obj = object.__new__(cls)
        object.__setattr__(obj, "tiles", tuple())
        return obj

    def add(self, tile: Tile) -> "Surface":
        obj = object.__new__(cls)
        object.__setattr__(obj, "tiles", self.tiles + (tile,))
        return obj



