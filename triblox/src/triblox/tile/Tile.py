import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.config import side
from triblox.geometry.Point import Point
from triblox.helper.util import sin60
from triblox.tile.Coord import Coord
from triblox.tile.Direction import Direction
from triblox.tile.Vertices import Vertices


@dataclass(frozen=True)
class AdjacentTiles:
    ab: "Tile"
    bc: "Tile"
    ca: "Tile"

    def to_list(self) -> list["Tile"]:
        return [self.ab, self.bc, self.ca]


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
        if self.direction.is_up():
            a = Point(self.x / 2 * side, self.y * sin60 * side)
            b = Point(a.x + side, a.y)
            c = Point(a.x + side / 2, (self.y + 1) * sin60 * side)
        elif self.direction.is_down():
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
    def adjacent_tiles(self) -> AdjacentTiles:
        if self.direction.is_up():
            ab = self.down()
            bc = self.right()
            ca = self.left()
        elif self.direction.is_down():
            ab = self.up()
            bc = self.left()
            ca = self.right()
        else:
            raise ValueError("This should never happen")
        return AdjacentTiles(ab, bc, ca)

    def is_adjacent(self, tile: "Tile") -> bool:
        if tile.coord == self.coord:
            raise ValueError("The given tile is the same")
        if tile.coord == self.adjacent_tiles.ab.coord:
            return True
        if tile.coord == self.adjacent_tiles.bc.coord:
            return True
        if tile.coord == self.adjacent_tiles.ca.coord:
            return True
        return False

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
