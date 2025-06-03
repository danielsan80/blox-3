import sys

sys.path.append("../../src/")

from dataclasses import dataclass, field
from typing import Tuple

from cadquery import Sketch, Workplane

from triblox.caching.CacheBase import CacheBase
from triblox.caching.CachedResult import CachedResult
from triblox.config import stub_h, taper_h
from triblox.helper.util import sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class CustomGridVoid:
    mosaics: Tuple[Mosaic] = field(default_factory=tuple)

    def add(self, mosaic: Mosaic) -> "CustomGridVoid":
        return CustomGridVoid(self.mosaics + (mosaic,))

    def get(self) -> Workplane:
        result = Workplane("XY")

        cache_base = CacheBase().add_owner(self)

        for mosaic in self.mosaics:
            cache_base = cache_base.add_mosaic(mosaic)

            cached_result = CachedResult(cache_base, result)

            for placed_tile in mosaic.placed_tiles.values():
                if cached_result.has(placed_tile):
                    cached_result.add(placed_tile)
                    continue
                result = cached_result.get()
                result = result.union(self._taper_void(placed_tile))
                result = result.union(self._stub_void(placed_tile))
                cached_result.add(placed_tile, result)

            result = cached_result.get()

        return result

    def _taper_void(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.original_points()
        points = [point.to_tuple() for point in points]
        up = Sketch().polygon(points)

        points = placed_tile.vertices.offset_points(taper_h * sin30)
        points = [point.to_tuple() for point in points]
        down = Sketch().polygon(points)

        wp_up = Workplane("XY").placeSketch(up)

        wp_down = Workplane("XY").transformed(offset=(0, 0, -taper_h)).placeSketch(down)

        return wp_up.add(wp_down).loft(combine=True)

    def _stub_void(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.offset_points(taper_h * sin30)
        points = [point.to_tuple() for point in points]
        down = Sketch().polygon(points)

        return (
            Workplane("XY")
            .transformed(offset=(0, 0, -taper_h - stub_h))
            .placeSketch(down)
            .extrude(stub_h)
        )
