from pathlib import Path

data = (Path(__file__).parent.parent / "data/day07.txt").read_text()


def test_line(ans, nums, concat=False):
    stack = [(nums[0], nums[1:])]
    while stack:
        current, vals = stack.pop()
        if current == ans and not vals:
            return True
        if not vals:
            continue
        stack.append((current * vals[0], vals[1:]))
        stack.append((current + vals[0], vals[1:]))
        if concat:
            stack.append((int(str(current) + str(vals[0])), vals[1:]))
    return False


def parse(data):
    for line in data.splitlines():
        a, b = line.split(":")
        a = int(a)
        vals = list(map(int, b.split()))
        yield a, vals


def p1():
    return sum(ans for ans, nums in parse(data) if test_line(ans, nums))


def p2():
    return sum(ans for ans, nums in parse(data) if test_line(ans, nums, concat=True))


print(p1())
print(p2())
