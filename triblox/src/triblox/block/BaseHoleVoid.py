import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.caching.CacheBase import CacheBase
from triblox.caching.CachedResult import CachedResult
from triblox.config import base_hole_margin, clr, stub_h, taper_h, wall_w
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class BaseHoleVoid:
    mosaic: Mosaic

    def get(self) -> Workplane:
        result = Workplane("XY")

        cache_base = CacheBase().add_owner(self).add_mosaic(self.mosaic)
        cached_result = CachedResult(cache_base, result)

        for placed_tile in self.mosaic.placed_tiles.values():
            if cached_result.has(placed_tile):
                cached_result.add(placed_tile)
                continue
            result = cached_result.get()
            result = result.union(self._tile_base_hole_void(placed_tile))
            cached_result.add(placed_tile)

        result = cached_result.get()
        return result

    def _tile_base_hole_void(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.centered_points(clr + wall_w + base_hole_margin)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)

        result = (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(wall_w)
            .translate((0, 0, -taper_h - stub_h))
        )

        return result
