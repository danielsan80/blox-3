import sys

sys.path.append("../../src/")

from dataclasses import dataclass
from pprint import pprint
from types import SimpleNamespace

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.config import clr, stub_h, taper_h, wall_w
from triblox.helper.util import normalize_float, sin30
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class PrismVoid:
    mosaic: Mosaic
    h: float

    def __post_init__(self):
        if self.h <= 0:
            raise ValueError("Height must be greater than 0")
        object.__setattr__(self, "h", normalize_float(self.h))

    def get(self) -> Workplane:

        result = Workplane("XY")

        for placed_tile in self.mosaic.placed_tiles.values():
            result = result.union(self._slope_void(placed_tile))
            result = result.union(self._prism_void(placed_tile))
        return result

    def _values(self) -> SimpleNamespace:
        taper_v = clr + taper_h
        taper_o = taper_v * sin30
        stub_v = stub_h
        prism_o = clr + wall_w

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
            .transformed(offset=(0, 0, h(self.h) - v.taper_v - v.stub_v))
            .placeSketch(slope_top)
        )

        wp_bottom = (
            Workplane("XY")
            .transformed(
                offset=(0, 0, h(self.h) - v.taper_v - v.stub_v - v.slope_bottom_v)
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
            .transformed(offset=(0, 0, h(self.h) - v.taper_v - v.stub_v))
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
        void_h = h(self.h) - reduce_v - wall_w

        pprint(void_h)

        assert void_h > 0, "Height is too small for prism void"

        points = placed_tile.vertices.offset_points(v.prism_o)
        points = [point.to_tuple() for point in points]
        triangle = Sketch().polygon(points)

        return (
            Workplane("XY")
            .placeSketch(triangle)
            .extrude(void_h)
            .translate((0, 0, wall_w))
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
            .extrude(h(self.h) - reduce_v - wall_w)
            .translate((0, 0, wall_w))
        )
