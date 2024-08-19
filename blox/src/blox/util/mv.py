import blox.config as c
from blox.geometry.types import Point
import cadquery as cq
from typing import Tuple


def mv(point:Point, pos:Point=(0,0,0), step:float = c.mv_step) -> Point:
    return (
        point[0]+pos[0]*step,
        point[1]+pos[1]*step,
        point[2]+pos[2]*step
    )

def mvs(solid: cq.Solid, pos:Point=(0,0,0), step:float = c.mv_step) -> cq.Solid:
    return (
        cq.Workplane()
        .union(solid)
        .translate((pos[0]*step, pos[1]*step, pos[2]*step))
        .findSolid()
    )
