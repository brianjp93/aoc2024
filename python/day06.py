from pathlib import Path

data = (Path(__file__).parent.parent / "data/day06.txt").read_text()

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

DIRS = [UP, RIGHT, DOWN, LEFT]


class Map:
    def __init__(self, data):
        self.m, self.guard, self.max_x, self.max_y = self.parse(data)
        self.facing = UP
        self.start = self.guard

    def parse(self, data):
        m = {}
        max_x = 0
        max_y = 0
        guard = (0, 0)
        for y, row in enumerate(data.splitlines()):
            max_y = max(y, max_y)
            for x, ch in enumerate(row):
                max_x = max(x, max_x)
                if ch == "^":
                    guard = (x, y)
                    m[(x, y)] = "."
                else:
                    m[(x, y)] = ch
        return m, guard, max_x, max_y

    def turn(self, facing):
        idx = (DIRS.index(facing) + 1) % len(DIRS)
        return DIRS[idx]

    def move(self, pos, facing):
        return (pos[0] + facing[0], pos[1] + facing[1])

    def move_guard(self) -> set[tuple[int, int]]:
        visited = set()
        while True:
            visited.add(self.guard)
            npos = self.move(self.guard, self.facing)
            ch = self.m.get(npos, None)
            match ch:
                case None:
                    return visited
                case ".":
                    self.guard = npos
                case "#":
                    self.facing = self.turn(self.facing)

    def is_loop(self, obs):
        visited = set()
        guard = self.guard
        facing = self.facing
        while True:
            key = (guard, facing)
            if key in visited:
                return True
            visited.add(key)
            npos = self.move(guard, facing)
            ch = self.m.get(npos, None)
            if npos == obs:
                ch = "#"
            match ch:
                case None:
                    return False
                case ".":
                    guard = npos
                case "#":
                    facing = self.turn(facing)

    def bogo_loops(self, positions):
        obstacles = []
        for obs in positions:
            if obs == self.start:
                continue
            if self.is_loop(obs):
                obstacles.append(obs)
        return obstacles


m = Map(data)
positions = m.move_guard()
print(len(positions))
m = Map(data)
print(len(m.bogo_loops(positions)))
