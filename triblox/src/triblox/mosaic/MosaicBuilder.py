import sys

sys.path.append("src/")

from dataclasses import dataclass, field

from triblox.mosaic.Mosaic import Mosaic
from triblox.tile.Tile import Tile


@dataclass(frozen=True)
class MosaicBuilder:
    mosaic: Mosaic = field(init=False)
    current: Tile = field(init=False)
    pending: list[Tile] = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "mosaic", Mosaic())
        object.__setattr__(self, "current", Tile(0, 0))
        object.__setattr__(self, "pending", [])

    def build(self) -> "Mosaic":
        builder = self._place_pending()
        return builder.mosaic

    def tile(self, x: int, y: int) -> "MosaicBuilder":
        tile = Tile(x, y)
        mosaic = self.mosaic
        pending = self.pending.copy()
        builder = MosaicBuilder()

        if not self.mosaic.contains(tile):
            if mosaic.is_empty() or mosaic.is_adjacent(tile):
                mosaic = mosaic.add(tile)
            else:
                pending = pending + [tile]

        object.__setattr__(builder, "mosaic", mosaic)
        object.__setattr__(builder, "current", tile)
        object.__setattr__(builder, "pending", pending)
        return builder

    def merge_mosaic(self, mosaic: Mosaic) -> "MosaicBuilder":
        builder = self
        for tile in mosaic.tiles.values():
            builder = builder.tile(tile.x, tile.y)
        return builder

    def move(self, x: int, y: int) -> "MosaicBuilder":
        tile = Tile(x, y)
        builder = MosaicBuilder()
        object.__setattr__(builder, "mosaic", self.mosaic)
        object.__setattr__(builder, "current", tile)
        object.__setattr__(builder, "pending", self.pending)
        return builder

    def move_right(self, length: int = 1) -> "MosaicBuilder":
        tile = self.current
        return self.move(tile.x + length, tile.y)

    def move_left(self, length: int = 1) -> "MosaicBuilder":
        tile = self.current
        return self.move(tile.x - length, tile.y)

    def move_up(self, length: int = 1) -> "MosaicBuilder":
        tile = self.current
        return self.move(tile.x, tile.y + length)

    def move_down(self, length: int = 1) -> "MosaicBuilder":
        tile = self.current
        return self.move(tile.x, tile.y - length)

    def here(self) -> "MosaicBuilder":
        return self.tile(self.current.x, self.current.y)

    def origin(self) -> "MosaicBuilder":
        return self.tile(0, 0)

    def right(self) -> "MosaicBuilder":
        tile = self.current.right()
        return self.tile(tile.x, tile.y)

    def left(self) -> "MosaicBuilder":
        tile = self.current.left()
        return self.tile(tile.x, tile.y)

    def up(self) -> "MosaicBuilder":
        tile = self.current.up()
        return self.tile(tile.x, tile.y)

    def down(self) -> "MosaicBuilder":
        tile = self.current.down()
        return self.tile(tile.x, tile.y)

    def hex(self) -> "MosaicBuilder":
        tile = self.current
        return self.here().right().up().left().left().down().move(tile.x, tile.y)

    def line_hor(self, length: int) -> "MosaicBuilder":
        if length == 0:
            return self

        builder = self
        if length > 0:
            for _ in range(length):
                builder = builder.right()
        if length < 0:
            for _ in range(-length):
                builder = builder.left()
        return builder

    def line_asc(self, length: int) -> "MosaicBuilder":
        if length == 0:
            return self

        builder = self
        if length > 0:
            flag = 0 if self.current.direction.is_up() else 1
            for i in range(length):
                if i % 2 == flag:
                    builder = builder.right()
                else:
                    builder = builder.up()
        if length < 0:
            flag = 1 if self.current.direction.is_up() else 0
            for i in range(-length):
                if i % 2 == flag:
                    builder = builder.left()
                else:
                    builder = builder.down()
        return builder

    def line_desc(self, length: int) -> "MosaicBuilder":
        if length == 0:
            return self

        builder = self
        if length > 0:
            flag = 0 if self.current.direction.is_up() else 1
            for i in range(length):
                if i % 2 == flag:
                    builder = builder.down()
                else:
                    builder = builder.right()
        if length < 0:
            flag = 1 if self.current.direction.is_up() else 0
            for i in range(-length):
                if i % 2 == flag:
                    builder = builder.up()
                else:
                    builder = builder.left()
        return builder

    def _try_place_pending(self) -> "MosaicBuilder":
        mosaic = self.mosaic
        pending = self.pending.copy()
        _pending = []

        while len(pending) > 0:
            tile = pending.pop(0)
            if mosaic.is_adjacent(tile):
                mosaic = mosaic.add(tile)
            else:
                _pending += [tile]

        builder = MosaicBuilder()
        object.__setattr__(builder, "mosaic", mosaic)
        object.__setattr__(builder, "current", self.current)
        object.__setattr__(builder, "pending", _pending)
        return builder

    def _place_pending(self) -> "MosaicBuilder":
        builder = self
        i = 0
        while len(builder.pending) > 0:
            builder = builder._try_place_pending()
            i += 1

            if i > 100:
                raise ValueError("Some tiles are not adjacent to the mosaic")

        return builder
