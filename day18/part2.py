from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    positions = []
    for line in s.splitlines():
        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)
        positions.append((x, y, z))

    min_x = min([x for x, *_ in positions])
    max_x = max([x for x, *_ in positions])
    min_y = min([y for _, y, _ in positions])
    max_y = max([y for _, y, _ in positions])
    min_z = min([z for *_, z in positions])
    max_z = max([z for *_, z in positions])

    spaces = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                if (x, y, z) not in positions:
                    spaces.append((x, y, z))

    space_is_outside_map = {}
    for x, y, z in spaces:
        if any([
            x == max_x, x == min_x,
            y == max_y, y == min_y,
            z == max_z, z == min_z
        ]):
            space_is_outside_map[(x, y, z)] = True
        else:
            space_is_outside_map[(x, y, z)] = False

    for dist in range(1, (max(max_x, max_y, max_z) // 2) + 1):
        for x, y, z in spaces:
            space_is_outside = space_is_outside_map[(x, y, z)]
            if space_is_outside:
                continue

            if any([
                x == max_x - dist, x == min_x + dist,
                y == max_y - dist, y == min_y + dist,
                z == max_z - dist, z == min_z + dist
            ]):
                if (x + 1, y, z) in spaces:
                    adj_space_is_outside = space_is_outside_map[(x + 1, y, z)]
                    if adj_space_is_outside:
                        space_is_outside_map[(x, y, z)] = True
                if (x - 1, y, z) in spaces:
                    adj_space_is_outside = space_is_outside_map[(x - 1, y, z)]
                    if adj_space_is_outside:
                        space_is_outside_map[(x, y, z)] = True
                if (x, y + 1, z) in spaces:
                    adj_space_is_outside = space_is_outside_map[(x, y + 1, z)]
                    if adj_space_is_outside:
                        space_is_outside_map[(x, y, z)] = True
                if (x, y - 1, z) in spaces:
                    adj_space_is_outside = space_is_outside_map[(x, y - 1, z)]
                    if adj_space_is_outside:
                        space_is_outside_map[(x, y, z)] = True
                if (x, y, z + 1) in spaces:
                    adj_space_is_outside = space_is_outside_map[(x, y, z + 1)]
                    if adj_space_is_outside:
                        space_is_outside_map[(x, y, z)] = True
                if (x, y, z - 1) in spaces:
                    adj_space_is_outside = space_is_outside_map[(x, y, z - 1)]
                    if adj_space_is_outside:
                        space_is_outside_map[(x, y, z)] = True

    positions.extend(s for s in spaces if not space_is_outside_map[s])

    surface = 0
    for x, y, z in positions:
        sides = 6
        if (x + 1, y, z) in positions:
            sides -= 1
        if (x - 1, y, z) in positions:
            sides -= 1
        if (x, y + 1, z) in positions:
            sides -= 1
        if (x, y - 1, z) in positions:
            sides -= 1
        if (x, y, z + 1) in positions:
            sides -= 1
        if (x, y, z - 1) in positions:
            sides -= 1
        surface += sides

    return surface


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 58


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
