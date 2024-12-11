from collections import defaultdict
from pathlib import Path

data = (Path(__file__).parent.parent / "data/day11.txt").read_text().strip()


class Stones:
    def __init__(self, data):
        self.stones = self.parse(data)
        self._stones = self.stones.copy()

    def parse(self, data: str):
        stones = defaultdict(int)
        for x in data.split():
            stones[int(x)] += 1
        return stones

    def blink_n(self, n_times):
        self.stones = self._stones
        for _ in range(n_times):
            self.blink()

    def blink(self):
        nstones = defaultdict(int)
        for n, count in self.stones.items():
            digits = str(n)
            if n == 0:
                nstones[1] += count
            elif len(digits) % 2 == 0:
                idx = len(digits) // 2
                nstones[int(digits[:idx])] += count
                nstones[int(digits[idx:])] += count
            else:
                nstones[n * 2024] += count
        self.stones = nstones

s = Stones(data)
s.blink_n(25)
print(sum(s.stones.values()))
s.blink_n(75)
print(sum(s.stones.values()))
