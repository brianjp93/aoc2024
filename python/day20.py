from pathlib import Path
from aoc_utils import StringMap, DIRS_4, Point


data = (Path(__file__).parent.parent / "data/day20.txt").read_text().strip()


class Map(StringMap):
    pos_char = 'S'
    end_char = 'E'

    def find_path(self, start, end, open=None):
        pos = start
        pq = [(0, pos)]
        seen = {}
        while pq:
            items = pq.pop(0)
            score, pos = items
            if pos in seen:
                continue
            seen[pos] = score

            if open and pos in open:
                ch = '.'
            else:
                ch = self.m.get(pos, '#')

            if pos == end:
                return score, seen
            if ch == '#':
                continue
            for dir in DIRS_4:
                pq.append((score + 1, pos + dir))
        return seen[end], seen

    def get_valid(self, pos: Point, man_dist: int):
        for y in range(-man_dist, man_dist + 1):
            x_range = man_dist - abs(y)
            for x in range(-x_range, x_range + 1):
                assert abs(x) + abs(y) <= man_dist
                if x == 0 and y == 0:
                    continue
                npos = pos + Point(x, y)
                if self.m.get(npos, '#') == '.':
                    yield npos

    def count_cheats(self, cheat=2, improvement: int=1):
        track = {pos for pos, ch in self.m.items() if ch == '.'}
        _, og_dmap = self.find_path(self.pos, self.end)
        solutions = 0
        for pos in track:
            start_dist = og_dmap[pos]
            for other in self.get_valid(pos, cheat):
                end_dist = og_dmap[other]
                if start_dist + pos.manhattan(other) <= end_dist - improvement:
                    solutions += 1
        return solutions


m = Map(data)
print(m.count_cheats(2, improvement=100))
print(m.count_cheats(20, improvement=100))
