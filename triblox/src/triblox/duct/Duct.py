import sys

sys.path.append("../../src/")

from dataclasses import dataclass
from pprint import pprint

from cadquery import Sketch, Workplane, Vector, Edge

from triblox.block.functions import h
from triblox.config import clr, fix
from triblox.geometry.Point import Point
from triblox.helper.util import normalize_float, sin60, sin45
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


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
            .transformed(offset=(enter.x, enter.y, enter_h))
            .circle(d/2)
            .extrude(-enter_l+curve_l)
        )

        exit_section = (
            Workplane("XY")
            .transformed(rotate=(90,0,0))
            .transformed(offset=(exit.x, exit_h, exit.y))
            .circle(d/2)
            .extrude(-exit_l+curve_l)

        )

        center = Vector(enter.x, enter.y - curve_l, enter_h - enter_l + curve_l)
        radius = curve_l

        arc = Edge.makeCircle(radius, center, Vector(1, 0, 0), 0, 90)

        curve_section = (
            Workplane("XY")
            .transformed(offset=(enter.x, enter.y, enter_h - enter_l + curve_l))
            .circle(d / 2)
            .sweep(Workplane("XY").newObject([arc]), isFrenet=True)
        )

        duct = (
            Workplane("XY")
            .union(enter_section)
            .union(exit_section)
            .union(curve_section)
        )

        return duct
