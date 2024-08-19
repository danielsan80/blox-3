import cadquery as cq
import blox.config as c
from blox.slab.slab import slab
from blox.slab.hull import hull
from blox.util.mv import mv, mvs
from blox.block.bottom import emptyBottom, fullBottom
from blox.block.Blocks import Blocks
from blox.util.posTranslate import posTranslate
import time

import logging

log = logging.getLogger(__name__)

# Given some points on the same plane, make a slab of a given thickness

def _rowJoint(rows:int, cols:int) -> cq.Solid:
    result = (
        slab([
            mv((0, 0, 0), (1,-1,1)),
            mv((Blocks.l(cols), 0, 0), (-1,-1,1)),
            mv((Blocks.l(cols), 0, 0), (-1,1,1)),
            mv((0, 0, 0), (1,1,1)),
        ], c.wall_w)
    )
    result = mvs(result, (0,0,-1))
    return result

def _colJoint(rows:int, cols:int) -> cq.Solid:
    result = (
        slab([
            mv((0, 0, 0), (-1,1,1)),
            mv((0, 0, 0), (1,1,1)),
            mv((0, Blocks.l(rows), 0), (1,-1,1)),
            mv((0, Blocks.l(rows), 0), (-1,-1,1)),
        ], c.wall_w)
    )
    result = mvs(result, (0,0,-1))
    return result


def boxBottom(
        rows: int = c.box_rows,
        cols: int = c.box_cols,
        mode: str = "empty",
    ) -> cq.Solid:

    start_time = time.time()

    if mode == "empty":
        tale = emptyBottom()
    if mode == "full":
        tale = fullBottom()

    rowJoint = _rowJoint(rows=rows, cols=cols)
    colJoint = _colJoint(rows=rows, cols=cols)

    rowJoints = (
        cq.Workplane("XY")
        .pushPoints([(0, c.block_side * i,0) for i in range(1,rows)])
        .eachpoint(
            lambda loc: (
                cq.Workplane()
                .union(rowJoint)
                .val()
                .located(loc)
            )
        )
        .findSolid()
    )

    colJoints = (
        cq.Workplane("XY")
        .pushPoints([(c.block_side * j,0,0) for j in range(1,cols)])
        .eachpoint(
            lambda loc: (
                cq.Workplane()
                .union(colJoint)
                .val()
                .located(loc)
            )
        )
        .clean()
        .findSolid()
    )

    points = [(c.block_side * j, c.block_side * i) for i in range(rows) for j in range(cols)]
    tales = (
        cq.Workplane("XY")
        .pushPoints(points)
        .eachpoint(
            lambda loc: (
                cq.Workplane()
                .union(tale)
                .val()
                .located(loc)
            )
        )
        .findSolid()
    )

    result = (
        cq.Workplane("XY")
        .union(tales)
        .union(rowJoints)
        .union(colJoints)
        .clean()
        .findSolid()
    )

    end_time = time.time()

    execution_time = end_time - start_time

    log.info(f"Execution time: {execution_time}")

    return result