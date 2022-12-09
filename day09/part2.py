from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass
from dataclasses import field

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Rope:
    parts: list[RopePart] = field(default_factory=list)

    @property
    def head(self):
        return self.parts[0]

    @property
    def tail(self):
        return self.parts[-1]


@dataclass
class RopePart:
    x: int
    y: int

    def dist_x(self, other):
        return abs(self.x - other.x)

    def dist_y(self, other):
        return abs(self.y - other.y)

    def move_direction(self, direction: str):
        if direction == 'L':
            self.x -= 1
        elif direction == 'R':
            self.x += 1
        elif direction == 'U':
            self.y += 1
        elif direction == 'D':
            self.y -= 1

    def as_tuple(self):
        return self.x, self.y


def compute(s: str) -> int:
    parts = [RopePart(0, 0) for _ in range(10)]
    rope = Rope(parts)
    tail_visits = {(0, 0)}

    lines = s.splitlines()
    for line in lines:
        direction, amount = line.split()
        amount = int(amount)

        for _ in range(amount):
            rope.head.move_direction(direction)

            for i in range(1, len(rope.parts)):
                prior = rope.parts[i - 1]
                current = rope.parts[i]

                while current.dist_x(prior) > 1 or current.dist_y(prior) > 1:

                    if current.dist_x(prior) > 0:
                        if prior.x > current.x:
                            current.x += 1
                        else:
                            current.x -= 1

                    if current.dist_y(prior) > 0:
                        if prior.y > current.y:
                            current.y += 1
                        else:
                            current.y -= 1

            tail_visits.add(rope.tail.as_tuple())

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
