import sys
sys.path.append('src/')

from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        object.__setattr__(self, 'x', abs(float(x)) * (1 if x >= 0 else -1))
        object.__setattr__(self, 'y', abs(float(y)) * (1 if y >= 0 else -1))
