import sys

sys.path.append("../../src/")

from triblox.config import h_fix, h_step
from triblox.helper.util import normalize_float


def h(n: float) -> float:
    n = normalize_float(n)
    return n * h_step + h_fix
