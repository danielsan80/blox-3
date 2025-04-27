import sys
sys.path.append('src/')


from dataclasses import dataclass
from triblox.helper.util import normalize_float, hypotenuse





@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        object.__setattr__(self, 'x', normalize_float(x))
        object.__setattr__(self, 'y', normalize_float(y))

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

    def toTuple(self) -> tuple:
        return (self.x, self.y)