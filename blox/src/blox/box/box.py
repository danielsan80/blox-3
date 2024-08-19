import cadquery as cq
import blox.config as c
from blox.box.features.bottom import boxBottom
from blox.box.features.wall import boxWall

# Given some points on the same plane, make a slab of a given thickness

def box(
        rows: int = c.box_rows,
        cols: int = c.box_cols,
        h: float = c.box_h,
    ) -> cq.Solid:

    bottom = boxBottom(rows, cols, mode = "empty")

    walls = [
        boxWall("north", rows, cols, h),
        boxWall("south", rows, cols, h),
        boxWall("west", rows, cols, h),
        boxWall("east", rows, cols, h),
    ]

    result = (
        cq.Workplane()
        .union(bottom)
    )

    for wall in walls:
        result = result.union(wall)


    return (
        result
        .findSolid()
        .clean()
    )
