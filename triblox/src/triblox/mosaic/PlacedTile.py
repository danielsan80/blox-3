import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.config import side
from triblox.helper.util import sin60
from triblox.point.Point import Point
from triblox.tile.Coord import Coord
from triblox.tile.Direction import Direction
from triblox.tile.Vertices import Vertices
from triblox.tile.AdjacentCoords import AdjacentCoords
from triblox.tile.Tile import Tile


from typing import Dict

@dataclass(frozen=True)
class PlacedTile:
    tile: Tile

    def vertexHexes(self) -> VertexHexes:
        a = VertexHex(self.tile)