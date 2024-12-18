from pathlib import Path
from aoc_utils import Point


data = (Path(__file__).parent.parent / "data/day18.txt").read_text().strip()


class Map:
    def __init__(self, data, start, end):
        self.start = start
        self.end = end
        self.data = self.parse(data)
        self.corrupted = set()

    def parse(self, data):
        return [list(map(int, x.split(','))) for x in data.splitlines()]

    def drop_bytes(self, n):
        self.corrupted = set()
        for x, y in self.data[:n]:
            self.corrupted.add(Point(x, y))

    def init_map(self, n=70):
        m = {}
        for y in range(n+1):
            for x in range(n+1):
                point = Point(x, y)
                if point in self.corrupted:
                    ch = "#"
                else:
                    ch = "."
                m[point] = ch
        return m

    def min_path(self, n=70, bfs=True):
        stack = [(0, self.start)]
        seen = {}
        m = self.init_map(n=n)
        while stack:
            if bfs:
                item = stack.pop(0)
            else:
                item = stack.pop()
            dist, point = item
            ch = m.get(point, '#')
            if point == self.end:
                return dist
            if ch == '#':
                continue
            if seen.get(point, float('inf')) <= dist:
                continue
            seen[point] = dist
            for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                npoint = point + dir
                stack.append((dist + 1, npoint))


m = Map(data, Point(0, 0), Point(70, 70))
m.drop_bytes(1024)
print(m.min_path(70))


i = 1024
while True:
    print(f"trying {i}")
    m.drop_bytes(i)
    found = m.min_path(70, bfs=False)
    if found is None:
        print(i)
    i += 1
