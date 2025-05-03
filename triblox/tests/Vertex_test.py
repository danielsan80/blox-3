import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.point.Point import Point
from triblox.helper.util import sin60
from triblox.tile.Tile import AdjacentTiles
from triblox.tile.Coord import Coord
from triblox.vertex.VertexHex import VertexHex
from triblox.tile.VertexPos import VertexPos
from triblox.vertex.Vertex import Vertex
from triblox.vertex.VertexOffset import VertexOffset
from triblox.vertex.VertexHexKey import VertexHexKey


import pytest
import re

def test_create_Vertex_for_center_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertexPos = VertexPos.C
    vertex = Vertex(tile, vertexPos)
    vertexHex = VertexHex(tile, vertexPos)

    assert vertex.tile == tile
    assert vertex.pos == vertexPos
    assert vertex.hex == vertexHex

    assert vertex.isMainPlaced() is True
    assert vertex.isLeftNearPlaced() is False
    assert vertex.isLeftFarPlaced() is False
    assert vertex.isRightNearPlaced() is False
    assert vertex.isRightFarPlaced() is False
    assert vertex.isOppositePlaced() is False

    assert vertex.offset() == VertexOffset.CENTER
    assert vertex.point() == tile.vertices.c
    assert vertex.movedPoints(clr) == [tile.vertices.c.move(tile.incenter, clr*2)]


def test_create_Vertex_for_left_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertexPos = VertexPos.C
    vertex = Vertex(tile, vertexPos)
    vertexHex = VertexHex(tile, vertexPos)

    vertex = vertex.markPlaced(VertexHexKey.LEFT_NEAR)

    assert vertex.tile == tile
    assert vertex.pos == vertexPos
    assert vertex.hex == vertexHex

    assert vertex.isMainPlaced() is True
    assert vertex.isLeftNearPlaced() is True
    assert vertex.isLeftFarPlaced() is False
    assert vertex.isRightNearPlaced() is False
    assert vertex.isRightFarPlaced() is False
    assert vertex.isOppositePlaced() is False

    assert vertex.offset() == VertexOffset.LEFT
    assert vertex.point() == tile.vertices.c
    assert vertex.movedPoints(clr) == [tile.vertices.c.move(tile.vertices.a, 1)]

def test_create_Vertex_for_right_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertexPos = VertexPos.C
    vertex = Vertex(tile, vertexPos)
    vertexHex = VertexHex(tile, vertexPos)

    vertex = vertex.markPlaced(VertexHexKey.RIGHT_NEAR)

    assert vertex.tile == tile
    assert vertex.pos == vertexPos
    assert vertex.hex == vertexHex

    assert vertex.isMainPlaced() is True
    assert vertex.isLeftNearPlaced() is False
    assert vertex.isLeftFarPlaced() is False
    assert vertex.isRightNearPlaced() is True
    assert vertex.isRightFarPlaced() is False
    assert vertex.isOppositePlaced() is False

    assert vertex.offset() == VertexOffset.RIGHT
    assert vertex.point() == tile.vertices.c
    assert vertex.movedPoints(clr) == [tile.vertices.c.move(tile.vertices.b, 1)]

def test_create_Vertex_for_split_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertexPos = VertexPos.C
    vertex = Vertex(tile, vertexPos)
    vertexHex = VertexHex(tile, vertexPos)

    vertex = (
        vertex.markPlaced(VertexHexKey.LEFT_NEAR)
        .markPlaced(VertexHexKey.RIGHT_NEAR)
    )

    assert vertex.tile == tile
    assert vertex.pos == vertexPos
    assert vertex.hex == vertexHex

    assert vertex.isMainPlaced() is True
    assert vertex.isLeftNearPlaced() is True
    assert vertex.isLeftFarPlaced() is False
    assert vertex.isRightNearPlaced() is True
    assert vertex.isRightFarPlaced() is False
    assert vertex.isOppositePlaced() is False

    assert vertex.offset() == VertexOffset.SPLIT
    assert vertex.point() == tile.vertices.c
    assert vertex.movedPoints(clr) == [
        tile.vertices.c.move(tile.vertices.a, 1),
        tile.vertices.c.move(tile.vertices.b, 1)
    ]
    assert not vertex.movedPoints(clr) == [
        tile.vertices.c.move(tile.vertices.b, 1),
        tile.vertices.c.move(tile.vertices.a, 1)
    ]

def test_create_Vertex_for_none_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertexPos = VertexPos.C
    vertex = Vertex(tile, vertexPos)
    vertexHex = VertexHex(tile, vertexPos)

    vertex = (
        vertex
        .markPlaced(VertexHexKey.LEFT_NEAR)
        .markPlaced(VertexHexKey.LEFT_FAR)
        .markPlaced(VertexHexKey.OPPOSITE)
        .markPlaced(VertexHexKey.RIGHT_FAR)
        .markPlaced(VertexHexKey.RIGHT_NEAR)
    )

    assert vertex.tile == tile
    assert vertex.pos == vertexPos
    assert vertex.hex == vertexHex

    assert vertex.isMainPlaced() is True
    assert vertex.isLeftNearPlaced() is True
    assert vertex.isLeftFarPlaced() is True
    assert vertex.isRightNearPlaced() is True
    assert vertex.isRightFarPlaced() is True
    assert vertex.isOppositePlaced() is True

    assert vertex.offset() == VertexOffset.NONE
    assert vertex.point() == tile.vertices.c
    assert vertex.movedPoints(clr) == [
        tile.vertices.c
    ]





