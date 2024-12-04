from pathlib import Path
import itertools

data = (Path(__file__).parent.parent / 'data/day04.txt').read_text()


def get_map(data: str):
    m = {}
    for y, row in enumerate(data.splitlines()):
        for x, ch in enumerate(row):
            m[(x, y)] = ch
    return m


def dirs():
    for a, b in itertools.product((-1, 0, 1), repeat=2):
        if a == 0 and b == 0:
            continue
        yield a, b


def count_xmas_at(m: dict, coord: tuple[int, int]):
    x, y = coord
    goal = 'XMAS'
    found = m[coord]
    count = 0
    if found != 'X':
        return 0
    ncoord = (x, y)
    for a, b in dirs():
        while goal.startswith(found):
            if goal == found:
                count += 1
            ncoord = (ncoord[0] + a, ncoord[1] + b)
            found = found + m.get(ncoord, ' ')
        ncoord = (x, y)
        found = m[coord]
    return count

def is_mas_x(m: dict, coord: tuple[int, int]):
    x, y = coord
    if m[coord] != "A":
        return False
    coord = (x, y)
    found = 0
    for diag in (((1, 1), (-1, -1)), ((-1, 1), (1, -1))):
        find = set("MS")
        for a, b in diag:
            ncoord = coord[0] + a, coord[1] + b
            ch = m.get(ncoord, ' ')
            if ch in find:
                find.remove(ch)
                found += 1
    # there should be 4 found letters (M, M, S, S)
    return found == 4


def find_mas_x(data: str):
    m = get_map(data)
    max_x = max(x[0] for x in m.keys())
    max_y = max(x[1] for x in m.keys())

    count = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if is_mas_x(m, (x, y)):
                count += 1
    return count


def find_xmas(data: str):
    m = get_map(data)
    max_x = max(x[0] for x in m.keys())
    max_y = max(x[1] for x in m.keys())

    count = 0
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            count += count_xmas_at(m, (x, y))
    return count



print(find_xmas(data))
print(find_mas_x(data))
