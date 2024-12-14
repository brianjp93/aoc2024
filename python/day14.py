from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass
from aoc_utils import Point
import re
from math import prod


data = (Path(__file__).parent.parent / "data/day14.txt").read_text().strip()
HEIGHT = 103
WIDTH = 101


@dataclass
class Robot:
    p: Point
    v: Point

    @classmethod
    def parse(cls, line):
        x, y, vx, vy = map(int, re.findall(r"\-?\d+", line))
        return cls(p=Point(x, y), v=Point(vx, vy))

    def next_frame(self):
        ncoord = self.p + self.v
        x = ncoord.x % WIDTH
        y = ncoord.y % HEIGHT
        if x != ncoord.x or y != ncoord.y:
            ncoord = Point(x, y)
        self.p = ncoord

    def do_frames(self, n):
        for _ in range(n):
            self.next_frame()


def get_robots(data):
    for line in data.splitlines():
        yield Robot.parse(line)


def draw_robots(robots):
    locations = defaultdict(int)
    for robot in robots:
        locations[robot.p] += 1
    out = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            row.append(str(locations.get(Point(x, y), ".")))
        out.append("".join(row))
    return "\n".join(out)


def draw_all_frames(robots, n):
    for i in range(n):
        print(draw_robots(robots))
        print(f"{i=}")
        for robot in robots:
            robot.next_frame()


def count_quadrants(robots: list[Robot]):
    x = WIDTH // 2
    y = HEIGHT // 2
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        match [robot.p.x < x, robot.p.x > x, robot.p.y < y, robot.p.y > y]:
            case [True, False, True, False]:
                quadrants[0] += 1
            case [False, True, True, False]:
                quadrants[1] += 1
            case [True, False, False, True]:
                quadrants[2] += 1
            case [False, True, False, True]:
                quadrants[3] += 1
            case _:
                pass
    return quadrants


def find_tree(robots):
    for i in range(10000):
        quads = count_quadrants(robots)
        for n in quads:
            if n / sum(quads) > 0.5:
                print(draw_robots(robots))
                print(f"frame={i}")
                return
        for robot in robots:
            robot.next_frame()


robots = list(get_robots(data))

for robot in robots:
    robot.do_frames(100)

quadrants = count_quadrants(robots)
print(prod(quadrants))
robots = list(get_robots(data))
find_tree(robots)
