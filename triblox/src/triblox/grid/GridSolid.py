import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.caching.CacheBase import CacheBase
from triblox.caching.CachedResult import CachedResult
from triblox.config import clr, h_clr, h_grid_fix, stub_h, taper_h
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class GridSolid:
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
            result = result.union(self._solid(placed_tile))
            cached_result.add(placed_tile, result)

        result = cached_result.get()

        return result

    def _solid(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.offset_points(clr)
        points = [point.to_tuple() for point in points]

        triangle = Sketch().polygon(points)
        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(taper_h + stub_h - h_clr + h_grid_fix)
            .translate((0, 0, -taper_h - stub_h))
        )
