from pathlib import Path
from dataclasses import dataclass
from typing import Self

data = (Path(__file__).parent.parent / "data/day10.txt").read_text().strip()

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

    def parse(self, data):
        m: dict[Point, int] = {}
        max_x = max_y = 0
        for y, row in enumerate(data.splitlines()):
            max_y = max(max_y, y)
            for x, ch in enumerate(row):
                m[Point(x, y)] = int(ch)
                max_x = max(max_x, x)
        return m, max_x, max_y

    @property
    def starts(self):
        yield from (key for key, val in self.m.items() if val == 0)

    def dirs(self, coord):
        for other in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            ncoord = coord + other
            if n := self.m.get(ncoord, None):
                yield coord + other, n

    def trailheads_at(self, coord, find_all=False):
        trails = []
        stack = [[coord]]
        ends_found = set()
        while stack:
            trail = stack.pop()
            coord = trail[-1]
            current_n = self.m[coord]
            if current_n == 9:
                if coord in ends_found and not find_all:
                    continue
                else:
                    ends_found.add(coord)
                trails.append(trail)
                continue
            for ncoord, n2 in self.dirs(coord):
                if current_n + 1 == n2:
                    stack.append(trail + [ncoord])
        return trails

    def all_trailheads(self, find_all=False):
        trails = []
        for coord in self.starts:
            if find_all:
                trails.extend(self.trailheads_at(coord, find_all))
            else:
                trails.extend(self.trailheads_at(coord))
        return trails


m = Map(data)
print(len(m.all_trailheads()))
print(len(m.all_trailheads(find_all=True)))
