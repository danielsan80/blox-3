import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.geometry.Point import Point
from triblox.helper.util import sin60
from triblox.tile.Coord import Coord
from triblox.vertex.VertexHex import VertexHex
from triblox.tile.VertexPos import VertexPos

import pytest
import re

def test_up_a():
    tile = Tile(0, 0)

    vertex_hex = VertexHex(tile, VertexPos.A)

    actual = [
        vertex_hex.main,
        vertex_hex.left_near,
        vertex_hex.left_far,
        vertex_hex.opposite,
        vertex_hex.right_far,
        vertex_hex.right_near,
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

    vertex_hex = VertexHex(tile, VertexPos.B)

    actual = [
        vertex_hex.main,
        vertex_hex.left_near,
        vertex_hex.left_far,
        vertex_hex.opposite,
        vertex_hex.right_far,
        vertex_hex.right_near,
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

    vertex_hex = VertexHex(tile, VertexPos.C)

    actual = [
        vertex_hex.main,
        vertex_hex.left_near,
        vertex_hex.left_far,
        vertex_hex.opposite,
        vertex_hex.right_far,
        vertex_hex.right_near,
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

    vertex_hex = VertexHex(tile, VertexPos.A)


    actual = [
        vertex_hex.main,
        vertex_hex.left_near,
        vertex_hex.left_far,
        vertex_hex.opposite,
        vertex_hex.right_far,
        vertex_hex.right_near,
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

    vertex_hex = VertexHex(tile, VertexPos.B)


    actual = [
        vertex_hex.main,
        vertex_hex.left_near,
        vertex_hex.left_far,
        vertex_hex.opposite,
        vertex_hex.right_far,
        vertex_hex.right_near,
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

    vertex_hex = VertexHex(tile, VertexPos.C)


    actual = [
        vertex_hex.main,
        vertex_hex.left_near,
        vertex_hex.left_far,
        vertex_hex.opposite,
        vertex_hex.right_far,
        vertex_hex.right_near,
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


