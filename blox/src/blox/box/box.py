import cadquery as cq
import blox.config as c
from blox.box.features.bottom import boxBottom
from blox.box.features.wall import boxWall
from blox.box.features.wallBorder import boxWallBorder
from blox.box.features.label import boxLabel

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

    label = boxLabel(wall_l = cols, wall_h = h, l = 2, w = 1)

    result = (
        cq.Workplane()
        .union(bottom)
    )

    for wall in walls:
        result = result.union(wall).clean()

    for wallBorder in wallBorders:
        result = result.union(wallBorder).clean()

    result = result.union(label).clean()

    return (
        result
        .findSolid()
    )
