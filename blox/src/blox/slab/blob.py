import cadquery as cq
import blox.config as config
import itertools
import logging


log = logging.getLogger(__name__)


def are_points_coplanar(points, tolerance=1e-6):

    if len(points) != 4:
        raise ValueError("You must provide exactly 4 points")

    ps = [cq.Vector(*p) for p in points]
    v1 = ps[1] - ps[0]
    v2 = ps[2] - ps[0]
    v3 = ps[3] - ps[0]

    return abs(v1.dot(v2.cross(v3))) < tolerance

def create_tetrahedron(points):
    if len(points) != 4:
        raise ValueError("You must provide exactly 4 points")

    faces = [
        cq.Face.makeFromWires(cq.Wire.makePolygon([points[0], points[1], points[2]]).close()),
        cq.Face.makeFromWires(cq.Wire.makePolygon([points[0], points[1], points[3]]).close()),
        cq.Face.makeFromWires(cq.Wire.makePolygon([points[1], points[2], points[3]]).close()),
        cq.Face.makeFromWires(cq.Wire.makePolygon([points[2], points[0], points[3]]).close())
    ]

    shell = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(shell)

def closest_point(point1, point2, tolerance=1e-6):
    p1 = cq.Vector(*point1)
    p2 = cq.Vector(*point2)

    direction = p2 - p1

    length = direction.Length

    return p1 + direction.multiply(tolerance)


def expand_solid_with_point(solid, point):
    log.info("E")

    oldPoints = [v.toTuple() for v in solid.Vertices()]

    newFaces = []

    for couple in itertools.combinations(oldPoints, 2):
        log.info(couple)
        newTriple = [couple[0], couple[1], point]

        if solid.isInside(closest_point(couple[0], point), tolerance=0):
            continue

        if solid.isInside(closest_point(couple[1], point), tolerance=0):
            continue

        wire = cq.Wire.makePolygon(newTriple).close()
        newFace = cq.Face.makeFromWires(wire)
        newFaces.append(newFace)

    allFaces = solid.Faces() + newFaces

    log.info(allFaces)
    shell = cq.Shell.makeShell(newFaces)

    return solid.append(cq.Solid.makeSolid(shell))


#                 if isPointInsideSolid(solid, centroid):
#                     continue
#
#
#
#     newTris = []
#     newFaces = solid.Faces()
#     log.info('E')
#     for face in solid.Faces():
#         log.info('F')
#         vertices = face.Vertices()
#         points = [v.toTuple() for v in vertices]
#         for tri in itertools.combinations(points, 2):
#             newTri = [tri[0], tri[1], point]
#             if newTri in newTris:
#                 continue
#             wire = cq.Wire.makePolygon(newTri).close()
#             newFace = cq.Face.makeFromWires(wire)
#             centroid = face.Center()
#
#             if isPointInsideSolid(solid, centroid):
#                 continue
#
#             newTris.append(newTri)
#             newFaces.append(newFace)
#
#
# #             wire = cq.Wire.makePolygon([tri[0], tri[1], point]).close()
# #             log.info('.')
# #             newFace = cq.Face.makeFromWires(wire)
# #             newFaces.append(newFace)
#     log.info(len(newTris))
#
#     allFaces = solid.Faces() + newFaces
#     shell = cq.Shell.makeShell(allFaces)
#     log.info(len(allFaces))
#     return cq.Solid.makeSolid(shell)

def create_convex_hull(points):

    for tetraPoints in itertools.combinations(points, 4):
        if not are_points_coplanar(tetraPoints):
            initialTetra = tetraPoints
            break
    else:
        raise ValueError("All points are coplanar")

    solid = create_tetrahedron(initialTetra)


    remainingPoints = [p for p in points if p not in initialTetra]
    for point in remainingPoints:
        solid = expand_solid_with_point(solid, point)

    return solid



def isPointInsideSolid(solid, point):
    return solid.isInside(point, tolerance=1e-6)
#
# def areFacesCoplanar(face1, face2, tolerance=1e-6):
#     normal1 = face1.normalAt()
#     normal2 = face2.normalAt()
#
#     if normal1.isParallel(normal2, tolerance):
#         # Check if the distance between the faces is zero
#         distance = face1.distanceTo(face2)
#         return distance < tolerance
#     return False
#

def blob(points):

    return create_convex_hull(points)
#
#     sets = list(itertools.combinations(points, 3))
#
#     faces = []
#
#     for set in sets:
#         wire = cq.Wire.makePolygon(set).close()
#         face = cq.Face.makeFromWires(wire)
#
#         centroid = face.Center()
#
#         newFaces = faces.copy()
#         newFaces.append(face)
#
#         envelope = cq.Solid.makeSolid(cq.Shell.makeShell(newFaces))
#
#         if not isPointInsideSolid(envelope, centroid):
#             faces.append(face)
#
#     mergedFaces = []
# #     while faces:
# #         face = faces.pop()
# #         coplanarFaces = [f for f in faces if areFacesCoplanar(face, f)]
# #
# #         for f in coplanarFaces:
# #             faces.remove(f)
# #             newEdges = list(face.outerWire().Edges()) + list(f.outerWire().Edges())
# #             newWire = cq.Wire.makePolygon([edge.Vertex1.Point() for edge in newEdges]).close()
# #             face = cq.Face.makeFromWires(newWire)
# #
# #             mergedFaces.append(face)
#
#     shell = cq.Shell.makeShell(mergedFaces)
#     return cq.Solid.makeSolid(shell).clean()
