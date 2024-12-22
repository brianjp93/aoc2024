from pathlib import Path
from aoc_utils import StringMap, DIRS_4, Point
import heapq
import sys

sys.setrecursionlimit(10000000)


data = (Path(__file__).parent.parent / "data/day20.txt").read_text().strip()


class Map(StringMap):
    pos_char = 'S'
    end_char = 'E'

    def find_path(self, start, end):
        pos = start
        pq = []
        heapq.heappush(pq, (0, pos))
        seen = {}
        while pq:
            items = heapq.heappop(pq)
            score, pos = items
            if pos in seen:
                continue
            seen[pos] = score
            ch = self.m.get(pos, '#')
            # if pos == self.end:
            #     return score, seen
            if ch == '#':
                continue
            for dir in DIRS_4:
                heapq.heappush(pq, (score + 1, pos + dir))
        return seen[end], seen

    def build_dist_map(self, save_time=100):
        old_min_dist, old_dmap = self.find_path(self.end, self.pos)
        _, dmap_from_start = self.find_path(self.pos, self.end)
        max_dist = old_min_dist - save_time
        # print(f"{max_dist=}")
        stack: list[tuple[int, Point, None | Point, int, set[Point]]] = [(self.pos.manhattan(self.end), self.pos, None, 0, set())]
        # distance map
        dmap = {}
        while stack:
            # print(f"{len(stack)=}")
            item = heapq.heappop(stack)
            best_possible, pos, cheat_pos, dist, cpath = item
            key = (pos, cheat_pos)

            if pos in cpath:
                continue

            if cheat_pos and key in dmap:
                continue

            if best_possible > max_dist:
                # print("too big")
                continue

            ch = self.m.get(pos, '#')
            if pos == self.end:
                if key not in dmap:
                    dmap[key] = {}
                dmap[key][dist] = dmap[key].get(dist, 0) + 1
                print(f"found a solution with distance {dist} which saves {old_min_dist - dist}")
                continue
            if ch == '#':
                if cheat_pos:
                    # print('already cheated')
                    continue
                cheat_pos = pos

            if dmap.get(key, None) is None:
                dmap[key] = {dist: 1}
            else:
                if cheat_pos and dist > dmap_from_start.get(pos, 0):
                    # print("impossible")
                    continue
                dmap[key][dist] = dmap[key].get(dist, 0) + 1
            for dir in DIRS_4:
                npath = cpath | {pos}
                npos = pos + dir
                ndist = dist + 1
                if cheat_pos:
                    best_possible = ndist + old_dmap.get(npos, float('inf'))
                else:
                    point_diff = npos.manhattan(self.end)
                    best_possible = point_diff + ndist
                heapq.heappush(stack, (best_possible, npos, cheat_pos, ndist, npath))
        return dmap

    def count_paths(self, pos: Point, dist: int, cheat_pos: Point | None, max_score, cache, cpath: list):
        key = (pos, bool(cheat_pos))
        if key in cache:
            if dist <= cache[key]:
                print(f"found item in cache {key}")
                return 1

        if pos in [x[0] for x in cpath]:
            return 0
        if dist > max_score:
            return 0
        if pos == self.end:
            print('Found a possible solution with dist=', dist)
            for pos, dist, cheat_pos in cpath:
                key = (pos, bool(cheat_pos))
                cache[key] = max(cache.get(key, 0), dist)
            return 1

        ch = self.m.get(pos, '#')

        ncheat_pos = cheat_pos
        if ch == '#':
            if cheat_pos:
                return 0
            else:
                ncheat_pos = pos

        npath = cpath + [(pos, dist, cheat_pos)]
        count = sum(self.count_paths(pos + dir, dist + 1, ncheat_pos, max_score, cache, npath) for dir in DIRS_4)
        return count


# m = Map(data)
# score, dmap = m.find_path(m.pos, m.end)
# max_score = score - 100
# print(m.count_paths(m.pos, 0, None, max_score, {}, []))




data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
m = Map(data)
score, dmap = m.find_path(m.pos, m.end)
max_score = score - 1
print(m.build_dist_map(save_time=1)[(m.end, )])
# print(m.count_paths(m.pos, 0, None, max_score, {}, []))
