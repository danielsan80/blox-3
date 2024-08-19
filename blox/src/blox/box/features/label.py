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


def _lableBody(
        wall_l: int = 5,
        wall_h: int = 4,
        l: float = 2,
        w: float = 1,
    ) -> cq.Solid:

    ext = c.ext

    main = hull(
        [
            mv((0,0,-2*ext), (1,1,0)),
            mv((0,Blocks.l(l),-2*ext), (1,-1,0)),
            mv((Blocks.l(w),Blocks.l(l),-2*ext), (-1,-1,0)),
            mv((Blocks.l(w),0,-2*ext), (-1,1,0)),

            mv((0,0,-2*ext-Blocks.l(w)), (1,1,2)),
            mv((0,Blocks.l(l)-Blocks.l(w),-2*ext-Blocks.l(w)), (1,-1,2)),

        ],
        c.wall_w/2
    )

    filler1 = hull(
        [
            mv((0,0,-2*ext), (1,1,0)),
            mv((0,Blocks.l(l),-2*ext), (1,-1,0)),
            mv((ext, Blocks.l(l),-2*ext), (0,-1,0)),
            mv((ext, 0,-2*ext), (0,1,0)),

            mv((ext, 0,-ext), (0,1,-1)),
            mv((ext, Blocks.l(l)+ext,-ext), (0,-2,-1)),

        ],
        c.wall_w/2
    )

    filler2 = hull(
        [
            mv((0,0,-2*ext), (1,1,0)),
            mv((Blocks.l(w),0,-2*ext), (-1,1,0)),
            mv((Blocks.l(w),ext,-2*ext), (-1,0,0)),
            mv((0,ext,-2*ext), (1,0,0)),

            mv((0,ext,-ext), (1,0,-1)),
            mv((Blocks.l(w)+ext,ext,-ext), (-2,0,-1)),

        ],
        c.wall_w/2
    )

    result = (
        cq.Workplane()
        .union(main)
        .union(filler1)
        .union(filler2)
        .clean()
        .findSolid()
    )


    return result



def boxLabel(
        wall_l: int = 5,
        wall_h: int = 4,
        l: float = 2,
        w: float = 1,
    ) -> cq.Solid:

    label = _lableBody(wall_l, wall_h, l, w)

    return (
        cq.Workplane()
        .union(label)
        .translate((0,0,Blocks.h(wall_h, True)))
        .findSolid()
    )



