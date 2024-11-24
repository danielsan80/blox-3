from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class TileCoord:
    x: int
    y: int