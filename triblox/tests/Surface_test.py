import sys
sys.path.append('src/')

import pytest
import re

from triblox.config import side
from triblox.tile.Tile import Tile
from triblox.tile.Surface import Surface
from triblox.tile.Direction import Direction
from triblox.point.Point import Point
from triblox.helper.util import sin60

def test_you_MUST_use_create_to_init_a_Surface():
    with pytest.raises(RuntimeError, match=re.escape("Use Surface.create() instead of Surface()")):
        Surface()

def test_empty_Surface():
    surface = Surface.create()

    assert surface.tiles == tuple()



