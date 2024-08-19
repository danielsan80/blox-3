import cadquery as cq
import blox.config as c
from blox.dir.dirs import assertIsValidDir

def dirRotate(solid: cq.Solid, dir: str = "west", rows:int = 1, cols: int = 1) -> cq.Solid:
    side = c.block_side

    assertIsValidDir(dir)

    match dir:
        case "west":
            return solid
        case "north":
            return (
                cq.Workplane()
                .union(solid)
                .rotate((0, 0, 0), (0, 0, 1), 270)
                .translate((0, side * rows, 0))
                .findSolid()
            )
        case "east":
            return (
                cq.Workplane()
                .union(solid)
                .rotate((0, 0, 0), (0, 0, 1), 180)
                .translate((side * cols, side * rows, 0))
                .findSolid()
            )
        case "south":
            return (
                cq.Workplane()
                .union(solid)
                .rotate((0, 0, 0), (0, 0, 1), 90)
                .translate((side * cols, 0, 0))
                .findSolid()
            )

    raise ValueError("this should never happen")