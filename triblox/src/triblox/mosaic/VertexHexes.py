import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.point.Point import Point
from triblox.mosaic.VertexHex import VertexHex


@dataclass(frozen=True)
class VertexHexes:
    a: VertexHex
    b: VertexHex
    c: VertexHex
