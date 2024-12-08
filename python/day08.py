from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass
from typing import Self

data = (Path(__file__).parent.parent / "data/day08.txt").read_text()

# data = """............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: Self | tuple[int, int]):
        if isinstance(other, tuple):
            x = other[0]
            y = other[1]
        else:
            x = other.x
            y = other.y
        return self.__class__(self.x + x, self.y + y)

    def __sub__(self, other: Self | tuple[int, int]):
        if isinstance(other, tuple):
            x = other[0]
            y = other[1]
        else:
            x = other.x
            y = other.y
        return self.__add__(self.__class__(-x, -y))

    def copy(self):
        return self.__class__(self.x, self.y)


class Map:
    def __init__(self, data):
        self.m, self.max_x, self.max_y = self.parse(data)
        self.antennas = self.get_antennas()
        self.antinodes = self.get_antinodes()

    def parse(self, data):
        m: dict[Point, str] = {}
        max_x = max_y = 0
        for y, row in enumerate(data.splitlines()):
            max_y = max(max_y, y)
            for x, ch in enumerate(row):
                m[Point(x, y)] = ch
                max_x = max(max_x, x)
        return m, max_x, max_y

    def get_antennas(self):
        antennas: dict[str, set[Point]] = defaultdict(set)
        for coord, ch in self.m.items():
            if ch != ".":
                antennas[ch].add(coord)
        return antennas

    def calc_dist(self, coord1: Point, coord2: Point):
        return coord2 - coord1

    def calc_t_antinodes(self, p1, p2):
        dist = self.calc_dist(p1, p2)
        antinodes = {p1, p2}
        current = p1
        while 0 <= current.x <= self.max_x and 0 <= current.y <= self.max_y:
            antinodes.add(current)
            current -= dist

        current = p2
        while 0 <= current.x <= self.max_x and 0 <= current.y <= self.max_y:
            antinodes.add(current)
            current += dist
        return antinodes

    def get_t_antinodes(self):
        antinodes = set()
        for locations in self.antennas.values():
            locations = list(locations)
            for i, loc in enumerate(locations):
                for other_loc in locations[i + 1 :]:
                    antinodes |= self.calc_t_antinodes(loc, other_loc)
        return antinodes

    def get_antinodes(self):
        antinodes = defaultdict(set)
        for node, locations in self.antennas.items():
            locations = list(locations)
            for i, loc in enumerate(locations):
                for other_loc in locations[i + 1 :]:
                    dist = self.calc_dist(loc, other_loc)
                    antinode1 = other_loc + dist
                    antinode2 = loc - dist
                    for a in (antinode1, antinode2):
                        if (0 <= a.x <= self.max_x) and (0 <= a.y <= self.max_y):
                            antinodes[node].add(a)
        return antinodes


m = Map(data)
unique_antinodes = set().union(*m.antinodes.values())
print(len(unique_antinodes))
print(len(m.get_t_antinodes()))
