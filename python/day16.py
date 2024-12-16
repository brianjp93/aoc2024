from pathlib import Path
from aoc_utils import StringMap
import heapq


data = (Path(__file__).parent.parent / "data/day16.txt").read_text().strip()

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class Map(StringMap):
    pos_char = "S"
    end_char = "E"
    empty_char = "."

    def find_path(self):
        pos = self.pos
        facing = (1, 0)
        pq = []
        heapq.heappush(pq, (0, pos, facing))
        seen = set()
        while pq:
            items = heapq.heappop(pq)
            score, pos, facing = items
            key = (pos, facing)
            if key in seen:
                continue
            seen.add(key)
            ch = self.m.get(pos, '#')
            if pos == self.end:
                return score
            elif ch == '#':
                continue
            heapq.heappush(pq, (score + 1, pos + facing, facing))
            idx = DIRS.index(facing)
            for new_dir in [idx - 1, idx + 1]:
                heapq.heappush(pq, (score + 1000, pos, DIRS[new_dir % len(DIRS)]))

    def find_path2(self):
        pos = self.pos
        facing = (1, 0)
        pq = []
        heapq.heappush(pq, (0, [pos], facing))
        seen = {}
        lowest_score = float('inf')
        best_path_spaces = set()
        while pq:
            items = heapq.heappop(pq)
            score, pos_list, facing = items
            pos = pos_list[-1]
            key = (pos, facing)
            if seen.get(key, float('inf')) < score:
                continue
            seen[key] = score
            ch = self.m.get(pos, '#')
            if ch == '#':
                continue
            if pos == self.end:
                if score <= lowest_score:
                    lowest_score = score
                    best_path_spaces |= set(pos_list)
                    continue
                else:
                    return best_path_spaces
            heapq.heappush(pq, (score + 1, pos_list + [pos + facing], facing))
            idx = DIRS.index(facing)
            for new_dir in [idx - 1, idx + 1]:
                heapq.heappush(pq, (score + 1000, pos_list, DIRS[new_dir % len(DIRS)]))
        return best_path_spaces

m = Map(data)
print(m.find_path())
print(len(m.find_path2()))
