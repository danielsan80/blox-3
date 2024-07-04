from . dirs import dirs

def turn_right(dir):
    return dirs()[(dirs().index(dir) + 1) % 4]

def turn_left(dir):
    return dirs()[(dirs().index(dir) + 3) % 4]

def turn_back(dir):
    return dirs()[(dirs().index(dir) + 2) % 4]