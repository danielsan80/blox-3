from math import sin, radians

def dsin(degrees: float) -> float:
    return sin(radians(degrees))

sin60 = dsin(60)

def normalize_float(value: float) -> float:
    return abs(float(value)) * (1 if value >= 0 else -1)

def hypotenuse(c1: float, c2: float) -> float:
    return normalize_float((c1 ** 2 + c2 ** 2) ** 0.5)

def cathetus(h: float, c: float) -> float:
    return normalize_float((h ** 2 - c ** 2) ** 0.5)