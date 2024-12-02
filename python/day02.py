from pathlib import Path

data = (Path(__file__).parent.parent / 'data/day02.txt').read_text()

def is_safe(level):
    for a, b in zip(level, level[1:]):
        if (b > a) != (level[1] > level[0]) or not (1 <= abs(a-b) < 4) or a == b:
            return 0
    return 1

def p1():
    return sum(is_safe(tuple(map(int, row.split()))) for row in data.splitlines())

def p2():
    safe_count = 0
    for row in data.splitlines():
        row = list(map(int, row.split()))
        if is_safe(row):
            safe_count += 1
        else:
            for i in range(len(row)):
                if is_safe(row[:i] + row[i+1:]):
                    safe_count += 1
                    break
    return safe_count


print(p1())
print(p2())
