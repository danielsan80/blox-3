import sys
sys.path.append('src/')

from cadquery import *
from cqkit import *
from cqgridfinity import *


def test_Gridfinity():
    grid = GridfinityBox(1, 1, 3, holes=True, no_lip=False, scoops=True, labels=True)
    assert True == True


