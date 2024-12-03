from pathlib import Path
import re

data = (Path(__file__).parent.parent / 'data/day03.txt').read_text()
pat = re.compile(r"mul\((\d+),(\d+)\)")
print(sum(int(a) * int(b) for a, b in pat.findall(data)))
print(sum(sum(int(a) * int(b) for a, b in pat.findall(part.split("don't()")[0])) for part in data.split("do()")))
