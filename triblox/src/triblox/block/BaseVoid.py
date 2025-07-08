import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.caching.CacheBase import CacheBase
from triblox.caching.CachedResult import CachedResult
from triblox.config import clr, stub_h, taper_h, wall_w
from triblox.helper.util import sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class BaseVoid:
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
            result = result.union(self._taper_void(placed_tile))
            result = result.union(self._stub_void(placed_tile))
            cached_result.add(placed_tile, result)
        result = cached_result.get()

        return result

    def _taper_void(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.centered_points(clr + wall_w)
        points = [point.to_tuple() for point in points]
        base_top = Sketch().polygon(points)

        points = placed_tile.vertices.centered_points(clr + wall_w + taper_h * sin30)
        points = [point.to_tuple() for point in points]
        base_bottom = Sketch().polygon(points)

        wp_top = (
            Workplane("XY").transformed(offset=(0, 0, wall_w)).placeSketch(base_top)
        )

        wp_bottom = (
            Workplane("XY")
            .transformed(offset=(0, 0, -taper_h + wall_w))
            .placeSketch(base_bottom)
        )

        return wp_top.add(wp_bottom).loft(combine=True)

    def _stub_void(self, placed_tile: PlacedTile) -> Workplane:
        points = placed_tile.vertices.centered_points(clr + wall_w + taper_h * sin30)
        points = [point.to_tuple() for point in points]
        base_bottom = Sketch().polygon(points)

        return (
            Workplane("XY")
            .transformed(offset=(0, 0, -taper_h - stub_h))
            .transformed(offset=(0, 0, wall_w))
            .placeSketch(base_bottom)
            .extrude(stub_h)
        )
