from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass

import pytest

import support

CYCLE_AMOUNT = 500

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class TetrisBlock:
    position: list[tuple[int, int]]


@dataclass
class TetrisRock:
    block: TetrisBlock
    position: list[tuple[int, int]]


class Tetris:
    def __init__(self, directions: str, rocks: list[TetrisBlock]) -> None:
        self.directions = directions
        self.rocks = rocks
        self.rock_count = 0
        self.cycle = 0
        self.highest = -1
        self.tower = set()
        self.mov_map = {'<': -1, '>': 1}
        self.started = False
        self.in_loop = False

    @property
    def dir_len(self):
        return len(self.directions)

    def get_new_rock(self) -> TetrisRock:
        new_rock_template = self.rocks[self.rock_count % 5]
        rock_positions = [
            (y + self.highest + 4, x)
            for y, x in new_rock_template.position
        ]
        return TetrisRock(new_rock_template, rock_positions)

    def move_rock(self, rock: TetrisRock) -> TetrisRock:
        x_movement = self.mov_map[
            self.directions[
                self.cycle % len(
                    self.directions,
                )
            ]
        ]
        rock_positions = [(y, x + x_movement) for y, x in rock.position]
        if any(y < 0 or x < 0 or x > 6 or (y, x) in self.tower for y, x in rock_positions):
            return rock
        rock.position = rock_positions
        return rock

    def move_rock_down(self, rock: TetrisRock) -> bool:
        rock_positions = rock.position.copy()
        for ni, rp in enumerate(rock_positions):
            y, x = rp
            ny, nx = y - 1, x
            if (ny, nx) in self.tower or ny < 0:
                return True
            rock_positions[ni] = (ny, nx)
        rock.position = rock_positions
        return False

    def place_rock(self, rock: TetrisRock) -> None:
        self.tower |= {(y, x) for y, x in rock.position}
        self.highest = max(self.highest, *(y for y, x in rock.position))

    def run(self, iterations: int) -> int:
        while self.rock_count < iterations:
            rock = self.get_new_rock()
            rock_falling = True
            while rock_falling:
                if self.cycle % self.dir_len == 0:
                    if self.rock_count > CYCLE_AMOUNT:
                        self.started = True
                rock = self.move_rock(rock)
                self.cycle += 1
                if self.move_rock_down(rock):
                    self.place_rock(rock)
                    self.rock_count += 1
                    rock_falling = False
            if self.rock_count > CYCLE_AMOUNT and self.started:
                if self.in_loop and all([
                    self.rock_count % self.dir_len == rock_start,
                    self.cycle % self.dir_len == cycle_start,
                ]):
                    ct_length = self.highest - ct_start_highest
                    cr_count = self.rock_count - cr_start_count
                    new_tower, old_highest = self.tower.copy(), self.highest
                    na_cycles = (iterations - self.rock_count) // cr_count
                    self.rock_count += na_cycles * cr_count
                    self.highest += na_cycles * ct_length
                    diff = self.highest - old_highest
                    self.tower = {(y + diff, x) for y, x in new_tower}
                elif not self.in_loop:
                    self.in_loop = True
                    cycle_start, rock_start = self.cycle % self.dir_len, self.rock_count % self.dir_len
                    ct_start_highest, cr_start_count = self.highest, self.rock_count
        return self.highest + 1


def compute(s: str) -> int:
    vline_blocko = TetrisBlock([(0, 2), (0, 3), (0, 4), (0, 5)])
    plus_blocko = TetrisBlock([(0, 3), (1, 2), (1, 3), (1, 4), (2, 3)])
    el_blocko = TetrisBlock([(0, 2), (0, 3), (0, 4), (1, 4), (2, 4)])
    hline_blocko = TetrisBlock([(0, 2), (1, 2), (2, 2), (3, 2)])
    square_blocko = TetrisBlock([(0, 2), (0, 3), (1, 2), (1, 3)])

    rocks = [vline_blocko, plus_blocko, el_blocko, hline_blocko, square_blocko]

    rockfall = Tetris(s, rocks)

    return rockfall.run(1000000000000)


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>\
'''
EXPECTED = 1514285714288


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
