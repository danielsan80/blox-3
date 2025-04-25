import sys
sys.path.append('src/')

from dataclasses import dataclass

@dataclass(frozen=True)
class Coord:
    x: int
    y: int