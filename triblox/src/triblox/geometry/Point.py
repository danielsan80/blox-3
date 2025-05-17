import sys

sys.path.append("src/")


from dataclasses import dataclass

from shapely.affinity import rotate as sh_rotate
from shapely.geometry import Point as ShPoint

from triblox.helper.util import hypotenuse, normalize_float


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        object.__setattr__(self, "x", normalize_float(x))
        object.__setattr__(self, "y", normalize_float(y))

    # Move to a destination point by a value in mm
    def move(self, destination: "Point", value: float) -> "Point":
        value = normalize_float(value)
        if value == float(0):
            return self

        dx = destination.x - self.x
        dy = destination.y - self.y
        distance = hypotenuse(dx, dy)

        if distance == 0:
            raise ValueError("Cannot move to the same point")

        ratio = value / distance
        return Point(self.x + dx * ratio, self.y + dy * ratio)

    def move_by_ratio(self, destination: "Point", ratio: float) -> "Point":
        ratio = normalize_float(ratio)
        if ratio == float(0):
            return self

        dx = destination.x - self.x
        dy = destination.y - self.y
        distance = hypotenuse(dx, dy)

        if distance == 0:
            raise ValueError("Cannot move to the same point")

        return Point(self.x + dx * ratio, self.y + dy * ratio)

    def distance(self, other: "Point") -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return hypotenuse(dx, dy)

    def rotate(self, origin: "Point", angle: float) -> "Point":

        _point = ShPoint(self.x, self.y)
        _origin = ShPoint(origin.x, origin.y)

        _rotated_point = sh_rotate(_point, angle=angle, origin=_origin)

        return Point(_rotated_point.x, _rotated_point.y)

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def is_equal(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y
