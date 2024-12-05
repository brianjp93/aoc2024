from pathlib import Path

data = (Path(__file__).parent.parent / 'data/day05.txt').read_text()


p1, p2  = data.split("\n\n")
rules = {}
for line in p1.splitlines():
    a, b = map(int, line.split("|"))
    if a not in rules:
        rules[a] = {"before": set(), "after": set()}
    if b not in rules:
        rules[b] = {"before": set(), "after": set()}
    rules[a]["after"].add(b)
    rules[b]["before"].add(a)

pages = [list(map(int, x.split(","))) for x in p2.splitlines()]

def is_valid_page(page):
    for i, n in enumerate(page):
        if rule := rules.get(n, None):
            before = set(page[:i])
            after = set(page[i+1:])
            if rule["before"] & after or rule["after"] & before:
                return False
    return True

def fix_page(page):
    page = page[:]
    while not is_valid_page(page):
        for i, n in enumerate(page):
            if rule := rules.get(n, None):
                before = set(page[:i])
                after = set(page[i+1:])
                wrong = (rule["before"] & after) | (rule["after"] & before)
                if wrong:
                    n2 = wrong.pop()
                    i2 = page.index(n2)
                    page[i2], page[i] = page[i], page[i2]
    return page

total = 0
for page in pages:
    if is_valid_page(page):
        idx = len(page) // 2
        total += page[idx]
print(total)

total = 0
for page in pages:
    if not is_valid_page(page):
        page = fix_page(page)
        idx = len(page) // 2
        total += page[idx]
print(total)
