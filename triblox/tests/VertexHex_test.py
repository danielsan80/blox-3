import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.point.Point import Point
from triblox.helper.util import sin60
from triblox.tile.Coord import Coord
from triblox.mosaic.VertexHex import VertexHex
from triblox.tile.VertexPos import VertexPos

import pytest
import re

def test_up_a():
    tile = Tile(0, 0)

    vertexHex = VertexHex(tile, VertexPos.A)

    actual = [
        vertexHex.main,
        vertexHex.leftNear,
        vertexHex.leftFar,
        vertexHex.opposite,
        vertexHex.rightFar,
        vertexHex.rightNear,
    ]

    expected = [
        Tile(0, 0),
        Tile(0, -1),
        Tile(-1, -1),
        Tile(-2, -1),
        Tile(-2, 0),
        Tile(-1, 0),
    ]

    assert actual == expected

def test_up_b():
    tile = Tile(0, 0)

    vertexHex = VertexHex(tile, VertexPos.B)

    actual = [
        vertexHex.main,
        vertexHex.leftNear,
        vertexHex.leftFar,
        vertexHex.opposite,
        vertexHex.rightFar,
        vertexHex.rightNear,
    ]

    expected = [
        Tile(0, 0),
        Tile(1, 0),
        Tile(2, 0),
        Tile(2, -1),
        Tile(1, -1),
        Tile(0, -1),
    ]

    assert actual == expected


def test_up_c():
    tile = Tile(0, 0)

    vertexHex = VertexHex(tile, VertexPos.C)

    actual = [
        vertexHex.main,
        vertexHex.leftNear,
        vertexHex.leftFar,
        vertexHex.opposite,
        vertexHex.rightFar,
        vertexHex.rightNear,
    ]

    expected = [
        Tile(0, 0),
        Tile(-1, 0),
        Tile(-1, 1),
        Tile(0, 1),
        Tile(1, 1),
        Tile(1, 0),
    ]

    assert actual == expected

def test_down_a():
    tile = Tile(1, 0)

    vertexHex = VertexHex(tile, VertexPos.A)


    actual = [
        vertexHex.main,
        vertexHex.leftNear,
        vertexHex.leftFar,
        vertexHex.opposite,
        vertexHex.rightFar,
        vertexHex.rightNear,
    ]

    expected = [
        Tile(1, 0),
        Tile(1, 1),
        Tile(2, 1),
        Tile(3, 1),
        Tile(3, 0),
        Tile(2, 0),
    ]

    assert actual == expected

def test_down_b():
    tile = Tile(1, 0)

    vertexHex = VertexHex(tile, VertexPos.B)


    actual = [
        vertexHex.main,
        vertexHex.leftNear,
        vertexHex.leftFar,
        vertexHex.opposite,
        vertexHex.rightFar,
        vertexHex.rightNear,
    ]

    expected = [
        Tile(1, 0),
        Tile(0, 0),
        Tile(-1, 0),
        Tile(-1, 1),
        Tile(0, 1),
        Tile(1, 1),
    ]

    assert actual == expected

def test_down_c():
    tile = Tile(1, 0)

    vertexHex = VertexHex(tile, VertexPos.C)


    actual = [
        vertexHex.main,
        vertexHex.leftNear,
        vertexHex.leftFar,
        vertexHex.opposite,
        vertexHex.rightFar,
        vertexHex.rightNear,
    ]

    expected = [
        Tile(1, 0),
        Tile(2, 0),
        Tile(2, -1),
        Tile(1, -1),
        Tile(0, -1),
        Tile(0, 0),
    ]

    assert actual == expected


