from pathlib import Path
from functools import cmp_to_key
from collections import defaultdict

data = (Path(__file__).parent.parent / "data/day05.txt").read_text()


def is_valid_page(page):
    return not any(rules[n] & set(page[i+1:]) for i, n in enumerate(page))

p1, p2 = data.split("\n\n")
rules = defaultdict(set)
for line in p1.splitlines():
    a, b = map(int, line.split("|"))
    rules[b].add(a)

pages = [list(map(int, x.split(","))) for x in p2.splitlines()]

p1 = p2 = 0
for page in pages:
    if is_valid_page(page):
        idx = len(page) // 2
        p1 += page[idx]
    else:
        page.sort(key=cmp_to_key(lambda x, y: -1 if y in rules[x] else 1))
        idx = len(page) // 2
        p2 += page[idx]

print(p1)
print(p2)
