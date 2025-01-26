from dataclasses import dataclass
from typing import List, Tuple
from tiles.tile.TileCoord import TileCoord
from tiles.geometry.Point import Point

def roundGet(list: List, i: int):
    if 0 <= i < len(list):
        return list[i]
    else:
        return list[(i+len(list)) % len(list)]

class TileAreaSection:
    dir: Dir
    length: int
    start: TileCoord
    offset: Offset
    turn: Turn

    def __init__(self, dir: Dir, length: int, start: TileCoord, offset: Offset, turn: Turn):

        # asserisci che length sia maggiore di 0
        assert length > 0, "Length must be greater than 0"

        self.dir = dir
        self.length = length
        self.start = start
        self.offset = offset
        self.turn = turn


class TileArea:
    coords: List[TileCoord]

    def rawSection(self, i: int):
        p1 = roundGet(self.coords, i+1)
        p0 = roundGet(self.coords, i)
        dir = Point(p1.x - p0.x, p1.y - p0.y)

        north = dir.x == 0 and dir.y > 0
        south = dir.x == 0 and dir.y < 0
        east = dir.y == 0 and dir.x > 0
        west = dir.y == 0 and dir.x < 0

        if north:
            return "north"
        if south:
            return "south"
        if east:
            return "east"
        if west:
            return "west"


    def __init__(self, coords: List[TileCoord]):
        self.coords = coords
        for i in range(len(coords)):
            print(f"Elemento {i}: {coords[i]}")
            print(f"Section {i}: {self.rawSection(i)}")
            print("")
