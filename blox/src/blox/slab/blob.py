import cadquery as cq
import blox.config as config

def blob(points, thick):
    pointsByFaces = [
        [points[0], points[1], points[2]],
        [points[0], points[2], points[3]],
        [points[0], points[1], points[3]],
        [points[1], points[2], points[3]]
    ]

    faces = []

    for pointsByFace in pointsByFaces:
        wire = cq.Wire.makePolygon(pointsByFace).close()
        faces.append(cq.Face.makeFromWires(wire))

    shell = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(shell)

#
#     origin = face.Center()
#     normal = face.normalAt()
#     face = face.translate((normal.x * -thick/2, normal.y * -thick/2, normal.z * -thick/2))
#     xDir = cq.Vector(0, 0, 1).cross(normal)
#     plane = cq.Plane(origin, xDir, normal)
#     result = cq.Workplane(plane).add(face).wires().toPending().offset2D(thick/2).extrude(thick).edges().fillet(thick/2-config.fix)
#
#
#     return result