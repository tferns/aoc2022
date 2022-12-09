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
    head = [(0, 0) for _ in range(10)]
    # tail = [(0, 0) for _ in range(10)]
    tail_visits = {(0, 0)}

    lines = s.splitlines()
    for line in lines:
        direction, amount = line.split()
        amount = int(amount)

        for _ in range(amount):
            old_head = head[0]
            if direction == 'L':
                head[0] = sum_tuples(old_head, (-1, 0))
            elif direction == 'R':
                head[0] = sum_tuples(old_head, (1, 0))
            elif direction == 'U':
                head[0] = sum_tuples(old_head, (0, 1))
            elif direction == 'D':
                head[0] = sum_tuples(old_head, (0, -1))

            # if not is_tail_touching(head, tail):
            #     tail_visits.add(tail)
            #     tail = old_head

            # for idx in range(0, len(head)):
            for i in range(1, len(head)):
                previous = prior_x, prior_y = head[i - 1]
                current = curr_x, curr_y = head[i]

                distance_x = abs(curr_x - prior_x)
                distance_y = abs(curr_y - prior_y)

                while distance_x > 1 or distance_y > 1:

                    if distance_x:
                        if prior_x > curr_x:
                            curr_x += 1
                        else:
                            curr_x -= 1

                    if distance_y:
                        if prior_y > curr_y:
                            curr_y += 1
                        else:
                            curr_y -= 1

                    # need to recalc these for the while loop
                    distance_x = abs(curr_x - prior_x)
                    distance_y = abs(curr_y - prior_y)

                # head[i] = current
                head[i] = curr_x, curr_y

            tail_visits.add(head[-1])

    return len(tail_visits)


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
