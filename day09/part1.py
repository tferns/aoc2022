from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_tail_touching(head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail
    return abs(head_x - tail_x) <= 1 and abs(head_y - tail_y) <= 1


def sum_tuples(a, b):
    return tuple(x + y for x, y in zip(a, b))


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
                head = sum_tuples(head, (-1, 0))
            elif direction == 'R':
                head = sum_tuples(head, (1, 0))
            elif direction == 'U':
                head = sum_tuples(head, (0, 1))
            elif direction == 'D':
                head = sum_tuples(head, (0, -1))

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
