from dataclasses import dataclass
from typing import List, Tuple
from tiles.tile.TileCoord import TileCoord


class TileArea:
    coords: List[TileCoord]

    def __init__(self, coords: List[TileCoord]):
        self.coords = coords
        for i in range(len(coords)):
            print(f"Elemento {i}: {fruits[i]}")