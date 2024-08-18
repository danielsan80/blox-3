import cadquery as cq
import blox.config as c
from blox.slab.slab import slab
from blox.slab.hull import hull
from blox.util.mv import mv

# Given some points on the same plane, make a slab of a given thickness

def dir_rotate(workplane, dir="west", rows=1, cols=1):
    side = c.block_side

    match dir:
        case "west":
            return workplane
        case "north":
            return (
                workplane
                .rotate((0, 0, 0), (0, 0, 1), 270)
                .translate((0, side * rows, 0))
            )
        case "east":
            return (
                workplane
                .rotate((0, 0, 0), (0, 0, 1), 180)
                .translate((side * cols, side * rows, 0))
            )
        case "south":
            return (
                workplane
                .rotate((0, 0, 0), (0, 0, 1), 90)
                .translate((side * cols, 0, 0))
            )
        case _:
            raise ValueError(f"Not valid dir: {dir}")


def slope(dir="west"):
    ext = c.ext
    side = c.block_side
    wall_w = c.wall_w

    result = (slab([
        mv((0, 0, 0), (1,1,1)),
        mv((0, side, 0), (1,-1,1)),
        mv((ext, side-ext, -ext), (1,-1,1)),
        mv((ext, ext, -ext), (1,1,1)),
    ], wall_w))

    result = dir_rotate(result, dir, 1, 1)

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
    return (
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

