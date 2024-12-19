from functools import cache
from pathlib import Path


data = (Path(__file__).parent.parent / "data/day19.txt").read_text().strip()


def parse(data):
    a, b = data.split("\n\n")
    towel_patterns = [x.strip() for x in a.split(",")]
    designs = b.splitlines()
    return set(towel_patterns), designs


PATTERNS, DESIGNS = parse(data)

def is_valid(design: str):
    stack = [""]
    seen = set()
    while stack:
        s = stack.pop()
        if design == s:
            return True
        if not design.startswith(s):
            continue
        if s in seen:
            continue
        seen.add(s)
        for nstring in PATTERNS:
            stack.append(s + nstring)
    return False

@cache
def count_valid(design: str):
    count = 0
    for pat in PATTERNS:
        if design == pat:
            count += 1
        elif design.startswith(pat):
            count += count_valid(design[len(pat):])
    return count

print(sum(is_valid(design) for design in DESIGNS))
print(sum(count_valid(design) for design in DESIGNS))
