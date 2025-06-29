import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Workplane

from triblox.block.functions import h
from triblox.config import clr, stub_h, taper_h
from triblox.geometry.Point import Point
from triblox.helper.util import normalize_float


@dataclass(frozen=True)
class WasherVoid:
    h: float
    washer_center: Point
    washer_h: float
    washer_d: float

    def __post_init__(self):
        if self.h <= 0:
            raise ValueError("Height must be greater than 0")
        if self.washer_h <= 0:
            raise ValueError("Washer height must be greater than 0")
        if self.washer_d <= 0:
            raise ValueError("Washer diameter must be greater than 0")

        object.__setattr__(self, "h", normalize_float(self.h))
        object.__setattr__(self, "washer_h", normalize_float(self.washer_h))
        object.__setattr__(self, "washer_d", normalize_float(self.washer_d))

    def get(self) -> Workplane:
        result = (
            Workplane("XY")
            .circle(self.washer_d / 2)
            .extrude(-self.washer_h)
            .translate((self.washer_center.x, self.washer_center.y, 0))
            .translate((0, 0, h(self.h) - clr - taper_h - stub_h))
        )

        return result
