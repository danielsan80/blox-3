import blox.config as config
import cadquery as cq

def xDir(vector: cq.Vector) -> cq.Vector:
    normal = vector.normalized()

    if (normal == cq.Vector(0, 0, 1)):
        xDir = cq.Vector(1, 0, 0)
    elif (normal == cq.Vector(0, 0, -1)):
        xDir = cq.Vector(1, 0, 0)
    else:
        xDir = cq.Vector(0, 0, 1).cross(normal)

    return xDir