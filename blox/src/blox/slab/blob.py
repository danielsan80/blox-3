import cadquery as cq
import blox.config as config

# Given 4 points make a solid

def blob(points):
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

