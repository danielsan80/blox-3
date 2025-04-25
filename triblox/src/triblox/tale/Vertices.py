import sys
sys.path.append('src/')

from triblox.point.Point import Point
from dataclasses import dataclass

@dataclass(frozen=True)
class Vertices:
    a: Point
    b: Point
    c: Point