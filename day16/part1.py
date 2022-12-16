from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    rates = {}
    leads = {}
    for line in lines:
        words = line.split(' ')
        start = words[1]
        rate = int(words[4].split('=')[1][:-1])
        rates[start] = rate
        leads_to = ''.join(words[9:]).split(',')
        leads[start] = leads_to

    # @functools.lru_cache(maxsize=None)
    # def get_max_flow(letter: str, ovalves: tuple[tuple], remaining: int) -> int:
    #     if remaining < 1:
    #         return 0
    #
    #     highest = 0
    #
    #     if letter not in ovalves:
    #         score = current_flow_rate * (remaining - 1)
    #         n_ovalves = tuple(sorted(ovalves + tuple(letter)))
    #         for lead in leads[letter]:
    #             if current_flow_rate > 0: # only open if we can get points
    #                 highest = max(highest, score + get_max_flow(lead, n_ovalves, remaining - 2))
    #             # use same ovalves for next cause we didnt open any
    #             highest = max(highest, score + get_max_flow(lead, ovalves, remaining - 1))
    #
    #     return highest
    # return get_max_flow("AA", tuple(), 1000)

    all_states = [('AA', 1, 0, tuple())]
    best_score = 0
    visited_valves = {}
    max_minute = 30

    while all_states:

        current = all_states.pop()
        letter, minute, score, ovalves = current
        unique_ovalves = set(ovalves)
        current_flow_rate = rates[letter]

        for uo in unique_ovalves:
            if uo not in rates:
                rates[uo] = 0

        if visited_valves.get((minute, letter), -float('inf')) > score:
            continue

        visited_valves[(minute, letter)] = score

        if minute >= max_minute:
            best_score = best_score if best_score > score else score
            continue

        if current_flow_rate > 0 and letter not in unique_ovalves:
            unique_ovalves |= {letter}
            pot_higher_score = score + sum(rates[uo] for uo in unique_ovalves)
            new_state = letter, minute + \
                1, pot_higher_score, tuple(unique_ovalves)
            all_states.append(new_state)
            unique_ovalves -= {letter}

        pot_higher_score = score + sum(rates[uo] for uo in unique_ovalves)
        for lead in leads[letter]:
            new_state = lead, minute + \
                1, pot_higher_score, tuple(unique_ovalves)
            all_states.append(new_state)

    return best_score


INPUT_S = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED = 1651


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
