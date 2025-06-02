import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.geometry.Point import Point
from triblox.helper.util import dsin
from triblox.caching.CacheKey import CacheKey
import hashlib

def test_empty_cache_key():
    cache_key = CacheKey()

    assert str(cache_key) == ""


def test_you_can_add_a_part():
    cache_key = CacheKey()
    cache_key = cache_key.add("a part")

    assert str(cache_key) == "a part"

    cache_key = cache_key.add("another part")
    assert str(cache_key) == "a part_another part"


def test_you_can_add_several_parts():
    cache_key = CacheKey()
    cache_key = cache_key.add(("part1", "part2", "part3"))

    assert str(cache_key) == "part1_part2_part3"

def test_hashing():
    cache_key = CacheKey()
    cache_key = cache_key.add("test")

    assert "test" == str(cache_key)
    assert b"test" == str(cache_key).encode()
    assert hashlib.sha256(str("test").encode()).hexdigest() == cache_key.hash()
    assert "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" == cache_key.hash()
