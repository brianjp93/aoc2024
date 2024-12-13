from pathlib import Path
import heapq
from sympy.matrices import Matrix


data = (Path(__file__).parent.parent / "data/day13.txt").read_text().strip()


class Game:
    def __init__(self, data):
        self.prize, self.a, self.b = self.parse(data)
        self.big_prize = self.prize[0] + 10000000000000, self.prize[1] + 10000000000000

    def __repr__(self):
        return f"Prize={self.prize}, a={self.a}, b={self.b}"

    def parse(self, data):
        a, b, prize = data.splitlines()
        ax, ay = a.split(":")[1].split(",")
        ax = int(ax.split("+")[1])
        ay = int(ay.split("+")[1])
        bx, by = b.split(":")[1].split(",")
        bx = int(bx.split("+")[1])
        by = int(by.split("+")[1])
        prize_x, prize_y = prize.split(":")[1].split(",")
        prize_x = int(prize_x.split("=")[1])
        prize_y = int(prize_y.split("=")[1])
        return ((prize_x, prize_y), (ax, ay), (bx, by))

    def cost(self, a, b):
        return (a * 3) + b

    def solve(self, big=False):
        a = self.a[0], self.b[0]
        b = self.a[1], self.b[1]
        p = self.prize
        if big:
            p = self.big_prize
        den = (a[0] * b[1]) - (a[1] * b[0])
        x = ((b[1] * p[0]) - (a[1] * p[1])) / den
        y = (-(b[0] * p[0]) + (a[0] * p[1])) / den
        if x >= 0 and y >= 0 and int(x) == x and int(y) == y:
            return int(self.cost(x, y)), x, y
        return 0, 0, 0

    def solve_sympy(self, big=False):
        prize = self.prize
        if big:
            prize = self.big_prize
        a = Matrix([[self.a[0], self.b[0]], [self.a[1], self.b[1]]])
        b = Matrix([[prize[0]], [prize[1]]])
        out = a.inv() * b
        x, y = out
        if x >= 0 and y >= 0 and int(x) == x and int(y) == y:
            return int(self.cost(*out)), out[0], out[1]
        return 0, 0, 0

    def find_answer(self, big=False):
        prize = self.prize
        if big:
            prize = self.big_prize
        pq = []
        heapq.heappush(pq, [self.cost(1, 0), 1, 0])
        heapq.heappush(pq, [self.cost(0, 1), 0, 1])
        seen = set()
        while pq:
            cost, a_count, b_count = heapq.heappop(pq)
            key = (a_count, b_count)
            if key in seen:
                continue
            seen.add(key)
            ax = a_count * self.a[0]
            ay = a_count * self.a[1]
            bx = b_count * self.b[0]
            by = b_count * self.b[1]
            x = ax + bx
            y = ay + by
            if (x, y) == prize:
                return (cost, a_count, b_count)
            if x > prize[0] or y > prize[1]:
                continue
            heapq.heappush(pq, [cost + 3, a_count + 1, b_count])
            heapq.heappush(pq, [cost + 1, a_count, b_count + 1])
        return 0, 0, 0


def get_games(data):
    for part in data.split("\n\n"):
        yield Game(part)


games = list(get_games(data))
# part 1 without and with sympy
print(sum([x.solve()[0] for x in games]))
print(sum([x.solve_sympy()[0] for x in games]))

# part 2 without and with sympy
print(sum([x.solve(big=True)[0] for x in games]))
print(sum([x.solve_sympy(big=True)[0] for x in games]))
