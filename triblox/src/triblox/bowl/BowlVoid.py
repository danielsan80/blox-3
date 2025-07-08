import sys

sys.path.append("../../src/")

from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, List

from cadquery import Sketch, Workplane

from triblox.block.functions import h
from triblox.caching.CacheBase import CacheBase
from triblox.caching.CachedResult import CachedResult
from triblox.config import clr, fix, wall_w
from triblox.geometry.Point import Point
from triblox.helper.util import normalize_float, sin60
from triblox.mosaic.Mosaic import Mosaic
from triblox.mosaic.PlacedTile import PlacedTile
from typing import Optional


@dataclass(frozen=True)
class BaseCol:
    top_tile: PlacedTile
    bottom_tile: PlacedTile


@dataclass(frozen=True)
class EdgeCol:
    top_tile: PlacedTile
    base_top_tile: PlacedTile


@dataclass(frozen=True)
class VertexCol:
    top_tile: PlacedTile
    base_top_tile: PlacedTile


@dataclass(frozen=True)
class ClassifiedCols:
    base: Dict[str, List[BaseCol]]
    edge: Dict[str, List[EdgeCol]]
    vertex: Dict[str, List[VertexCol]]


@dataclass(frozen=True)
class BowlVoid:
    mosaic_bottom: Mosaic
    mosaic_top: Mosaic
    hu: float
    wall_thick: Optional[float] = None
    bottom_thick: Optional[float] = None

    def __post_init__(self):
        if self.hu <= 0:
            raise ValueError("Height units must be greater than 0")
        if self.wall_thick is None:
            object.__setattr__(self, "wall_thick", wall_w)
        if self.wall_thick <= 0:
            raise ValueError("Wall thick must be greater than 0")
        if self.bottom_thick is None:
            object.__setattr__(self, "bottom_thick", self.wall_thick)
        if self.bottom_thick < 0:
            raise ValueError("Bottom thick must be positive or zero")
        object.__setattr__(self, "hu", normalize_float(self.hu))
        object.__setattr__(self, "wall_thick", normalize_float(self.wall_thick))
        object.__setattr__(self, "bottom_thick", normalize_float(self.bottom_thick))

        if (self.bottom_thick > self.wall_thick):
            raise ValueError("Bottom thick must be less than or equal to wall thick")

    def get(self) -> Workplane:
        result = Workplane("XY")

        cache_base = (
            CacheBase()
            .add_owner(self)
            .add_mosaic(self.mosaic_bottom)
            .add_mosaic(self.mosaic_top)
            .add("hu", self.hu)
            .add("wall_thick", self.wall_thick)
            .add("bottom_thick", self.bottom_thick)
        )

        cached_result = CachedResult(cache_base, result)

        classified_cols = self._classified_cols()

        for key, base_cols in classified_cols.base.items():
            placed_tile = base_cols[0].top_tile
            if cached_result.has(placed_tile):
                cached_result.add(placed_tile)
                continue
            result = cached_result.get()
            for base_col in base_cols:
                result = self._add_pillar(result, base_col)
            cached_result.add(base_col.top_tile, result)

        for key, edge_cols in classified_cols.edge.items():
            placed_tile = edge_cols[0].top_tile
            if cached_result.has(placed_tile):
                cached_result.add(placed_tile)
                continue
            result = cached_result.get()
            for edge_col in edge_cols:
                result = self._add_edge_overhang(result, edge_col)
            cached_result.add(edge_col.top_tile, result)

        for key, vertex_cols in classified_cols.vertex.items():
            placed_tile = vertex_cols[0].top_tile
            if cached_result.has(placed_tile):
                cached_result.add(placed_tile)
                continue
            result = cached_result.get()
            for vertex_col in vertex_cols:
                result = self._add_vertex_overhang(result, vertex_col)
            cached_result.add(vertex_col.top_tile, result)

        result = cached_result.get()

        return result

    def _classified_cols(self) -> ClassifiedCols:

        top_tiles = self.mosaic_top.placed_tiles
        bottom_tiles = self.mosaic_bottom.placed_tiles

        base_cols = defaultdict(list)
        edge_cols = defaultdict(list)
        vertex_cols = defaultdict(list)

        _top_tiles = top_tiles
        unhandled_top_tiles = {}

        for key, top_tile in _top_tiles.items():
            if key in bottom_tiles:
                base_cols[key].append(BaseCol(top_tile, bottom_tiles[key]))
            else:
                unhandled_top_tiles[key] = top_tile

        _top_tiles = unhandled_top_tiles
        unhandled_top_tiles = {}

        base_top_tiles = [
            base_col.top_tile for values in base_cols.values() for base_col in values
        ]

        for key, top_tile in _top_tiles.items():
            adjacent_base_top_tiles = self._adjacent_tiles(top_tile, base_top_tiles)
            for base_top_tile in adjacent_base_top_tiles:
                edge_cols[key].append(EdgeCol(top_tile, base_top_tile))
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
                    current_top_tile, base_top_tiles
                )

                if adjacent_base_top_tiles:
                    for base_top_tile in adjacent_base_top_tiles:
                        if top_tile.common_points(base_top_tile):
                            vertex_cols[key].append(VertexCol(top_tile, base_top_tile))
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

        return ClassifiedCols(
            base_cols,
            edge_cols,
            vertex_cols,
        )

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

    def _tile_points(self, placed_tile: PlacedTile, thick: float = 0) -> list[tuple[float, float]]:
        points = placed_tile.vertices.offset_points(clr+thick, to6=True)
        points = [point.to_tuple() for point in points]
        return points

    def _tile_points_on_edge(
        self, placed_tile: PlacedTile, edge_points: list[Point], thick: float = 0
    ) -> list[tuple[float, float]]:
        all_points = []
        vertices = placed_tile.vertices.to_list()

        for i in range(3):
            vertex = vertices[i]

            if vertex.original_points()[0] not in edge_points:
                continue

            previous_vertex = vertices[(i - 1) % 3]
            previous_point = previous_vertex.offset_points(clr+thick)[-1]

            next_vertex = vertices[(i + 1) % 3]
            next_point = next_vertex.offset_points(clr+thick)[0]

            points = vertex.offset_points(clr+thick)

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
        self, placed_tile: PlacedTile, vertex_point: Point, thick: float = 0
    ) -> list[tuple[float, float]]:
        vertices = placed_tile.vertices.to_list()

        for i in range(3):
            vertex = vertices[i]

            if not vertex.original_points()[0] == vertex_point:
                continue

            previous_vertex = vertices[(i - 1) % 3]
            previous_point = previous_vertex.offset_points(clr+thick)[-1]

            next_vertex = vertices[(i + 1) % 3]
            next_point = next_vertex.offset_points(clr+thick)[0]

            points = vertex.offset_points(clr+thick)

            if len(points) == 1:
                points += [points[-1].move(next_point, fix)]

            points += [points[-1].move(next_point, fix)]
            points += [points[-1].move(next_point, fix)]

            points = [points[0].move(previous_point, fix)] + points
            points = [points[0].move(previous_point, fix)] + points

        points = [point.to_tuple() for point in points]

        return points

    def _add_pillar(self, result: Workplane, base_col: BaseCol) -> Workplane:
        top_tile = base_col.top_tile
        bottom_tile = base_col.bottom_tile

        bottom_sketch = Sketch().polygon(self._tile_points(bottom_tile, max(self.wall_thick - self.bottom_thick, 0)))
        top_sketch = Sketch().polygon(self._tile_points(top_tile, self.wall_thick))

        wp_bottom = (
            Workplane("XY")
            .transformed(offset=(0, 0, self.bottom_thick))
            .placeSketch(bottom_sketch)
        )
        wp_bottom_ext = (
            Workplane("XY")
            .transformed(offset=(0, 0, self.wall_thick))
            .transformed(offset=(0, 0, clr / sin60))
            .placeSketch(top_sketch)
        )

        wp_top = (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.hu)))
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

    def _add_edge_overhang(self, result: Workplane, edge_col: EdgeCol) -> Workplane:
        top_tile = edge_col.top_tile
        base_top_tile = edge_col.base_top_tile
        edge_points = []
        for point in top_tile.tile.vertices.to_list():
            if point in base_top_tile.tile.vertices.to_list():
                edge_points += [point]

        if len(edge_points) != 2:
            raise ValueError("Edge point not found")

        bottom_sketch = Sketch().polygon(
            self._tile_points_on_edge(top_tile, edge_points, self.wall_thick)
        )
        top_sketch = Sketch().polygon(self._tile_points(top_tile, self.wall_thick))

        wp_bottom = (
            Workplane("XY")
            .transformed(offset=(0, 0, self.wall_thick))
            .transformed(offset=(0, 0, clr / sin60))
            .placeSketch(bottom_sketch)
        )
        wp_top = (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.hu)))
            .placeSketch(top_sketch)
        )

        try:
            loft = wp_bottom.add(wp_top).loft(combine=True)
            return result.union(loft)
        except Exception as e:
            print(f"Failed Loft: {e}")
            return result

    def _add_vertex_overhang(
        self, result: Workplane, vertex_col: VertexCol
    ) -> Workplane:
        top_tile = vertex_col.top_tile
        base_top_tile = vertex_col.base_top_tile

        common_points = top_tile.common_points(base_top_tile)

        if len(common_points) != 1:
            raise ValueError("Vertex point not found")

        vertex_point = common_points[0]

        bottom_sketch = Sketch().polygon(
            self._tile_points_on_vertex(top_tile, vertex_point, self.wall_thick)
        )
        top_sketch = Sketch().polygon(self._tile_points(top_tile, self.wall_thick))

        wp_bottom = (
            Workplane("XY")
            .transformed(offset=(0, 0, self.wall_thick))
            .transformed(offset=(0, 0, clr / sin60))
            .placeSketch(bottom_sketch)
        )
        wp_top = (
            Workplane("XY")
            .transformed(offset=(0, 0, h(self.hu)))
            .placeSketch(top_sketch)
        )
        try:
            loft = wp_bottom.add(wp_top).loft(combine=True)
            result = result.union(loft)
        except Exception as e:
            print(f"Failed Loft: {e}")
            result = result

        return result
