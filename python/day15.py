from pathlib import Path
from aoc_utils import Point


data = (Path(__file__).parent.parent / "data/day15.txt").read_text().strip()

class Map:
    def __init__(self, data, moves):
        self.m, self.max_x, self.max_y, self.pos = self.parse(data)
        self.moves = moves

    def parse(self, data):
        m: dict[Point, str] = {}
        max_x = max_y = 0
        pos = Point(0, 0)
        for y, row in enumerate(data.splitlines()):
            max_y = max(max_y, y)
            for x, ch in enumerate(row):
                if ch == '@':
                    pos = Point(x, y)
                    ch = "."
                m[Point(x, y)] = ch
                max_x = max(max_x, x)
        return m, max_x, max_y, pos

    def get_line(self, point: Point, dir: Point):
        point += dir
        ch = self.m.get(point, '#')
        points = [(point, ch)]
        while ch == 'O':
            point += dir
            ch = self.m.get(point, '#')
            points.append((point, ch))
        return points

    def move(self, dir: Point):
        line = self.get_line(self.pos, dir)
        if line[0][1] == '#':
            return
        end_point, end_ch = line[-1]
        if end_ch == ".":
            self.pos += dir
            self.m[self.pos] = "."
            if len(line) > 1:
                self.m[end_point] = "O"

    def gps(self):
        return sum(point.y * 100 + point.x for point, ch in self.m.items() if ch == 'O')

    def do_moves(self):
        for dir_string in self.moves:
            if dir_string == '\n':
                continue
            dir = DIRS[dir_string]
            self.move(dir)

    def draw(self):
        out = []
        for y in range(self.max_y + 1):
            row = []
            for x in range(self.max_x + 1):
                ch = self.m[Point(x, y)]
                if Point(x, y) == self.pos:
                    ch = '@'
                row.append(ch)
            out.append(''.join(row))
        return '\n'.join(out)


class Map2(Map):
    def parse(self, data):
        m: dict[Point, str] = {}
        max_x = max_y = 0
        pos = Point(0, 0)
        for y, row in enumerate(data.splitlines()):
            max_y = max(max_y, y)
            for x, ch in enumerate(row):
                point = Point(x*2, y)
                if ch == '@':
                    ch = "."
                    pos = point
                    m[point] = ch
                    m[point + (1, 0)] = ch
                elif ch == "O":
                    m[point] = "["
                    m[point + (1, 0)] = "]"
                else:
                    m[point] = ch
                    m[point + (1, 0)] = ch
                max_x = max(max_x, x*2 + 1)
        return m, max_x, max_y, pos

    def get_blocking(self, points: list[Point], dir: Point):
        walls = set()
        region = set()
        for point in points:
            npoint = point + dir
            ch = self.m[npoint]
            if ch == '#':
                walls.add(npoint)
            elif ch == ".":
                continue
            elif dir.x:
                if ch in "[]":
                    region.add(npoint)
                    region.add(npoint + dir)
                    nregion, nwalls = self.get_blocking([npoint + dir], dir)
                    region.update(nregion)
                    walls.update(nwalls)
            elif dir.y:
                if ch == "[":
                    pieces = [npoint, npoint + (1, 0)]
                elif ch == "]":
                    pieces = [npoint, npoint + (-1, 0)]
                else:
                    assert False, 'should not get here'
                region.update(pieces)
                nregion, nwalls = self.get_blocking(pieces, dir)
                region.update(nregion)
                walls.update(nwalls)
            else:
                assert False, 'how did this happen'
        return region, walls

    def move(self, dir):
        region, walls = self.get_blocking([self.pos], dir)
        if walls:
            return
        self.pos += dir
        new_map = self.m.copy()
        for p in region:
            new_map[p] = "."
        for p in region:
            new_map[p + dir] = self.m[p]
        self.m = new_map

    def gps(self):
        return sum(100 * point.y + point.x for point, ch in self.m.items() if ch == '[')



DIRS = {
    '>': Point(1, 0),
    'v': Point(0, 1),
    '<': Point(-1, 0),
    '^': Point(0, -1),
}


map_data, moves = data.split("\n\n")

m = Map(map_data, moves)
m.do_moves()
print(m.gps())

m = Map2(map_data, moves)
m.do_moves()
print(m.gps())
