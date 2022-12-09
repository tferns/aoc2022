from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_tail_touching(head, tail):
    return abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1


def compute(s: str) -> int:

    head = 0, 0
    tail = 0, 0
    tail_visits = {tail}

    lines = s.splitlines()
    for line in lines:
        direction, amount = line.split()
        amount = int(amount)

        for _ in range(amount):
            old_head = head
            if direction == 'L':
                head = head[0] - 1, head[1]
            elif direction == 'R':
                head = head[0] + 1, head[1]
            elif direction == 'U':
                head = head[0], head[1] + 1
            elif direction == 'D':
                head = head[0], head[1] - 1

            if not is_tail_touching(head, tail):
                tail_visits.add(tail)
                tail = old_head

    # last tail isn't accounted for in the loop
    tail_visits.add(tail)

    return len(tail_visits)


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
