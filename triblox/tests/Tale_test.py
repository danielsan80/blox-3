import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.point.Point import Point
from triblox.helper.util import sin60
from triblox.tile.Tile import AdjacentTiles
from triblox.tile.Coord import Coord
import pytest
import re

def test_Tile_coordinates_system():
    tiles = [
        Tile(0, 0),
        Tile(1, 0),
        Tile(-1, 0),
        Tile(1, 1),
        Tile(0, 1),
        Tile(-1, 1),

        Tile(100, 100),
        Tile(101, 100),
    ]

    expectedData = [
        (Direction.up(), Point(0,0), Point(side,0), Point(side/2,sin60*side), Point(side/2,sin60/3*side)),
        (Direction.down(), Point(3/2*side,sin60*side), Point(side/2,sin60*side), Point(side,0), Point(side,sin60/3*2*side)),
        (Direction.down(), Point(side/2,sin60*side), Point(-side/2,sin60*side), Point(0,0), Point(0,sin60/3*2*side)),
        (Direction.up(), Point(side/2,sin60*side), Point(3/2*side,sin60*side), Point(side,sin60*2*side), Point(side,side*sin60*4/3)),
        (Direction.down(), Point(side,sin60*2*side), Point(0,sin60*2*side), Point(side/2,sin60*side), Point(side/2,side*sin60*5/3)),
        (Direction.up(), Point(-side/2,sin60*side), Point(side/2,sin60*side), Point(0,sin60*2*side), Point(0,side*sin60*4/3)),

        (Direction.up(), Point(50*side,sin60*100*side), Point(51*side,sin60*100*side), Point(50.5*side,sin60*101*side), Point(50.5*side,side*sin60*301/3)),
        (Direction.down(), Point(51.5*side,sin60*101*side), Point(50.5*side,sin60*101*side), Point(51*side,sin60*100*side), Point(51*side,side*sin60*302/3)),
    ]

    for i, tile in enumerate(tiles):
        data = (tile.direction, tile.vertices.a, tile.vertices.b, tile.vertices.c, tile.incenter)
        assert expectedData[i] == data


def test_Tile_adjacency():
    assert Tile(0, 0).adjacentTiles == AdjacentTiles(Tile(0, -1), Tile(1, 0), Tile(-1, 0))
    assert Tile(1, 0).adjacentTiles == AdjacentTiles(Tile(1, 1), Tile(0, 0), Tile(2, 0))

    assert Tile(0,0).isAdjacent(Tile(0, -1))
    assert not Tile(0,0).isAdjacent(Tile(2, 0))
    with pytest.raises(ValueError, match=re.escape(f"The given tile is the same")):
        Tile(0,0).isAdjacent(Tile(0, 0))

