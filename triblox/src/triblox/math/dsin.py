import sys
sys.path.append('src/')

from math import sin, radians

def dsin(degrees: float) -> float:
    return sin(radians(degrees))

