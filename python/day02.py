from pathlib import Path

data = (Path(__file__).parent.parent / 'data/day02.txt').read_text()
parsed = list(map(lambda row: tuple(map(int, row.split())), data.splitlines()))

def is_safe(level):
    return 0 if any((b > a) != (level[1] > level[0]) or not (0 < abs(a-b) < 4) for a, b in zip(level, level[1:])) else 1

print(sum(is_safe(row) for row in parsed))
print(sum(any(is_safe(row[:i] + row[i+1:]) for i in range(len(row))) for row in parsed))
