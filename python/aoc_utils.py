from dataclasses import dataclass
from typing import Self
from functools import total_ordering


DIRS_4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]

@dataclass(frozen=True)
@total_ordering
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __lt__(self, other):
        if other is None:
            return False
        return (self.x, self.y) < (other.x, other.y)

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

    def manhattan(self, other: Self | tuple[int, int]):
        if isinstance(other, tuple):
            other = self.__class__(*other)
        diff = self - other
        return abs(diff.x) + abs(diff.y)


class StringMap:
    pos_char = False
    end_char = False
    empty_char = "."

    def __init__(self, data):
        self.m, self.max_x, self.max_y = self.parse(data)

    def parse(self, data):
        m: dict[Point, str] = {}
        max_x = max_y = 0
        for y, row in enumerate(data.splitlines()):
            max_y = max(max_y, y)
            for x, ch in enumerate(row):
                point = Point(x, y)
                if ch == self.pos_char:
                    self.pos = point
                    ch = self.empty_char
                elif ch == self.end_char:
                    self.end = point
                    ch = self.empty_char
                m[point] = ch
                max_x = max(max_x, x)
        return m, max_x, max_y

class IntMap:
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
