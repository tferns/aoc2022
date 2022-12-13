from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def check_sorted(curr_val, next_val):
    if type(curr_val) == list and type(next_val) == int:
        next_val = [next_val]
    elif type(curr_val) == int and type(next_val) == list:
        curr_val = [curr_val]
    if type(curr_val) == int and type(next_val) == int:
        if curr_val == next_val:
            return None  # None if equal
        return curr_val < next_val
    elif type(curr_val) == list and type(next_val) == list:
        for ci in range(max([len(curr_val), len(next_val)])):
            if ci > len(curr_val) - 1:
                return True
            if ci > len(next_val) - 1:
                return False
            cci = curr_val[ci]
            nci = next_val[ci]
            in_right_order = check_sorted(cci, nci)
            if in_right_order is not None:
                return in_right_order
    return None  # None if equal


def compute(s: str) -> int:
    packet_pairs = s.split('\n\n')

    in_right_order_indexs = []
    for i, packet_pair in enumerate(packet_pairs, start=1):
        p1, p2 = (eval(p) for p in packet_pair.split('\n'))
        in_right_order = check_sorted(p1, p2)
        if in_right_order:
            in_right_order_indexs.append(i)

    return sum(in_right_order_indexs)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]\
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
