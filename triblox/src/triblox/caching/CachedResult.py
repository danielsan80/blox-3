import sys

sys.path.append("../../src/")

from dataclasses import field
from pathlib import Path

from cadquery import Workplane, exporters, importers

from triblox.caching.CacheBase import CacheBase
from triblox.caching.CacheKey import CacheKey
from triblox.mosaic.PlacedTile import PlacedTile


class CachedResult:
    cache_key: CacheKey = field(init=False)
    result: Workplane = field(init=False)
    cache_dir: Path = field(init=False)
    last_cached_result_file: Path | None = field(init=False)

    def __init__(
        self,
        cache_base: CacheBase,
        initial_result: Workplane,
        cache_dir: str = "_step_cache",
    ):
        self.cache_key = cache_base.get()
        self.result = initial_result

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        self.last_cached_result_file = None

    def _cached_result_file(self, cache_key: CacheKey) -> Path:
        return self.cache_dir / f"{cache_key.hash()}.step"

    def _placed_tile_cache_key_part(self, placed_tile: PlacedTile) -> str:
        return "tile:" + str(placed_tile.tile.coord) + " "

    def has(self, placed_tile: PlacedTile) -> bool:
        cache_key = self.cache_key.add(self._placed_tile_cache_key_part(placed_tile))
        cached_result_file = self._cached_result_file(cache_key)
        return cached_result_file.exists()

    def add(
        self, placed_tile: PlacedTile, result: Workplane | None = None
    ) -> "CachedResult":
        self.cache_key = self.cache_key.add(
            self._placed_tile_cache_key_part(placed_tile)
        )
        cached_result_file = self._cached_result_file(self.cache_key)

        if result is None:
            assert (
                cached_result_file.exists()
            ), f"Cached result file {cached_result_file} does not exist."
            self.last_cached_result_file = cached_result_file
            return self

        self.last_cached_result_file = None
        self.result = result
        if not cached_result_file.exists():
            exporters.export(self.result, str(cached_result_file), exportType="STEP")

        return self

    def get(self) -> Workplane:
        if self.last_cached_result_file:
            return importers.importStep(str(self.last_cached_result_file))
        return self.result
