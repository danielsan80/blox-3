import cadquery as cq
import blox.config as c
from blox.dir.dirs import assertIsValidDir
from blox.slab.hull import hull
from blox.util.mv import mv
from blox.block.bottom import emptyBottom, fullBottom
from blox.block.Blocks import Blocks
from blox.util.dirRotate import dirRotate
import time

import logging

log = logging.getLogger(__name__)


def _singleBorder(
        l: int = c.box_l,
        h: float = c.box_h,
    ) -> cq.Solid:

    ext = c.ext

    border = (
        hull(
            [
                mv((0, 0, 0), (1,1,-2)),
                mv((0, Blocks.l(l), 0), (1,-1,-2)),

                mv((0, 0, -2*ext), (1,1,0)),
                mv((0, Blocks.l(l), -2*ext), (1,-1,0)),

                mv((ext, 0, -ext), (0,1,-1)),
                mv((ext, Blocks.l(l), -ext), (0,-1,-1)),
            ],
            c.wall_w/2
        )
    )

    border = (
        cq.Workplane("XY")
        .union(border)
        .translate((0,0,Blocks.h(h, True)))
        .findSolid()
    )

    return border


def boxWallBorder(
        dir: str = "west",
        rows: int = c.box_rows,
        cols: int = c.box_cols,
        h: float = c.box_h,
    ) -> cq.Solid:

    assertIsValidDir(dir)

    if (dir in ["west", "east"]):
        border = _singleBorder(l=rows, h=h)
    elif (dir in ["north", "south"]):
        border = _singleBorder(l=cols, h=h)
    else:
        raise ValueError("this should never happen")

    return dirRotate(border, dir, rows, cols)
