import cadquery as cq
import blox.config as config


def slab(points, thick):
    wire = cq.Workplane().polyline(points).close()
    plate = wire.extrude(thick).edges("|Z").fillet(thick).edges("|X").fillet(thick/2-config.fix)
    return plate


def slab3d(points, thick):
    wire = cq.Wire.makePolygon(points).close()
    face = cq.Face.makeFromWires(wire)
    origin = face.Center()
    normal = face.normalAt()
    face = face.translate((normal.x * -thick/2, normal.y * -thick/2, normal.z * -thick/2))
    xDir = cq.Vector(0, 0, 1).cross(normal)
    plane = cq.Plane(origin, xDir, normal)
    result = cq.Workplane(plane).add(face).wires().toPending().offset2D(thick/2).extrude(thick).edges().fillet(thick/2-config.fix)


    return result