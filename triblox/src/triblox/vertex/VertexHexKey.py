import sys

sys.path.append("src/")

from enum import Enum


class VertexHexKey(Enum):
    MAIN = "main"
    LEFT_NEAR = "left_near"
    LEFT_FAR = "left_far"
    RIGHT_NEAR = "right_near"
    RIGHT_FAR = "right_far"
    OPPOSITE = "opposite"
