import sys
sys.path.append('src/')

import pytest
import re

from triblox.config import side
from triblox.tile.Tile import Tile
from triblox.tile.Mosaic import Mosaic
from triblox.tile.Direction import Direction
from triblox.point.Point import Point
from triblox.helper.util import sin60

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

def test_add_tile_already_in_mosaic():
    tile = Tile(0, 0)
    mosaic = Mosaic().add(tile)

    with pytest.raises(ValueError, match=re.escape(f"The mosaic already contains the tile {tile}")):
        mosaic.add(tile)

def test_add_tile_not_adjacent():
    tile1 = Tile(0, 0)
    tile2 = Tile(2, 2)
    mosaic = Mosaic().add(tile1)

    with pytest.raises(ValueError, match=re.escape(f"The tile {tile2} is not adjacent to any tile in the mosaic")):
        mosaic.add(tile2)