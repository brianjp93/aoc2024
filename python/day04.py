from pathlib import Path
import itertools
from dataclasses import dataclass

data = (Path(__file__).parent.parent / 'data/day04.txt').read_text()


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def copy(self):
        return self.__class__(self.x, self.y)


def dirs():
    yield from (Point(*coord) for coord in itertools.product((-1, 0, 1), repeat=2) if coord != (0, 0))


class Map:
    def __init__(self, data):
        self.m, self.max_x, self.max_y = self.parse(data)

    def parse(self, data):
        m = {}
        max_x = max_y = 0
        for y, row in enumerate(data.splitlines()):
            max_y = max(max_y, y)
            for x, ch in enumerate(row):
                m[Point(x, y)] = ch
                max_x = max(max_x, x)
        return m, max_x, max_y

    def count_xmas_at(self, coord: Point):
        goal = 'XMAS'
        count = 0
        if self.m[coord] != 'X':
            return 0
        for point in dirs():
            ncoord = coord.copy()
            found = self.m[coord]
            while goal.startswith(found):
                if goal == found:
                    count += 1
                ncoord = ncoord + point
                found = found + self.m.get(ncoord, ' ')
        return count

    def is_mas_x(self, coord: Point):
        if self.m[coord] != "A":
            return False
        found = 0
        for diag in ((Point(1, 1), Point(-1, -1)), (Point(-1, 1), Point(1, -1))):
            find = set("MS")
            for point in diag:
                ncoord = coord + point
                ch = self.m.get(ncoord, ' ')
                if ch in find:
                    find.remove(ch)
                    found += 1
        # there should be 4 found letters (M, M, S, S)
        return found == 4

    def find_mas_x(self):
        return sum(self.is_mas_x(Point(x, y)) for y, x in itertools.product(range(self.max_y + 1), range(self.max_x + 1)))

    def find_xmas(self):
        return sum(self.count_xmas_at(Point(x, y)) for y, x in itertools.product(range(self.max_y + 1), range(self.max_x + 1)))


m = Map(data)
print(m.find_xmas())
print(m.find_mas_x())
