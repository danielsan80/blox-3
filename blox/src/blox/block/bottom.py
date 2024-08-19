import cadquery as cq
import blox.config as c
from blox.slab.slab import slab
from blox.slab.hull import hull
from blox.util.mv import mv, mvs
from blox.util.dirRotate import dirRotate


def slope(dir="west") -> cq.Solid:
    ext = c.ext
    side = c.block_side
    wall_w = c.wall_w

    result = (
        slab([
            mv((0, 0, 0), (1,1,1)),
            mv((0, side, 0), (1,-1,1)),
            mv((ext, side-ext, -ext), (1,-1,1)),
            mv((ext, ext, -ext), (1,1,1)),
        ], wall_w)
    )

    result = dirRotate(result, dir, 1, 1)

    result = mvs(result, (0,0,-1))

    return result

def floor() -> cq.Solid:
    ext = c.ext
    side = c.block_side
    wall_w = c.wall_w

    result = (slab([
        mv((ext, ext, -ext), (1,1,1)),
        mv((ext, side-ext, -ext), (1,-1,1)),
        mv((side-ext, side-ext, -ext), (-1,-1,1)),
        mv((side-ext, ext, -ext), (-1,1,1)),
    ], wall_w))

    result = mvs(result, (0,0,-1))

    return result

def emptyBottom() -> cq.Solid:
    return (
        cq.Workplane()
        .union(floor())
        .union(slope("west"))
        .union(slope("north"))
        .union(slope("east"))
        .union(slope("south"))
        .clean()
        .findSolid()
    )

def fullBottom() -> cq.Solid:
    ext = c.ext
    side = c.block_side
    wall_w = c.wall_w
    result = (
        hull([
            mv((0, 0, 0), (1,1,1)),
            mv((0, side, 0), (1,-1,1)),
            mv((side, side, 0), (-1,-1,1)),
            mv((side, 0, 0), (-1,1,1)),
            mv((ext, ext, -ext), (1,1,1)),
            mv((ext, side-ext, -ext), (1,-1,1)),
            mv((side-ext, side-ext, -ext), (-1,-1,1)),
            mv((side-ext, ext, -ext), (-1,1,1)),
        ], wall_w/2)
    )

    result = mvs(result, (0,0,-1))

    return result

