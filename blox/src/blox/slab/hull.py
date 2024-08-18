import cadquery as cq
from blox.geometry.types import PointList, Point

from scipy.spatial import ConvexHull

def simpleHull(points: PointList) -> cq.Solid:
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


def hull(points: PointList, ext: float = 0) -> cq.Solid:

    assert (ext >= 0), "ext must be greater than or equal to zero"

    solid = simpleHull(points)

    if ext == 0:
        return solid
    return (
        cq.Workplane()
        .union(solid.shell([], ext))
        .union(solid)
        .clean()
        .findSolid()
    )
