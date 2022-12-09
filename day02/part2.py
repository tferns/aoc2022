from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

SCORE_MAP = {'X': 1, 'Y': 2, 'Z': 3}

WIN_MAP = {'X': 'C', 'Y': 'A', 'Z': 'B'}
DRAW_MAP = {'X': 'A', 'Y': 'B', 'Z': 'C'}
LOSE_MAP = {'X': 'B', 'Y': 'C', 'Z': 'A'}


def FLIP(_dict): return {v: k for k, v in _dict.items()}


PART_2_MAP = {
    'X': (FLIP(LOSE_MAP), 0),
    'Y': (FLIP(DRAW_MAP), 3),
    'Z': (FLIP(WIN_MAP), 6),
}


def compute(s: str) -> int:
    lines = s.splitlines()

    score = 0
    for line in lines:
        theirs, secret = line.split()
        result_map, result_score = PART_2_MAP[secret]
        our_answer = result_map[theirs]

        score += SCORE_MAP[our_answer]
        score += result_score

    return score


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
