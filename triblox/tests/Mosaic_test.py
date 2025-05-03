import sys
sys.path.append('src/')

import pytest
import re

from triblox.config import side
from triblox.tile.Tile import Tile
from triblox.mosaic.Mosaic import Mosaic
from triblox.tile.Direction import Direction
from triblox.point.Point import Point
from triblox.helper.util import sin60
from triblox.tile.Coord import Coord
from triblox.vertex.VertexHex import VertexHex
from triblox.mosaic.PlacedVertices import PlacedVertices
from triblox.tile.VertexPos import VertexPos
from triblox.mosaic.PlacedTile import PlacedTile
from triblox.vertex.VertexOffset import VertexOffset
from triblox.vertex.Vertex import Vertex
from triblox.vertex.VertexHexKey import VertexHexKey




def test_empty_Mosaic():
    mosaic = Mosaic()

    assert mosaic.tiles == dict()


def test_add_tile():
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile)

    assert len(mosaic.tiles) == 1
    assert mosaic.tiles[str(tile.coord)] == tile

def test_add_multiple_tiles():
    tile1 = Tile(0, 0)
    tile2 = Tile(1, 0)
    mosaic = Mosaic().add(tile1).add(tile2)

    assert len(mosaic.tiles) == 2
    assert mosaic.tiles[str(tile1.coord)] == tile1
    assert mosaic.tiles[str(tile2.coord)] == tile2

def test_empty_mosaic():
    mosaic = Mosaic()

    assert mosaic.isEmpty() is True

    mosaic = mosaic.add(Tile(0, 0))

    assert mosaic.isEmpty() is False

def test_mosaic_contains_tile():
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile)

    assert mosaic.contains(tile) is True
    assert mosaic.contains(Tile(1, 0)) is False

def test_is_adjacent():
    tile1 = Tile(0, 0)
    tile2 = Tile(1, 0)
    tile3 = Tile(2, 2)
    mosaic = Mosaic().add(Tile(0, 0))

    assert mosaic.isAdjacent(Tile(1, 0)) is True
    assert mosaic.isAdjacent(Tile(2, 2)) is False

    with pytest.raises(ValueError, match=re.escape(f"The tile {Tile(0,0)} is already in the mosaic")):
        mosaic.isAdjacent(Tile(0, 0))


def test_error_when_add_tile_already_in_mosaic():
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile)

    with pytest.raises(ValueError, match=re.escape(f"The mosaic already contains the tile {tile}")):
        mosaic.add(tile)

def test_error_when_add_tile_not_adjacent():
    tile1 = Tile(0, 0)
    tile2 = Tile(2, 2)
    mosaic = Mosaic().add(tile1)

    with pytest.raises(ValueError, match=re.escape(f"The tile {tile2} is not adjacent to any tile in the mosaic")):
        mosaic.add(tile2)

def test_get_VertexHex():
    mosaic = Mosaic().add(Tile(0, 0)).add(Tile(1, 0))

    assert len(mosaic.placedTiles) == 2

    hex = mosaic.placedTile(0, 0).vertices.c.hex

    assert mosaic.contains(hex.main)
    assert not mosaic.contains(hex.leftNear)
    assert not mosaic.contains(hex.leftFar)
    assert mosaic.contains(hex.rightNear)
    assert not mosaic.contains(hex.rightFar)
    assert not mosaic.contains(hex.opposite)

    hex = mosaic.placedTile(0, 0).vertices.a.hex

    assert mosaic.contains(hex.main)
    assert not mosaic.contains(hex.leftNear)
    assert not mosaic.contains(hex.leftFar)
    assert not mosaic.contains(hex.rightNear)
    assert not mosaic.contains(hex.rightFar)
    assert not mosaic.contains(hex.opposite)

    hex = mosaic.placedTile(0, 0).vertices.b.hex

    assert mosaic.contains(hex.main)
    assert mosaic.contains(hex.leftNear)
    assert not mosaic.contains(hex.leftFar)
    assert not mosaic.contains(hex.rightNear)
    assert not mosaic.contains(hex.rightFar)
    assert not mosaic.contains(hex.opposite)


