import sys
sys.path.append('src/')

from triblox.config import side

from triblox.tile.Tile import Tile
from triblox.tile.Direction import Direction
from triblox.geometry.Point import Point
from triblox.helper.util import dsin

def test_it_can_move_a_Point_to_another_Point_of_a_given_value():
    origin = Point(0, 0)
    destination = Point(1, 1)

    assert origin.move(destination, 1) == Point(dsin(45), dsin(45))

def test_it_can_be_converted_to_a_tuple():
    point = Point(1, 2)
    assert point.to_tuple() == (1, 2)

