import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.mosaic.PlacedVertices import PlacedVertices
from triblox.tile.Tile import Tile


@dataclass(frozen=True)
class PlacedTile:
    tile: Tile
    vertices: PlacedVertices
