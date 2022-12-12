from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def index(letter):
    return ALPHABET.index(letter)


def bfs(grid, start, end):
    visited = set()
    q = deque([(start, 0)])

    while q:
        position, distance = q.popleft()

        if position == end:
            return distance

        if position in visited:
            continue

        visited.add(position)
        x, y = position

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            # for dx, dy in tuple(support.adjacent_4(x, y)):
            # for dx, dy in support.adjacent_4(x, y):
            if (0 <= y + dy < len(grid) and 0 <= x + dx < len(grid[0])):
                if index(grid[y + dy][x + dx]) - index(grid[y][x]) <= 1:
                    q.append(((x + dx, y + dy), distance + 1))

    raise ValueError('No path found')


def compute(s: str) -> int:
    grid = [list(y) for y in s.splitlines()]

    start = end = None
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'S':
                start = (x, y)
                grid[y][x] = 'a'
            elif grid[y][x] == 'E':
                end = (x, y)
                grid[y][x] = 'z'

    if not start or not end:
        raise ValueError('No start or end found')

    return bfs(grid, start, end)


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
