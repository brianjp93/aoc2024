from pathlib import Path
from itertools import batched

data = (Path(__file__).parent.parent / "data/day09.txt").read_text().strip()


def decompress(data: list[int]):
    ret = []
    empty = []
    current_index = 0
    for idx, val in enumerate(batched(data, 2, strict=False)):
        if len(val) == 2:
            blocks, free = val
        else:
            blocks = val[0]
            free = 0
        ret.extend([idx] * blocks)
        current_index += blocks
        ret.extend([-1] * free)
        for i in range(free):
            empty.append(i + current_index)
        current_index += free
    return ret, empty


def decompress2(data: list[int]):
    ret = []
    empty = []
    current_index = 0
    for idx, val in enumerate(batched(data, 2, strict=False)):
        if len(val) == 2:
            blocks, free = val
        else:
            blocks = val[0]
            free = 0
        ret.extend([idx] * blocks)
        current_index += blocks
        ret.extend([-1] * free)
        if free:
            empty.append((current_index, free))
        current_index += free
    return ret, empty


def defrag(data: list[int], empty: list[int]):
    data_idx = len(data)
    data = data[:]
    empty = empty[::-1]
    while empty:
        idx = empty.pop()
        while True:
            data_idx -= 1
            if data[data_idx] != -1:
                break
        if idx > data_idx:
            break
        data[idx] = data[data_idx]
        data[data_idx] = -1
    return [x for x in data if x != -1]


def defrag2(data: list[int], empty: list[tuple[int, int]]):
    data = data[:]
    empty = empty[:]
    start = end = len(data)
    while end > 0:
        end -= 1
        if data[end] != -1:
            start = end
            while True:
                if data[start - 1] == data[end]:
                    start -= 1
                else:
                    break
            length = end - start + 1
            for idx, (empty_idx, empty_length) in enumerate(empty):
                if empty_idx > end:
                    break
                if empty_length >= length:
                    for i in range(length):
                        data[i + empty_idx] = data[end]
                    for i in range(start, end+1):
                        data[i] = -1
                    if empty_length > length:
                        empty[idx] = (empty_idx + length, empty_length - length)
                    else:
                        del empty[idx]
                    break
            end = start
    return data


def checksum(data: list[int]):
    return sum(i * x for i, x in enumerate(data) if x != -1)


def parse(data: str):
    return list(map(int, data))


nums = parse(data)

decompressed, empty_list = decompress(nums)
out = defrag(decompressed, empty_list)
print(checksum(out))

decompressed, empty_list = decompress2(nums)
out = defrag2(decompressed, empty_list)
print(checksum(out))
