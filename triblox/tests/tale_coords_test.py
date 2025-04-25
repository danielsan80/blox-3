import sys
sys.path.append('src/')

from triblox.coord.resolveCoord import resolveCoord
from triblox.config import side

from triblox.tale.Tale import Tale
from triblox.tale.Direction import Direction
from triblox.point.Point import Point
from triblox.math.dsin import dsin

def test_coords():
    tales = [
        Tale(0, 0),
        Tale(1, 0),
        Tale(-1, 0),
        Tale(1, 1),
        Tale(0, 1),
        Tale(-1, 1),

        Tale(100, 100),
        Tale(101, 100),
    ]

    expectedData = [
        (Direction.up(), Point(0,0), Point(side,0), Point(side/2,dsin(60)*side), Point(side/2,dsin(60)/3*side)),
        (Direction.down(), Point(3/2*side,dsin(60)*side), Point(side/2,dsin(60)*side), Point(side,0), Point(side,dsin(60)/3*2*side)),
        (Direction.down(), Point(side/2,dsin(60)*side), Point(-side/2,dsin(60)*side), Point(0,0), Point(0,dsin(60)/3*2*side)),
        (Direction.up(), Point(side/2,dsin(60)*side), Point(3/2*side,dsin(60)*side), Point(side,dsin(60)*2*side), Point(side,side*dsin(60)*4/3)),
        (Direction.down(), Point(side,dsin(60)*2*side), Point(0,dsin(60)*2*side), Point(side/2,dsin(60)*side), Point(side/2,side*dsin(60)*5/3)),
        (Direction.up(), Point(-side/2,dsin(60)*side), Point(side/2,dsin(60)*side), Point(0,dsin(60)*2*side), Point(0,side*dsin(60)*4/3)),

        (Direction.up(), Point(50*side,dsin(60)*100*side), Point(51*side,dsin(60)*100*side), Point(50.5*side,dsin(60)*101*side), Point(50.5*side,side*dsin(60)*301/3)),
        (Direction.down(), Point(51.5*side,dsin(60)*101*side), Point(50.5*side,dsin(60)*101*side), Point(51*side,dsin(60)*100*side), Point(51*side,side*dsin(60)*302/3)),
    ]

    for i, tale in enumerate(tales):
        data = (tale.direction(), tale.vertices().a, tale.vertices().b, tale.vertices().c, tale.incenter())
        assert expectedData[i] == data

