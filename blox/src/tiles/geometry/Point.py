from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class Point:
    x: int
    y: int