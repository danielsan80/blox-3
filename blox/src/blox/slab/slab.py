import cadquery as cq
import blox.config as c
import itertools
import logging
import math
from blox.util.xDir import xDir
from blox.slab.hull import hull
from scipy.spatial import ConvexHull

from blox.geometry.types import PointList, Point

log = logging.getLogger(__name__)


# Given some points on the same plane, make a slab of a given thickness

def areComplanar(points: PointList) -> bool:
    if len(points) < 4:
        return True

    p1, p2, p3 = [cq.Vector(*p) for p in points[:3]]
    v1 = p2 - p1
    v2 = p3 - p1

    normal = v1.cross(v2)

    for p in points[3:]:
        v = cq.Vector(*p) - p1
        if normal.dot(v) != 0:
            return False

    return True


def _noCoplanarSlab(points: PointList, thick: float) -> cq.Solid:
    return hull(points, thick/2)

def _onePointSlab(points: PointList, thick: float) -> cq.Solid:

    assert (len(points) == 1), "onePointSlab takes exactly one point"

    return (
        cq.Workplane()
        .sphere(thick/2)
        .translate(points[0])
        .findSolid()
    )

def _twoPointSlab(points: PointList, thick: float) -> cq.Solid:

    assert (len(points) == 2), "twoPointSlab takes exactly two points"

    p1, p2 = [cq.Vector(*p) for p in points[:2]]

    direction = p2 - p1
    distance = direction.Length

    plane = cq.Plane(p1, xDir(direction), direction)

    cylinder = (
        cq.Workplane(plane)
        .circle(c.fix/1000)
        .extrude(distance)
        .findSolid()
    )

    return cylinder.shell([], thick/2)


def slab(points: PointList, thick: float = 0) -> cq.Solid:

    assert (thick >= 0), "thick must be greater than or equal to zero"

    if (len(points) == 1):
        return _onePointSlab(points, thick)

    if (len(points) == 2):
        return _twoPointSlab(points, thick)

    if ( not areComplanar(points)):
        return _noCoplanarSlab(points, thick)

    wire = cq.Wire.makePolygon(points).close()
    face = cq.Face.makeFromWires(wire)
    origin = face.Center()
    normal = face.normalAt()
    face = face.translate((normal.x * -c.fix/2, normal.y * -c.fix/2, normal.z * -c.fix/2))

    plane = cq.Plane(origin, xDir(normal), normal)
    solid = (
        cq.Workplane(plane)
        .add(face)
        .wires()
        .toPending()
        .extrude(c.fix)
        .findSolid()
    )

    if thick == 0:
        return solid

    return (
        cq.Workplane()
        .union(solid.shell([], thick/2))
        .union(solid)
        .clean()
        .findSolid()
    )

