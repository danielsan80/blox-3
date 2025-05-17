import sys

sys.path.append("src/")

from dataclasses import dataclass


@dataclass(frozen=True)
class AdjacentTiles:
    ab: "Tile"
    bc: "Tile"
    ca: "Tile"

    def to_list(self) -> list["Tile"]:
        return [self.ab, self.bc, self.ca]
