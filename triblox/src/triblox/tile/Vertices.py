import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.point.Point import Point


@dataclass(frozen=True)
class Vertices:
    a: Point
    b: Point
    c: Point
