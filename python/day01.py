from pathlib import Path
from collections import Counter

data = (Path(__file__).parent.parent / 'data/day01.txt').read_text()

l1 = []
l2 = []
for line in data.splitlines():
    a, b = map(int, line.split())
    l1.append(a)
    l2.append(b)
l1.sort()
l2.sort()
l2_counter = Counter(l2)

print(sum(abs(a - b) for a, b in zip(l1, l2)))
print(sum(a * l2_counter.get(a, 0) for a in l1))
