import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.geometry.Point import Point
from triblox.helper.util import dsin
from triblox.caching.CacheKey import CacheKey
from triblox.caching.CacheBase import CacheBase
import hashlib
from triblox.mosaic.Mosaic import Mosaic



def test_empty_cache_base():
    cache_base = CacheBase()

    assert cache_base.get() == CacheKey()

def test_add_owner():
    cache_base = CacheBase()
    class TestOwner:
        pass

    cache_base = cache_base.add_owner(TestOwner())

    assert cache_base.get() == CacheKey().add("TestOwner ")

def test_add_mosaic():
    cache_base = CacheBase()
    mosaic = (
        Mosaic()
        .add(Tile(0,0))
        .add(Tile(1,0))
    )

    assert  cache_base.add_mosaic(mosaic).get() == (
        CacheKey()
        .add("mosaic:0,0 ")
        .add("mosaic:1,0 ")
    )

    assert  cache_base.add_mosaic(mosaic, "M").get() == (
        CacheKey()
        .add("M:0,0 ")
        .add("M:1,0 ")
    )

def test_add():
    cache_base = CacheBase()

    assert cache_base.add("key1", "value1").get() == CacheKey().add("key1:value1 ")

