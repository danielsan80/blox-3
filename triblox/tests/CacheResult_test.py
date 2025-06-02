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
from triblox.caching.CachedResult import CachedResult
from cadquery import Workplane
import shutil
from pathlib import Path





def test_use_CacheResult():

    cache_dir = Path("tests/_test_step_cache")
    if cache_dir.exists():
        for step_file in cache_dir.glob("*.step"):
            step_file.unlink()

    class TestOwner:
        pass

    mosaic = Mosaic().add(Tile(0, 0)).add(Tile(1, 0))

    tolerance = 1e-6


    result1 = Workplane("XY")
    cache_base = CacheBase().add_owner(TestOwner()).add_mosaic(mosaic)
    cached_result = CachedResult(cache_base, result1, cache_dir="tests/_test_step_cache")

    assert cached_result.cache_key == CacheKey().add("TestOwner ").add("mosaic:0,0 ").add("mosaic:1,0 ")

    assert cached_result.has(mosaic.placed_tile(0,0)) == False

    result2 = result1.union(
        Workplane("XY")
        .circle(1)
        .extrude(1)
        .translate((0,0,0))
    )
    assert cached_result.add(mosaic.placed_tile(0,0), result2)

    assert cached_result.has(mosaic.placed_tile(1,0)) == False

    result3 = result2.union(
        Workplane("XY")
        .circle(1)
        .extrude(1)
        .translate((1,0,0))
    )

    assert cached_result.add(mosaic.placed_tile(1,0), result3)


    assert abs(cached_result.get().cut(result3).val().Volume()) < tolerance
    assert abs(result3.cut(cached_result.get()).val().Volume()) < tolerance

    result1 = Workplane("XY")
    cache_base = CacheBase().add_owner(TestOwner()).add_mosaic(mosaic)
    cached_result = CachedResult(cache_base, result1, cache_dir="tests/_test_step_cache")
    assert cached_result.cache_key == CacheKey().add("TestOwner ").add("mosaic:0,0 ").add("mosaic:1,0 ")

    assert cached_result.has(mosaic.placed_tile(0,0)) == True

    result2 = result1.union(
        Workplane("XY")
        .circle(1)
        .extrude(1)
        .translate((0,0,0))
    )

    assert cached_result.add(mosaic.placed_tile(0,0))

    assert cached_result.has(mosaic.placed_tile(1,0)) == True

    result3 = result2.union(
        Workplane("XY")
        .circle(1)
        .extrude(1)
        .translate((1,0,0))
    )

    assert cached_result.add(mosaic.placed_tile(1,0))

    assert abs(cached_result.get().cut(result3).val().Volume()) < tolerance
    assert abs(result3.cut(cached_result.get()).val().Volume()) < tolerance

