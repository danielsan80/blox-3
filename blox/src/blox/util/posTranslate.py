import cadquery as cq
import blox.config as c
from blox.dir.dirs import assertIsValidDir
from blox.geometry.types import Point
from blox.block.Blocks import Blocks

def _isDef(x) -> bool:
    return x is not None

def posTranslate(solid: cq.Solid, pos: Point|None = None, row:int|None = None, col:int|None = None, h:float|None = None) -> cq.Solid:

    if _isDef(row):
        row = row
    else:
        row = pos[1] if _isDef(pos) else 0

    if _isDef(col):
        col = col
    else:
        col = pos[0] if _isDef(pos) else 0

    if _isDef(h):
        h = h
    else:
        h = pos[2] if _isDef(pos) else 0

    if _isDef(pos):
        assert row == pos[1], "Use of pos and row together is not allowed"
        assert col == pos[0], "Use of pos and col together is not allowed"
        assert h == pos[2], "Use of pos and h together is not allowed"

    return (
        cq.Workplane()
        .union(solid)
        .translate((
            Blocks.l(col),
            Blocks.l(row),
            Blocks.h(h)
        ))
        .findSolid()
    )
