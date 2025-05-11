import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.geometry.Point import Point
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
    vertex_pos = VertexPos.C
    vertex = Vertex(tile, vertex_pos)
    vertex_hex = VertexHex(tile, vertex_pos)

    assert vertex.tile == tile
    assert vertex.pos == vertex_pos
    assert vertex.hex == vertex_hex

    assert vertex.is_main_placed() is True
    assert vertex.is_left_near_placed() is False
    assert vertex.is_left_far_placed() is False
    assert vertex.is_right_near_placed() is False
    assert vertex.is_right_far_placed() is False
    assert vertex.is_opposite_placed() is False

    assert vertex.offset() == VertexOffset.CENTER
    assert vertex.point() == tile.vertices.c
    assert vertex.offset_points(clr) == [tile.vertices.c.move(tile.incenter, clr*2)]


def test_create_Vertex_for_left_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertex_pos = VertexPos.C
    vertex = Vertex(tile, vertex_pos)
    vertex_hex = VertexHex(tile, vertex_pos)

    vertex = vertex.mark_placed(VertexHexKey.LEFT_NEAR)

    assert vertex.tile == tile
    assert vertex.pos == vertex_pos
    assert vertex.hex == vertex_hex

    assert vertex.is_main_placed() is True
    assert vertex.is_left_near_placed() is True
    assert vertex.is_left_far_placed() is False
    assert vertex.is_right_near_placed() is False
    assert vertex.is_right_far_placed() is False
    assert vertex.is_opposite_placed() is False

    assert vertex.offset() == VertexOffset.LEFT
    assert vertex.point() == tile.vertices.c
    assert vertex.offset_points(clr) == [tile.vertices.c.move(tile.vertices.a, 1)]

def test_create_Vertex_for_right_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertex_pos = VertexPos.C
    vertex = Vertex(tile, vertex_pos)
    vertex_hex = VertexHex(tile, vertex_pos)

    vertex = vertex.mark_placed(VertexHexKey.RIGHT_NEAR)

    assert vertex.tile == tile
    assert vertex.pos == vertex_pos
    assert vertex.hex == vertex_hex

    assert vertex.is_main_placed() is True
    assert vertex.is_left_near_placed() is False
    assert vertex.is_left_far_placed() is False
    assert vertex.is_right_near_placed() is True
    assert vertex.is_right_far_placed() is False
    assert vertex.is_opposite_placed() is False

    assert vertex.offset() == VertexOffset.RIGHT
    assert vertex.point() == tile.vertices.c
    assert vertex.offset_points(clr) == [tile.vertices.c.move(tile.vertices.b, 1)]

def test_create_Vertex_for_split_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertex_pos = VertexPos.C
    vertex = Vertex(tile, vertex_pos)
    vertex_hex = VertexHex(tile, vertex_pos)

    vertex = (
        vertex.mark_placed(VertexHexKey.LEFT_NEAR)
        .mark_placed(VertexHexKey.RIGHT_NEAR)
    )

    assert vertex.tile == tile
    assert vertex.pos == vertex_pos
    assert vertex.hex == vertex_hex

    assert vertex.is_main_placed() is True
    assert vertex.is_left_near_placed() is True
    assert vertex.is_left_far_placed() is False
    assert vertex.is_right_near_placed() is True
    assert vertex.is_right_far_placed() is False
    assert vertex.is_opposite_placed() is False

    assert vertex.offset() == VertexOffset.SPLIT
    assert vertex.point() == tile.vertices.c
    assert vertex.offset_points(clr) == [
        tile.vertices.c.move(tile.vertices.b, 1),
        tile.vertices.c.move(tile.vertices.a, 1),
    ]
    assert not vertex.offset_points(clr) == [
        tile.vertices.c.move(tile.vertices.a, 1),
        tile.vertices.c.move(tile.vertices.b, 1),
    ]

def test_create_Vertex_for_none_offset():
    clr = sin60
    tile = Tile(0, 0)
    vertex_pos = VertexPos.C
    vertex = Vertex(tile, vertex_pos)
    vertex_hex = VertexHex(tile, vertex_pos)

    vertex = (
        vertex
        .mark_placed(VertexHexKey.LEFT_NEAR)
        .mark_placed(VertexHexKey.LEFT_FAR)
        .mark_placed(VertexHexKey.OPPOSITE)
        .mark_placed(VertexHexKey.RIGHT_FAR)
        .mark_placed(VertexHexKey.RIGHT_NEAR)
    )

    assert vertex.tile == tile
    assert vertex.pos == vertex_pos
    assert vertex.hex == vertex_hex

    assert vertex.is_main_placed() is True
    assert vertex.is_left_near_placed() is True
    assert vertex.is_left_far_placed() is True
    assert vertex.is_right_near_placed() is True
    assert vertex.is_right_far_placed() is True
    assert vertex.is_opposite_placed() is True

    assert vertex.offset() == VertexOffset.NONE
    assert vertex.point() == tile.vertices.c
    assert vertex.offset_points(clr) == [
        tile.vertices.c
    ]





