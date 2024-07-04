import sys
sys.path.append('../../src/')

import os
from cadquery import Workplane, Sketch, Vector, Location, exporters
from blox.dir.dirs import dirs
from blox.dir.turn_dir import turn_right, turn_left, turn_back
from blox.slab.slab import slab, slab3d
from common.project import Project
# from blox.config import *
#
#
# print(config.fix)

# result = (
#     Workplane("front")
#     .rect(10, 10)
#     .extrude(10)
# )
#
# slab = slab([(0, 0), (10, 0), (10, 10), (0, 10), (0,0)], 1)
# slab = slab.rotate((0, 0, 0), (0, 1, 0), 45)

# show_object(slab)


walls = (slab3d([(0, 0, 0), (10, 0, 0), (10, 0, 10), (0, 0, 10)], 1)
        .add(slab3d([(0, 0, 0), (0, 10, 0), (0, 10, 10), (0, 0, 10)], 1))
        .clean()
    )
# walls = walls.union(
show_object(walls)

exporters.export(walls, Project.stl_dir() + "/main.stl")
# show_object(result)



#
# def box(face):
#     origin = face.Center()
#     normal = face.normalAt()
#     x_dir = cq.Vector(0, 0, 1).cross(normal)
#     plane = cq.Plane(origin, x_dir, normal)
#     loc = cq.Location(plane)
#     box = cq.Solid.makeBox(2, 1, 1, pnt=cq.Vector(-1, -0.5, 0)).located(loc)
#     return box
#
#
# result = (
#     cq.Workplane()
#     .polygon(8, 10)
#     .extrude(5)
# )
# result = result.union(
#     result
#     .faces("#Z")
#     .each(box)
# )