def test_tile_vertice_offset_center():
    clr = sin60
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile)

    assert mosaic.placedTile(0,0).vertices.a == Vertex(tile, VertexPos.A)
    assert mosaic.placedTile(0,0).vertices.b == Vertex(tile, VertexPos.B)
    assert mosaic.placedTile(0,0).vertices.c == Vertex(tile, VertexPos.C)

    assert mosaic.placedTile(0,0).vertices.a.movedPoints(clr) == [Point(1.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.b.movedPoints(clr) == [Point(side-1.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.c.movedPoints(clr) == [Point(side/2,side*sin60-sin60*2)]

def test_tile_vertice_offset_left_and_right():
    clr = sin60
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile).add(Tile(1,0))

    assert mosaic.placedTile(0,0).vertices.a == Vertex(tile, VertexPos.A)
    assert mosaic.placedTile(0,0).vertices.b == Vertex(tile, VertexPos.B).markPlaced(VertexHexKey.LEFT_NEAR)
    assert mosaic.placedTile(0,0).vertices.c == Vertex(tile, VertexPos.C).markPlaced(VertexHexKey.RIGHT_NEAR)

    assert mosaic.placedTile(0,0).vertices.a.movedPoints(clr) == [Point(1.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.b.movedPoints(clr) == [Point(side-0.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.c.movedPoints(clr) == [Point(side/2+0.5,side*sin60-sin60)]


def test_tile_vertice_offset_left_right_and_split():
    clr = sin60
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile).add(Tile(1,0)).add(Tile(-1,0)).add(Tile(-1,1)).add(Tile(0,1))

    assert mosaic.placedTile(0,0).vertices.a == Vertex(tile, VertexPos.A).markPlaced(VertexHexKey.RIGHT_NEAR)
    assert mosaic.placedTile(0,0).vertices.b == Vertex(tile, VertexPos.B).markPlaced(VertexHexKey.LEFT_NEAR)
    assert mosaic.placedTile(0,0).vertices.c == Vertex(tile, VertexPos.C).markPlaced(VertexHexKey.RIGHT_NEAR).markPlaced(VertexHexKey.LEFT_NEAR).markPlaced(VertexHexKey.LEFT_FAR).markPlaced(VertexHexKey.OPPOSITE)

    assert mosaic.placedTile(0,0).vertices.a.movedPoints(clr) == [Point(0.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.b.movedPoints(clr) == [Point(side-0.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.c.movedPoints(clr) == [
        Point(side/2-0.5,side*sin60-sin60),
        Point(side/2+0.5,side*sin60-sin60),
    ]

def test_tile_vertice_offset_none():
    clr = sin60
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile).add(Tile(1,0)).add(Tile(-1,0)).add(Tile(-1,1)).add(Tile(0,1)).add(Tile(1,1))

    assert mosaic.placedTile(0,0).vertices.a == Vertex(tile, VertexPos.A).markPlaced(VertexHexKey.RIGHT_NEAR)
    assert mosaic.placedTile(0,0).vertices.b == Vertex(tile, VertexPos.B).markPlaced(VertexHexKey.LEFT_NEAR)
    assert mosaic.placedTile(0,0).vertices.c == Vertex(tile, VertexPos.C).markPlaced(VertexHexKey.RIGHT_NEAR).markPlaced(VertexHexKey.LEFT_NEAR).markPlaced(VertexHexKey.LEFT_FAR).markPlaced(VertexHexKey.RIGHT_FAR).markPlaced(VertexHexKey.OPPOSITE)

    assert mosaic.placedTile(0,0).vertices.a.movedPoints(clr) == [Point(0.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.b.movedPoints(clr) == [Point(side-0.5,sin60)]
    assert mosaic.placedTile(0,0).vertices.c.movedPoints(clr) == [Point(side/2,side*sin60)]
