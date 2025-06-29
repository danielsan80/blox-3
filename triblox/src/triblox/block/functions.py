import sys

sys.path.append("../../src/")

from triblox.config import h_fix, h_unit
from triblox.helper.util import normalize_float


def h(hu: float) -> float:
    hu = normalize_float(hu)
    return hu * h_unit + h_fix


def h_reverse(h_mm: float) -> float:
    h_mm = normalize_float(h_mm)
    return (h_mm - h_fix) / h_unit
