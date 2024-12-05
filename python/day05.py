from pathlib import Path
from functools import cmp_to_key

data = (Path(__file__).parent.parent / "data/day05.txt").read_text()


p1, p2 = data.split("\n\n")
rules = {}
for line in p1.splitlines():
    a, b = map(int, line.split("|"))
    if b not in rules:
        rules[b] = set()
    rules[b].add(a)

pages = [list(map(int, x.split(","))) for x in p2.splitlines()]


def is_valid_page(page):
    for i, n in enumerate(page):
        if rule := rules.get(n, None):
            if rule & set(page[i + 1 :]):
                return False
    return True


p1 = p2 = 0
for page in pages:
    if is_valid_page(page):
        idx = len(page) // 2
        p1 += page[idx]
    else:
        page = sorted(page, key=cmp_to_key(lambda x, y: -1 if y in rules[x] else 1))
        idx = len(page) // 2
        p2 += page[idx]

print(p1)
print(p2)
