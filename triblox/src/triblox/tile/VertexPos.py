import sys

sys.path.append("src/")

from triblox.tile.Tile import Tile

from dataclasses import dataclass
from enum import Enum
from typing import Dict

class VertexPos(Enum):
    A = "a"
    B = "b"
    C = "c"
