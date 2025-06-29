import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.caching.CacheBase import CacheBase
from triblox.caching.CachedResult import CachedResult
from triblox.config import clr, h_clr, h_cut, stub_h, taper_h
from triblox.helper.util import normalize_float, sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class TopVoid:
    mosaic: Mosaic
    hu: float

    def __post_init__(self):
        if self.hu <= 0:
            raise ValueError("Height units must be greater than 0")
        object.__setattr__(self, "hu", normalize_float(self.hu))

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
            result = result.union(self._top_leveling(placed_tile))

            cached_result.add(placed_tile, result)

        result = cached_result.get()
        result = result.translate((0, 0, h(self.hu)))
        return result

    def _taper_void(self, placed_tile: PlacedTile) -> Workplane:
        taper_v = clr + taper_h

        points = placed_tile.vertices.original_points(to6=True)
        points = [point.to_tuple() for point in points]
        base_up = Sketch().polygon(points)

        points = placed_tile.vertices.offset_points(taper_v * sin30, to6=True)
        points = [point.to_tuple() for point in points]
        base_down = Sketch().polygon(points)

        wp_up = Workplane("XY").placeSketch(base_up)

        wp_down = (
            Workplane("XY").transformed(offset=(0, 0, -taper_v)).placeSketch(base_down)
        )

        return wp_up.add(wp_down).loft(combine=True)

    def _stub_void(self, placed_tile: PlacedTile) -> Workplane:
        taper_v = clr + taper_h

        points = placed_tile.vertices.offset_points(taper_v * sin30)
        points = [point.to_tuple() for point in points]
        base_down = Sketch().polygon(points)

        return (
            Workplane("XY")
            .transformed(offset=(0, 0, -taper_v - stub_h))
            .placeSketch(base_down)
            .extrude(stub_h)
        )

        return wp_up.add(wp_down).loft(combine=True)

    def _top_leveling(self, placed_tile) -> Workplane:
        points = placed_tile.vertices.offset_points(clr)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)
        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(h_clr + h_cut)
            .translate((0, 0, -h_clr - h_cut))
        )
