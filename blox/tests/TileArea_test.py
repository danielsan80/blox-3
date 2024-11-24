import sys
sys.path.append('src/')

from blox.dir.dirs import dirs

from tiles.tile.TileCoord import TileCoord
from tiles.area.TileArea import TileArea

def test_TileArea():
    coords = [
        TileCoord(0, 0),
        TileCoord(0, 4),
        TileCoord(-2, 4),
        TileCoord(-2, 6),
        TileCoord(4, 6),
        TileCoord(4, 0)
    ]
    expected_result = [
        ["north", 4, [0, 0], ["bottom", "bottom"], "right"],
        ["west", 2, [0, 4], ["top", "top"], "left"],
        ["north", 2, [-2, 4], ["bottom", "top"], "right"],
        ["east", 6, [-2, 6], ["bottom", "top"], "right"],
        ["south", 6, [4, 6], ["bottom", "top"], "right"],
        ["west", 4, [4, 0], ["bottom", "top"], "right"]
    ]


    area = TileArea(coords)

    assert True == True
