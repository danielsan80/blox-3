import cadquery as cq
import blox.config as c
from blox.box.features.bottom import boxBottom
from blox.box.features.wall import boxWall
from blox.box.features.wallBorder import boxWallBorder

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

    wallBorders = [
        boxWallBorder("north", rows, cols, h),
        boxWallBorder("south", rows, cols, h),
        boxWallBorder("west", rows, cols, h),
        boxWallBorder("east", rows, cols, h),
    ]

    result = (
        cq.Workplane()
        .union(bottom)
    )

    for wall in walls:
        result = result.union(wall).clean()

    for wallBorder in wallBorders:
        result = result.union(wallBorder).clean()

    return (
        result
        .findSolid()
    )
