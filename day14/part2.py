from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()

    allpaths = []
    for line in lines:
        path = []
        coords = line.split(" -> ")
        for coord in coords:
            x, y = coord.split(",")
            x = int(x)
            y = int(y)
            path.append((x, y))
        allpaths.append(path)

    # for line in lines, draw each line
    fullpaths = set()
    for path in allpaths:
        for i in range(1, len(path)):
            x1, y1 = path[i - 1]
            x2, y2 = path[i]
            if x1 == x2:
                if y1 < y2:
                    for y in range(y1, y2 + 1):
                        fullpaths.add((x1, y))
                elif y1 > y2:
                    for y in range(y2, y1 + 1):
                        fullpaths.add((x1, y))
            elif y1 == y2:
                if x1 < x2:
                    for x in range(x1, x2 + 1):
                        fullpaths.add((x, y1))
                elif x1 > x2:
                    for x in range(x2, x1 + 1):
                        fullpaths.add((x, y1))
            fullpaths.add((x2, y2))



    max_y = max([y for x, y in fullpaths])
    max_x = max([x for x, y in fullpaths])
    min_x = min([x for x, y in fullpaths])

    max_y += 2
    extra_x = (max_y * 2) // 2
    max_x += extra_x
    min_x -= extra_x

    for x in range(min_x, max_x):
        fullpaths.add((x, max_y))

    max_y = max([y for x, y in fullpaths])
    max_x = max([x for x, y in fullpaths])
    min_x = min([x for x, y in fullpaths])

    grid = []
    for y in range(0, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in fullpaths:
                row.append('◼')
            else:
                row.append('◺')
        grid.append(row)

    sand_resting = 0
    ss_x, ss_y = 500, 0
    sand_x, sand_y = ss_x - min_x, ss_y
    while True:

        if sand_x == ss_x - min_x and sand_y == ss_y:
            found = True
            for x, y in [(sand_x, sand_y), (sand_x, sand_y+1),
                         (sand_x-1, sand_y+1), (sand_x+1, sand_y+1)]:
                if grid[y][x] != '◻':
                    found = False

            if found:
                return sand_resting

        sand_fell = False
        for x, y in [(sand_x, sand_y+1), (sand_x-1, sand_y+1), (sand_x+1, sand_y+1)]:
            if grid[y][x] == '◺':
                sand_x, sand_y = x, y
                sand_fell = True
                break

        if not sand_fell:
            sand_resting += 1
            grid[sand_y][sand_x] = '◻'
            sand_x, sand_y = ss_x - min_x, ss_y

    raise Exception("No solution found")


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


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
