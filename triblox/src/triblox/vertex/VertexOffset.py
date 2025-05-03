import sys

sys.path.append("src/")

from enum import Enum


class VertexOffset(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    SPLIT = "split"
    NONE = "none"
