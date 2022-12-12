from __future__ import annotations

import argparse
import functools
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    all_lines = [x for x in s.split('\n\n') if x]
    monkeys = []
    for lines in all_lines:
        lines = lines.splitlines()
        items = [
            int(x.strip())
            for x in lines[1].split(':')[1].split(',') if x
        ]
        operation = lines[2].split(': new = ')[1].strip()
        divisor = int(lines[3].split(': divisible by ')[1].strip())
        if_true = int(lines[4].split(': throw to monkey')[1].strip())
        if_false = int(lines[5].split(': throw to monkey')[1].strip())
        monkeys.append([items, operation, divisor, if_true, if_false])

    monkey_totals = [0] * len(monkeys)
    for _ in range(20):
        for idx in range(len(monkeys)):
            items, operation, divisor, if_true, if_false = monkeys[idx]
            to_pop = []
            for index in range(len(items)):
                monkey_totals[idx] += 1
                old = items[index]  # noqa (used in eval)
                result = int(eval(operation)) // 3
                if result % divisor == 0:
                    monkeys[if_true][0].append(result)
                else:
                    monkeys[if_false][0].append(result)
                to_pop.append(index)
            for index in sorted(to_pop, reverse=True):
                monkeys[idx][0].pop(index)

    monkey_totals = sorted(monkey_totals, reverse=True)

    return monkey_totals[0] * monkey_totals[1]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 10605


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

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
