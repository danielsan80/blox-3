import sys

sys.path.append("../../src/")

from dataclasses import dataclass

from cadquery import Workplane

from triblox.block.functions import h
from triblox.block.Prism import Prism
from triblox.bowl.Bowl import Bowl
from triblox.helper.util import normalize_float
from triblox.mosaic.Mosaic import Mosaic
from triblox.tile.Tile import Tile


@dataclass(frozen=True)
class Spout:
    duct_d: float
    top_h: float

    def __post_init__(self):
        if self.duct_d <= 0:
            raise ValueError("Duct diameter must be greater than 0")
        if self.top_h <= 0:
            raise ValueError("Top height must be greater than 0")

        object.__setattr__(self, "duct_d", normalize_float(self.duct_d))
        object.__setattr__(self, "top_h", normalize_float(self.top_h))

    def get(self) -> Workplane:
        spout_bottom = (
            Mosaic()
            .add(Tile(0, 0))
            .add(Tile(1, 0))
            .add(Tile(2, 0))
            .add(Tile(3, 0))
            .add(Tile(-1, 0))
        )
        spout_top = spout_bottom.add(Tile(0, -1)).add(Tile(1, -1)).add(Tile(2, -1))

        spout = Bowl(spout_bottom, spout_top, 1)
        spout_border = Prism(spout_top, self.top_h / h(1))

        result = (
            Workplane("XY")
            .union(spout.get())
            .union(spout_border.get().translate((0, 0, h(1))))
        )

        return result
