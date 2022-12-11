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
        test = lines[3].split(': divisible by ')[1].strip()
        test = int(test)
        if_true = int(lines[4].split(': throw to monkey')[1].strip())
        if_true = int(if_true)
        if_false = int(lines[5].split(': throw to monkey')[1].strip())
        if_false = int(if_false)
        monkeys.append([items, operation, test, if_true, if_false])

    monkey_totals = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in range(20):
        for idx in range(len(monkeys)):
            monkey = monkeys[idx]
            items, operation, test, if_true, if_false = monkey
            to_pop = []
            for index in range(len(items)):
                item = items[index]
                monkey_totals[idx] += 1
                old = item
                result = int(eval(operation))
                result = result // 3
                new_test = int(result) % test
                if new_test == 0:
                    monkeys[if_true][0].append(result)
                    to_pop.append(index)
                else:
                    monkeys[if_false][0].append(result)
                    to_pop.append(index)
            popped = 0
            for index in sorted(to_pop):
                monkeys[idx][0].pop(index - popped)
                popped += 1

    monkey_totals = sorted(
        monkey_totals.items(),
        key=lambda x: x[1], reverse=True,
    )
    return monkey_totals[0][1] * monkey_totals[1][1]


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
