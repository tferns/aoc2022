from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    crates, instructions = s.split('\n\n')

    crates_lines = crates.splitlines()
    crates_indexes = [int(c) for c in crates_lines.pop().split()]

    crates = [[] for _ in crates_indexes]

    for line in crates_lines:
        for index in crates_indexes:
            letter = line[(index - 1) * 4 + 1]
            if letter.strip():
                crates[index - 1] += letter

    crates = [crate[::-1] for crate in crates]

    for instruction in instructions.splitlines():
        _, amount, _, cfrom, _, cto = instruction.split()
        cto_idx, cfrom_idx = int(cto) - 1, int(cfrom) - 1
        amount = int(amount)

        if amount > 1:
            crates[cto_idx] += crates[cfrom_idx][-amount:]
            crates[cfrom_idx] = crates[cfrom_idx][:-amount]
        else:
            for _ in range(amount):
                crates[cto_idx] += crates[cfrom_idx].pop()

    return ''.join([c[-1] for c in crates])


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'MCD'


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
