import sys

sys.path.append("../../src/")

import math
from dataclasses import dataclass

from cadquery import Edge, Vector, Workplane

from triblox.geometry.Point import Point
from triblox.helper.util import normalize_float


@dataclass(frozen=True)
class Duct:
    enter_point: Point
    enter_h: float

    exit_point: Point
    exit_h: float

    d: float

    def __post_init__(self):
        if self.enter_h <= 0:
            raise ValueError("Enter height must be greater than 0")
        if self.exit_h <= 0:
            raise ValueError("Exit height must be greater than 0")
        if self.d <= 0:
            raise ValueError("Duct diameter must be greater than 0")

        object.__setattr__(self, "enter_h", normalize_float(self.enter_h))
        object.__setattr__(self, "exit_h", normalize_float(self.exit_h))
        object.__setattr__(self, "d", normalize_float(self.d))

    def get(self) -> Workplane:
        result = Workplane("XY")

        enter = self.enter_point
        enter_h = self.enter_h

        exit = self.exit_point
        exit_h = self.exit_h

        d = self.d

        enter_l = enter_h - exit_h
        exit_l = exit.distance(enter)

        curve_l = min(enter_l, exit_l) / 2

        enter_section = (
            Workplane("XY")
            .transformed(offset=(0, 0, enter_h))
            .circle(d / 2)
            .extrude(-enter_l + curve_l)
        )

        exit_section = (
            Workplane("XY")
            .transformed(rotate=(90, 0, 0))
            .transformed(offset=(0, exit_h, exit_l))
            .circle(d / 2)
            .extrude(-exit_l + curve_l)
        )

        center = Vector(0, -curve_l, enter_h - enter_l + curve_l)
        radius = curve_l

        arc = Edge.makeCircle(radius, center, Vector(1, 0, 0), 0, 90)

        curve_section = (
            Workplane("XY")
            .transformed(offset=(0, 0, enter_h - enter_l + curve_l))
            .circle(d / 2)
            .sweep(Workplane("XY").newObject([arc]), isFrenet=True)
        )

        duct = (
            Workplane("XY")
            .union(enter_section)
            .union(exit_section)
            .union(curve_section)
        )

        v1 = Vector(0, -1)
        v2 = Vector(exit.x - enter.x, exit.y - enter.y).normalized()

        angle = math.atan2(v2.y, v2.x) - math.atan2(v1.y, v1.x)
        angle = (angle + math.pi) % (2 * math.pi) - math.pi

        duct = duct.rotate((0, 0, 0), (0, 0, 1), math.degrees(angle))
        duct = duct.translate((enter.x, enter.y, 0))

        return duct
