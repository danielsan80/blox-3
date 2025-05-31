import sys

sys.path.append("../../src/")

from dataclasses import dataclass
from pprint import pprint

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.config import clr, fix
from triblox.geometry.Point import Point
from triblox.helper.util import normalize_float, sin60
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile


@dataclass(frozen=True)
class Tunnel:
    mosaic_bottom: Mosaic
    mosaic_top: Mosaic
    h: float

    def __post_init__(self):
        if self.h <= 0:
            raise ValueError("Height must be greater than 0")
        object.__setattr__(self, "h", normalize_float(self.h))

    def get(self) -> Workplane:
        result = Workplane("XY")

        top_tiles = self.mosaic_top.placed_tiles
        bottom_tiles = self.mosaic_bottom.placed_tiles

        base_top_tiles = {}
        edge_top_tiles = {}
        vertex_top_tiles = {}

        _top_tiles = top_tiles
        unhandled_top_tiles = {}

        for key, top_tile in _top_tiles.items():
            if key in bottom_tiles:
                result = self._add_pillar(result, bottom_tiles[key], top_tile)
                base_top_tiles[key] = top_tile
            else:
                unhandled_top_tiles[key] = top_tile

        _top_tiles = unhandled_top_tiles
        unhandled_top_tiles = {}

        for key, top_tile in _top_tiles.items():
            adjacent_base_top_tiles = self._adjacent_tiles(
                top_tile, base_top_tiles.values()
            )
            for base_tile in adjacent_base_top_tiles:
                result = self._add_edge_overhang(result, base_tile, top_tile)
                edge_top_tiles[key] = top_tile
            if not adjacent_base_top_tiles:
                unhandled_top_tiles[key] = top_tile

        _top_tiles = unhandled_top_tiles
        unhandled_top_tiles = {}

        for key, top_tile in _top_tiles.items():
            visited = []
            stack = [top_tile]

            found = False
            while stack:
                current_top_tile = stack.pop()

                if current_top_tile in visited:
                    continue
                visited.append(current_top_tile)

                adjacent_base_top_tiles = self._adjacent_tiles(
                    current_top_tile, base_top_tiles.values()
                )

                if adjacent_base_top_tiles:
                    for base_top_tile in adjacent_base_top_tiles:
                        if top_tile.common_points(base_top_tile):
                            result = self._add_vertex_overhang(
                                result, top_tile, base_top_tile
                            )
                            vertex_top_tiles[key] = current_top_tile
                            found = True
                else:
                    adjacent_edge_top_tiles = self._adjacent_tiles(
                        current_top_tile, top_tiles.values()
                    )
                    for edge_top_tile in adjacent_edge_top_tiles:
                        if edge_top_tile not in visited:
                            stack.append(edge_top_tile)

            if not found:
                unhandled_top_tiles[key] = top_tile

        if len(unhandled_top_tiles) > 0:
            pprint(f"Unhandled top tiles: {len(unhandled_top_tiles)}")

        return result.clean()

    def _adjacent_tiles(
        self, placed_tile: PlacedTile, other_placed_tiles: list[PlacedTile]
    ) -> list[PlacedTile]:
        adjacent_tiles = []
        for other_placed_tile in other_placed_tiles:
            if other_placed_tile.tile.coord == placed_tile.tile.coord:
                continue
            if other_placed_tile.tile.is_adjacent(placed_tile.tile):
                adjacent_tiles += [other_placed_tile]
        return adjacent_tiles

    def _tile_points(self, placed_tile: PlacedTile) -> list[tuple[float, float]]:
        points = placed_tile.vertices.offset_points(clr, to6=True)
        points = [point.to_tuple() for point in points]
        return points

    def _tile_points_on_edge(
        self, placed_tile: PlacedTile, edge_points: list[Point]
    ) -> list[tuple[float, float]]:

        all_points = []
        vertices = placed_tile.vertices.to_list()

        for i in range(3):
            vertex = vertices[i]

            if vertex.original_points()[0] not in edge_points:
                continue

            previous_vertex = vertices[(i - 1) % 3]
            previous_point = previous_vertex.offset_points(clr)[-1]

            next_vertex = vertices[(i + 1) % 3]
            next_point = next_vertex.offset_points(clr)[0]

            points = vertex.offset_points(clr)

            if len(points) == 1:
                points += [points[-1].move(next_point, fix)]

            if next_vertex.original_points()[0] not in edge_points:
                points += [points[-1].move(next_point, fix)]

            if previous_vertex.original_points()[0] not in edge_points:
                points = [points[0].move(previous_point, fix)] + points

            all_points += points

        all_points = [point.to_tuple() for point in all_points]

        return all_points

    def _tile_points_on_vertex(
        self, placed_tile: PlacedTile, vertex_point: Point
    ) -> list[tuple[float, float]]:

        vertices = placed_tile.vertices.to_list()

        for i in range(3):
            vertex = vertices[i]

            if not vertex.original_points()[0] == vertex_point:
                continue

            previous_vertex = vertices[(i - 1) % 3]
            previous_point = previous_vertex.offset_points(clr)[-1]

            next_vertex = vertices[(i + 1) % 3]
            next_point = next_vertex.offset_points(clr)[0]

            points = vertex.offset_points(clr)

            if len(points) == 1:
                points += [points[-1].move(next_point, fix)]

            points += [points[-1].move(next_point, fix)]
            points += [points[-1].move(next_point, fix)]

            points = [points[0].move(previous_point, fix)] + points
            points = [points[0].move(previous_point, fix)] + points

        points = [point.to_tuple() for point in points]

        return points

    def _add_pillar(
        self, result: Workplane, bottom_tile: PlacedTile, top_tile: PlacedTile
    ) -> Workplane:
        bottom_sketch = Sketch().polygon(self._tile_points(bottom_tile))
        top_sketch = Sketch().polygon(self._tile_points(top_tile))

        wp_bottom = Workplane("XY").placeSketch(bottom_sketch)
        wp_bottom_ext = (
            Workplane("XY")
            .transformed(offset=(0, 0, clr / sin60))
            .placeSketch(top_sketch)
        )

        wp_top = (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.h)))
            .placeSketch(top_sketch)
        )

        try:
            loft1 = wp_bottom.add(wp_bottom_ext).loft(combine=True)
            loft2 = wp_bottom_ext.add(wp_top).loft(combine=True)
            result = result.union(loft1)
            result = result.union(loft2)
        except Exception as e:
            print(f"Failed Loft: {e}")

        return result

    def _add_edge_overhang(
        self, result: Workplane, base_top_tile: PlacedTile, top_tile: PlacedTile
    ) -> Workplane:
        edge_points = []
        for point in top_tile.tile.vertices.to_list():
            if point in base_top_tile.tile.vertices.to_list():
                edge_points += [point]

        if len(edge_points) != 2:
            raise ValueError("Edge point not found")

        bottom_sketch = Sketch().polygon(
            self._tile_points_on_edge(top_tile, edge_points)
        )
        top_sketch = Sketch().polygon(self._tile_points(top_tile))

        wp_bottom = (
            Workplane("XY")
            .transformed(offset=(0, 0, clr / sin60))
            .placeSketch(bottom_sketch)
        )
        wp_top = (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.h)))
            .placeSketch(top_sketch)
        )

        try:
            loft = wp_bottom.add(wp_top).loft(combine=True)
            return result.union(loft)
        except Exception as e:
            print(f"Failed Loft: {e}")
            return result

    def _add_vertex_overhang(
        self, result: Workplane, top_tile: PlacedTile, base_top_tile: PlacedTile
    ) -> Workplane:
        common_points = top_tile.common_points(base_top_tile)

        if len(common_points) != 1:
            raise ValueError("Vertex point not found")

        vertex_point = common_points[0]

        bottom_sketch = Sketch().polygon(
            self._tile_points_on_vertex(top_tile, vertex_point)
        )
        top_sketch = Sketch().polygon(self._tile_points(top_tile))

        wp_bottom = (
            Workplane("XY")
            .transformed(offset=(0, 0, clr / sin60))
            .placeSketch(bottom_sketch)
        )
        wp_top = (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.h)))
            .placeSketch(top_sketch)
        )
        try:
            loft = wp_bottom.add(wp_top).loft(combine=True)
            result = result.union(loft)
        except Exception as e:
            print(f"Failed Loft: {e}")
            result = result

        return result
