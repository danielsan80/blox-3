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


from typing import Dict


@dataclass(frozen=True)
class Tile:
    x: int
    y: int

    @property
    def coord(self) -> Coord:
        return Coord(self.x, self.y)

    @property
    def direction(self) -> Direction:
        if (self.x + self.y) % 2 == 0:
            return Direction.up()
        else:
            return Direction.down()

    @property
    def vertices(self) -> Vertices:
        if self.direction.isUp():
            a = Point(self.x / 2 * side, self.y * sin60 * side)
            b = Point(a.x + side, a.y)
            c = Point(a.x + side / 2, (self.y + 1) * sin60 * side)
        elif self.direction.isDown():
            a = Point((0.5 + (self.x + 1) / 2) * side, (self.y + 1) * sin60 * side)
            b = Point(a.x - side, a.y)
            c = Point(a.x - side / 2, self.y * sin60 * side)
        else:
            raise ValueError("This should never happen")

        return Vertices(a, b, c)

    @property
    def incenter(self) -> Point:
        vertices = self.vertices
        return Point(
            (vertices.a.x + vertices.b.x + vertices.c.x) / 3,
            (vertices.a.y + vertices.b.y + vertices.c.y) / 3,
        )

    @property
    def adjacentTiles(self) -> AdjacentCoords:
        if self.direction.isUp():
            asdf = Tile(0, 0)
            ab = Coord(self.x, self.y - 1)
            bc = Coord(self.x + 1, self.y)
            ca = Coord(self.x - 1, self.y)
        elif self.direction.isDown():
            ab = Coord(self.x, self.y + 1)
            bc = Coord(self.x - 1, self.y)
            ca = Coord(self.x + 1, self.y)
        else:
            raise ValueError("This should never happen")
        return AdjacentCoords(ab, bc, ca)

    def isAdjacent(self, tile: "Tile") -> bool:
        if tile.coord == self.coord:
            raise ValueError("The given tile is the same")
        if tile.coord == self.adjacentTiles.ab:
            return True
        if tile.coord == self.adjacentTiles.bc:
            return True
        if tile.coord == self.adjacentTiles.ca:
            return True
        return False

    def isUp(self) -> bool:
        return self.direction.isUp()

    def isDown(self) -> bool:
        return self.direction.isDown()

    def up(self) -> "Tile":
        return Tile(self.x, self.y + 1)

    def down(self) -> "Tile":
        return Tile(self.x, self.y - 1)

    def left(self) -> "Tile":
        return Tile(self.x - 1, self.y)

    def right(self) -> "Tile":
        return Tile(self.x + 1, self.y)

    def move(self, x: int, y: int) -> "Tile":
        return Tile(self.x + x, self.y + y)