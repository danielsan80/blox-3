import sys
sys.path.append('src/')

import pytest
import re

from triblox.config import side, fix
from triblox.tile.Tile import Tile
from triblox.mosaic.MosaicBuilder import MosaicBuilder
from triblox.mosaic.Mosaic import Mosaic
from triblox.tile.Direction import Direction
from triblox.geometry.Point import Point
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
    builder = MosaicBuilder()

    assert  Mosaic() == builder.build()

def test_add_tile():
    builder = MosaicBuilder()

    builder = builder.tile(0,0)

    assert  Mosaic().add(Tile(0,0)) == builder.build()

def test_add_origin_tile():
    builder = MosaicBuilder()

    builder = builder.origin()

    assert  Mosaic().add(Tile(0,0)) == builder.build()

def test_move_current_and_add_here():
    builder = MosaicBuilder()

    builder = (
        builder
        .origin()
        .move(1,0)
        .here()
        .move(0,0)
        .here()
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(1,0))
    )

    assert  mosaic == builder.build()

def test_add_dirs():
    builder = MosaicBuilder()

    builder = (
        builder
        .origin()
        .right()
        .up()
        .left()
        .left()
        .down()
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(1,0))
        .add(Tile(1,1))
        .add(Tile(0,1))
        .add(Tile(-1,1))
        .add(Tile(-1,0))
    )

    assert  mosaic == builder.build()

def test_add_hex():
    builder = MosaicBuilder()

    builder = (
        builder
        .hex()
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(1,0))
        .add(Tile(1,1))
        .add(Tile(0,1))
        .add(Tile(-1,1))
        .add(Tile(-1,0))
    )

    assert  mosaic == builder.build()


def test_line_hor_zero():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_hor(0)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
    )

    assert  mosaic == builder.build()

def test_line_asc_zero():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_asc(0)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
    )

    assert  mosaic == builder.build()

def test_line_desc_zero():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_desc(0)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
    )

    assert  mosaic == builder.build()


def test_line_hor_positive():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_hor(5)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(1,0))
        .add(Tile(2,0))
        .add(Tile(3,0))
        .add(Tile(4,0))
        .add(Tile(5,0))
    )

    assert  mosaic == builder.build()

def test_line_hor_negative():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_hor(-5)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(-1,0))
        .add(Tile(-2,0))
        .add(Tile(-3,0))
        .add(Tile(-4,0))
        .add(Tile(-5,0))
    )

    assert  mosaic == builder.build()


def test_line_asc_positive():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_asc(5)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(1,0))
        .add(Tile(1,1))
        .add(Tile(2,1))
        .add(Tile(2,2))
        .add(Tile(3,2))
    )

    assert  mosaic == builder.build()

def test_line_asc_negative():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_asc(-5)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(0,-1))
        .add(Tile(-1,-1))
        .add(Tile(-1,-2))
        .add(Tile(-2,-2))
        .add(Tile(-2,-3))
    )

    assert  mosaic == builder.build()


def test_line_desc_positive():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_desc(5)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(0,-1))
        .add(Tile(1,-1))
        .add(Tile(1,-2))
        .add(Tile(2,-2))
        .add(Tile(2,-3))
    )

    assert  mosaic == builder.build()

def test_line_desc_negative():
    builder = MosaicBuilder()
    builder = (
        builder
        .origin()
        .line_desc(-5)
    )

    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(-1,0))
        .add(Tile(-1,1))
        .add(Tile(-2,1))
        .add(Tile(-2,2))
        .add(Tile(-3,2))
    )

    assert  mosaic == builder.build()
