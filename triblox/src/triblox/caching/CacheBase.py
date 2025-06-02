import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from triblox.caching.CacheKey import CacheKey
from triblox.mosaic.Mosaic import Mosaic


@dataclass(frozen=True)
class CacheBase:
    cache_key: CacheKey = CacheKey()

    def add_owner(self, object: object) -> "CacheBase":
        return CacheBase(self.cache_key.add(object.__class__.__name__ + " "))

    def add_mosaic(self, mosaic: Mosaic, key: str = "mosaic") -> "CacheBase":
        parts = ()
        for placed_tile in mosaic.placed_tiles.values():
            parts += (key + ":" + str(placed_tile.tile.coord) + " ",)
        return CacheBase(self.cache_key.add(parts))

    def add(self, key: str, value: str) -> "CacheBase":
        return CacheBase(self.cache_key.add(key + ":" + str(value) + " "))

    def get(self) -> CacheKey:
        return self.cache_key
