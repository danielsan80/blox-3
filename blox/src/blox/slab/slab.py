import cadquery as cq
import blox.config as config
import itertools
import logging
import math

log = logging.getLogger(__name__)


# Given some points on the same plane, make a slab of a given thickness

def areComplanar(points):
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


def noComplanarSlab(points, thick):
    sets = list(itertools.combinations(points, 3))
    result = None
    for set in sets:
        if (result == None):
            result = slab(set, thick)
        else:
            result = result.add(slab(set, thick))

    return result

def onePointSlab(points, thick):
    return cq.Workplane().sphere(thick/2).translate(points[0])

def twoPointSlab(points, thick):

    p1, p2 = [cq.Vector(*p) for p in points[:2]]

    sphere1 = cq.Workplane("XY").sphere(thick/2).translate(p1.toTuple())
    sphere2 = cq.Workplane("XY").sphere(thick/2).translate(p2.toTuple())

    result = (
        sphere1.union(sphere2)
    )


    direction = p2 - p1
    distance = direction.Length

    xDir = cq.Vector(0, 0, 1).cross(direction.normalized())

    plane = cq.Plane(p1, xDir, direction)

    cylinder = (
        cq.Workplane(plane)
        .circle(thick/2)
        .extrude(distance)
    )

    result = result.add(cylinder)

    return result





def slab(points, thick):
    if (len(points) == 1):
        return onePointSlab(points, thick)

    if (len(points) == 2):
        return twoPointSlab(points, thick)

    if ( not areComplanar(points)):
        return noComplanarSlab(points, thick).clean()


    wire = cq.Wire.makePolygon(points).close()
    face = cq.Face.makeFromWires(wire)
    origin = face.Center()
    normal = face.normalAt()
    face = face.translate((normal.x * -thick/2, normal.y * -thick/2, normal.z * -thick/2))

    if (normal == cq.Vector(0, 0, 1)):
        xDir = cq.Vector(1, 0, 0)
    elif (normal == cq.Vector(0, 0, -1)):
        xDir = cq.Vector(1, 0, 0)
    else:
        xDir = cq.Vector(0, 0, 1).cross(normal)

    plane = cq.Plane(origin, xDir, normal)
    result = cq.Workplane(plane).add(face).wires().toPending().offset2D(thick/2).extrude(thick).edges().fillet(thick/2-config.fix)


    return result