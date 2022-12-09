from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def distance(v):
    return v.index(False) + 1 if (False in v) else len(v)


def compute(s: str) -> int:
    trees = [[int(v) for v in list(row)] for row in s.strip().split('\n')]

    max_score = 0
    for i, row in enumerate(trees):
        for j, col in enumerate(row):
            tree = trees[i][j]

            top = [tree > row[j] for row in trees[:i]][::-1]
            left = [tree > col for col in trees[i][:j]][::-1]
            bottom = [tree > row[j] for row in trees[i + 1:]]
            right = [tree > col for col in trees[i][j + 1:]]

            to_top, to_bottom = distance(top), distance(bottom)
            to_left, to_right = distance(left), distance(right)

            score = to_top * to_left * to_right * to_bottom
            if score > max_score:
                max_score = score

    return max_score


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
