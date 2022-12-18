from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    positions = []
    for line in lines:
        x,y,z = line.split(',')
        x,y,z = int(x), int(y), int(z)
        positions.append((x, y, z))
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
EXPECTED = 64


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
