from pathlib import Path
from functools import cached_property
from aoc_utils import Point, StringMap


data = (Path(__file__).parent.parent / "data/day12.txt").read_text().strip()


class Map(StringMap):
    @cached_property
    def region_names(self):
        seen = set()
        for ch in self.m.values():
            if ch not in seen:
                yield ch
                seen.add(ch)

    def dirs(self, point, allow_none=False):
        for dir in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            npoint = point + dir
            ch = self.m.get(npoint, None)
            if ch is not None or allow_none:
                yield npoint, ch

    def flood(self, point: Point):
        seen = set()
        stack = [point]
        start_ch = self.m[point]
        while stack:
            point = stack.pop()
            if point in seen:
                continue
            if self.m[point] != start_ch:
                continue
            seen.add(point)
            for npoint, _ in self.dirs(point):
                stack.append(npoint)
        return seen

    @property
    def regions(self):
        seen_region_points = set()
        regions = []
        for point in self.m:
            if point in seen_region_points:
                continue
            else:
                points = self.flood(point)
                seen_region_points |= points
                regions.append((self.m[point], points))
        return regions

    def get_area(self, region: set[Point]):
        return len(region)

    def check_perimeter(self, point: Point):
        for dir in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yield point + dir, dir

    def get_perimeter(self, region: set[Point]):
        perimeter = set()
        for point in region:
            for npoint, dir in self.check_perimeter(point):
                if npoint not in region:
                    perimeter.add((npoint, dir))
        return perimeter

    def number_of_sides(self, perimeter: set[tuple[Point, tuple[int, int]]]):
        seen = set()
        sides = []
        for point, dir in perimeter:
            if (point, dir) in seen:
                continue
            edge = set()
            stack = [point]
            if dir in [(1, 0), (-1, 0)]:
                moves = [(0, 1), (0, -1)]
            else:
                moves = [(1, 0), (-1, 0)]
            while stack:
                current_point = stack.pop()
                if (current_point, dir) not in perimeter:
                    continue
                if (current_point, dir) in seen:
                    continue
                seen.add((current_point, dir))
                if current_point in edge:
                    continue
                edge.add(current_point)
                for move in moves:
                    npoint = current_point + move
                    stack.append(npoint)
            sides.append(edge)
        return sides

    def costs(self, new=False):
        costs = {}
        for ch, region in self.regions:
            if ch not in costs:
                costs[ch] = 0
            area = self.get_area(region)
            perimeter = self.get_perimeter(region)
            if new:
                perimeter_val = len(self.number_of_sides(perimeter))
            else:
                perimeter_val = len(perimeter)
            costs[ch] += area * perimeter_val
        return costs


m = Map(data)
print(sum(m.costs().values()))
print(sum(m.costs(new=True).values()))
