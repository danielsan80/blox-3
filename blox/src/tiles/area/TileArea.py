from dataclasses import dataclass
from typing import List, Tuple
from tiles.tile.TileCoord import TileCoord


class TileArea:
    coords: List[TileCoord]

    def __init__(self, coords: List[TileCoord]):
        self.coords = coords