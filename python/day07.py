from pathlib import Path

data = (Path(__file__).parent.parent / "data/day07.txt").read_text()

# data = """190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20"""


def test_line(ans, nums):
    stack = [(nums[0], nums[1:])]
    while stack:
        current, vals = stack.pop()
        # print(current, vals)
        # input()
        if current == ans and not vals:
            return True
        if not vals:
            continue
        # print(f"appending {(current * vals[0], vals[1:])}")
        # print(f"appending {(current + vals[0], vals[1:])}")
        stack.append((current * vals[0], vals[1:]))
        stack.append((current + vals[0], vals[1:]))
    return False


def test_line2(ans, nums):
    stack = [(nums[0], nums[1:])]
    while stack:
        current, vals = stack.pop()
        # print(current, vals)
        # input()
        if current == ans and not vals:
            return True
        if not vals:
            continue
        # print(f"appending {(current * vals[0], vals[1:])}")
        # print(f"appending {(current + vals[0], vals[1:])}")
        stack.append((current * vals[0], vals[1:]))
        stack.append((current + vals[0], vals[1:]))
        stack.append((int(str(current) + str(vals[0])), vals[1:]))
    return False


def parse(data):
    for line in data.splitlines():
        a, b = line.split(":")
        a = int(a)
        vals = list(map(int, b.split()))
        yield a, vals


def p1():
    total = 0
    for ans, nums in parse(data):
        # print(ans, nums)
        if test_line(ans, nums):
            total += ans
            # print(f"adding {ans=}")
    return total

def p2():
    total = 0
    for ans, nums in parse(data):
        # print(ans, nums)
        if test_line2(ans, nums):
            total += ans
            # print(f"adding {ans=}")
    return total

print(p1())
print(p2())
