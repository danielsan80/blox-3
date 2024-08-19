import cadquery as cq
import blox.config as c
from blox.slab.slab import slab
from blox.dir.dirs import assertIsValidDir
from blox.slab.hull import hull
from blox.util.mv import mv
from blox.block.bottom import emptyBottom, fullBottom
from blox.block.Blocks import Blocks
from blox.util.dirRotate import dirRotate
import time

import logging

log = logging.getLogger(__name__)


def _singleBoxWall(
        l: int = c.box_l,
        h: float = c.box_h,
    ) -> cq.Solid:

    return (
        slab(
            [
                mv((0, 0, 0), (1,1,0)),
                mv((0, 0, Blocks.h(h, True)), (1,1,-2)),
                mv((0, Blocks.l(l), Blocks.h(h, True)), (1,-1,-2)),
                mv((0, Blocks.l(l), 0), (1,-1,0)),
            ],
            c.wall_w
        )
    )

def boxWall(
        dir: str = "west",
        rows: int = c.box_rows,
        cols: int = c.box_cols,
        h: float = c.box_h,
    ) -> cq.Solid:

    assertIsValidDir(dir)

    if (dir in ["west", "east"]):
        wall = _singleBoxWall(l=rows, h=h)
    elif (dir in ["north", "south"]):
        wall = _singleBoxWall(l=cols, h=h)
    else:
        raise ValueError("this should never happen")

    return dirRotate(wall, dir, rows, cols)



