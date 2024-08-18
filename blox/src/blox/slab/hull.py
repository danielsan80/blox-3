import cadquery as cq
import blox.config as c
import itertools
from typing import List, Tuple, TypeAlias

from scipy.spatial import ConvexHull, Delaunay

Point: TypeAlias = Tuple[float, float, float]
PointList: TypeAlias = List[Point]

def hull(points: PointList) -> cq.Solid:
    hull = ConvexHull(points)

    simplices = hull.simplices

    faces = []

    for s in simplices:
        wire = cq.Wire.makePolygon([
            points[s[0]],
            points[s[1]],
            points[s[2]],
        ]).close()
        faces.append(cq.Face.makeFromWires(wire))

    shell = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(shell).clean()


def thickHull(points: PointList, thick: float = 0) -> cq.Solid:

    assert (thick >= 0), "thick must be greater than or equal to zero"

    solid = hull(points)

    if thick == 0:
        return solid
    return (
        cq.Workplane()
        .add(solid.shell([], thick))
        .add(solid)
        .clean()
        .findSolid()
    )
