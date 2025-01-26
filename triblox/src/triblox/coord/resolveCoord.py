import sys
sys.path.append('src/')

from math import sin
from triblox.config import side

def resolveCoord(coord):

    if (coord[0]+coord[1]) % 2 == 0:
        versus = "up"
        a = (coord[0]/2*side, coord[1]*sin(60)*side)
        b = (a[0]+side, coord[1]*sin(60)*side)
        c = (a[0]+side/2, a[1]+side*sin(60))
    else:
        versus = "down"
        a = ((0.5+(coord[0]+1)/2)*side, (coord[1]+1)*sin(60)*side)
        b = (a[0]-side, (coord[1]+1)*sin(60)*side)
        c = (a[0]-side/2, a[1]-side*sin(60))

    return (versus, a, b, c)
