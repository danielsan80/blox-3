import sys

sys.path.append("../../src/")

from dataclasses import dataclass
from pprint import pprint
from types import SimpleNamespace

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.caching.CacheBase import CacheBase
from triblox.caching.CachedResult import CachedResult
from triblox.config import clr, stub_h, taper_h, wall_w
from triblox.helper.util import normalize_float, sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile
from typing import Optional

@dataclass(frozen=True)
class PrismVoid:
    mosaic: Mosaic
    hu: float
    wall_thick: Optional[float] = None
    bottom_thick: Optional[float] = None

    def __post_init__(self):
        if self.hu <= 0:
            raise ValueError("Height units must be greater than 0")
        if self.wall_thick is None:
            object.__setattr__(self, "wall_thick", wall_w)
        if self.wall_thick <= 0:
            raise ValueError("Wall thick must be greater than 0")
        if self.bottom_thick is None:
            object.__setattr__(self, "bottom_thick", self.wall_thick)
        if self.bottom_thick < 0:
            raise ValueError("Bottom thick must be positive or zero")

        object.__setattr__(self, "hu", normalize_float(self.hu))
        object.__setattr__(self, "wall_thick", normalize_float(self.wall_thick))
        object.__setattr__(self, "bottom_thick", normalize_float(self.bottom_thick))


    def get(self) -> Workplane:
        result = Workplane("XY")

        cache_base = (
            CacheBase()
                .add_owner(self)
                .add_mosaic(self.mosaic)
                .add("hu", self.hu)
                .add("wall_thick", self.wall_thick)
                .add("bottom_thick", self.bottom_thick)
        )

        cached_result = CachedResult(cache_base, result)

        for placed_tile in self.mosaic.placed_tiles.values():
            if cached_result.has(placed_tile):
                cached_result.add(placed_tile)
                continue
            result = cached_result.get()
            result = result.union(self._slope_void(placed_tile))
            result = result.union(self._prism_void(placed_tile))
            cached_result.add(placed_tile, result)

        result = cached_result.get()

        return result

    def _values(self) -> SimpleNamespace:
        taper_v = clr + taper_h
        taper_o = taper_v * sin30
        stub_v = stub_h
        prism_o = clr + self.wall_thick

        slope_top_o = taper_o
        back_o = slope_top_o - prism_o
        slope_bottom_o = slope_top_o - back_o
        slope_bottom_v = back_o / sin30

        return SimpleNamespace(
            taper_v=taper_v,
            taper_o=taper_o,
            stub_v=stub_v,
            prism_o=prism_o,
            slope_top_o=slope_top_o,
            back_o=back_o,
            slope_bottom_o=slope_bottom_o,
            slope_bottom_v=slope_bottom_v,
        )

    def _slope_void(self, placed_tile: PlacedTile) -> Workplane:
        v = self._values()
        if v.prism_o < v.taper_o:
            return self._slope_void_default(placed_tile)
        else:
            return self._slope_void_null(placed_tile)

    def _slope_void_default(self, placed_tile: PlacedTile) -> Workplane:
        v = self._values()

        points = placed_tile.vertices.offset_points(v.slope_top_o)
        points = [point.to_tuple() for point in points]
        slope_top = Sketch().polygon(points)

        points = placed_tile.vertices.offset_points(v.slope_bottom_o)
        points = [point.to_tuple() for point in points]
        slope_bottom = Sketch().polygon(points)

        wp_top = (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.hu) - v.taper_v - v.stub_v))
            .placeSketch(slope_top)
        )

        wp_bottom = (
            Workplane("XY")
            .transformed(
                offset=(0, 0, h(self.hu) - v.taper_v - v.stub_v - v.slope_bottom_v)
            )
            .placeSketch(slope_bottom)
        )

        return wp_top.add(wp_bottom).loft(combine=True)

    def _slope_void_null(self, placed_tile: PlacedTile) -> Workplane:
        v = self._values()

        points = placed_tile.vertices.offset_points(v.slope_top_o)
        points = [point.to_tuple() for point in points]
        slope_top = Sketch().polygon(points)

        return (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.hu) - v.taper_v - v.stub_v))
            .placeSketch(slope_top)
            .extrude(0.00001)
        )

    def _prism_void(self, placed_tile: PlacedTile) -> Workplane:
        v = self._values()

        if v.prism_o < v.taper_o:
            return self._prism_void_default(placed_tile)
        else:
            return self._prism_void_null(placed_tile)

    def _prism_void_default(self, placed_tile: PlacedTile) -> Workplane:
        v = self._values()

        reduce_v = v.taper_v + v.stub_v + v.slope_bottom_v
        void_h = h(self.hu) - reduce_v - self.bottom_thick

        pprint(void_h)

        assert void_h > 0, "Height is too small for prism void"

        points = placed_tile.vertices.offset_points(v.prism_o)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)

        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(void_h)
            .translate((0, 0, self.bottom_thick))
        )

    def _prism_void_null(self, placed_tile: PlacedTile) -> Workplane:
        v = self._values()

        reduce_v = 0

        points = placed_tile.vertices.offset_points(v.prism_o)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)

        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(h(self.hu) - reduce_v - self.bottom_thick)
            .translate((0, 0, self.bottom_thick))
        )
