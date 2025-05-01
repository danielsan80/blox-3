import sys

sys.path.append("src/")

from dataclasses import dataclass

from triblox.tile.Coord import Coord


@dataclass(frozen=True)
class AdjacentCoords:
    ab: Coord
    bc: Coord
    ca: Coord
