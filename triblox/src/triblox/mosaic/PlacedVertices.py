import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.vertex.Vertex import Vertex


@dataclass(frozen=True)
class PlacedVertices:
    a: Vertex
    b: Vertex
    c: Vertex
