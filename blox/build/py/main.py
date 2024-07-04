import sys
sys.path.append('../../src/')

import os
from cadquery import Workplane, Sketch, Vector, Location, exporters
from blox.dir.dirs import dirs
from blox.dir.turn_dir import turn_right, turn_left, turn_back
from blox.slab.slab import slab
from blox.slab.blob import blob
from common.project import Project
import blox.config as config


walls = (slab([(0, 0, 0), (10, 0, 0), (10, 0, 10), (0, 0, 10)], 1)
        .add(slab([(0, 0, 0), (0, 10, 0), (0, 10, 10), (0, 0, 10)], 1))
        .clean()
    )




block = blob([(0, 0, 0), (10, 0, 0), (10, 0, 10), (10, 10, 10)], 1)

result = block
show_object(result)
exporters.export(result, Project.stl_dir() + "/main.stl")

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