import sys
sys.path.append('src/')

from triblox.coord.resolveCoord import resolveCoord
from triblox.config import side
from math import sin

def test_coords_x():
    coords = [
        (-1, 0),
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),

        (100, 100),
        (101, 100),
    ]

    resolvedCoords = [
        ("down", (side/2,sin(60)*side), (-side/2,sin(60)*side), (0,0)),
        ("up", (0,0),(side,0), (side/2,sin(60)*side)),
        ("down", (3/2*side,sin(60)*side), (side/2,sin(60)*side), (side,0)),
        ("up", (side/2,sin(60)*side),(3/2*side,sin(60)*side), (side,sin(60)*2*side)),
        ("down", (side,sin(60)*2*side), (0,sin(60)*2*side), (side/2,sin(60)*side)),
        ("up", (-side/2,sin(60)*side),(side/2,sin(60)*side), (0,sin(60)*2*side)),

        ("up", (50*side,sin(60)*100*side),(51*side,sin(60)*100*side), (50.5*side,sin(60)*101*side)),
        ("down", (51.5*side,sin(60)*101*side),(50.5*side,sin(60)*101*side), (51*side,sin(60)*100*side)),
    ]

    for i, coord in enumerate(coords):
        resolvedCoord = resolveCoord(coord)
        assert resolvedCoords[i] == resolvedCoord

