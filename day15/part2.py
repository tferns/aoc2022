from __future__ import annotations

import argparse
import math
import os.path
from heapq import heappop
from heapq import heappush

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


# def a_star(start, target):
#     visited = {start}
#     queue = [(0, start)]
#     max_coord = start
#     min_coord = start
#     while queue:
#         cost, coord = heappop(queue)
#         max_coord = max(max_coord, coord, key=lambda x: (x[0], x[1]))
#         min_coord = min(min_coord, coord, key=lambda x: (x[0], x[1]))
#         if coord == target:
#             return visited
#         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#             x, y = coord[0] + dx, coord[1] + dy
#             if (x, y) not in visited:
#                 g = cost + 1
#                 h = abs(x - target[0]) + abs(y - target[1])
#                 f = g + h
#                 heappush(queue, (f, (x, y)))
#                 visited.add((x, y))
#     raise ValueError('No path found')
#
#
# def breadth_first(center, target):
#     visited = {center}
#     queue = [center]
#     max_coord = center
#     min_coord = center
#     while queue:
#         coord = queue.pop(0)
#         max_coord = max(max_coord, coord, key=lambda x: (x[0], x[1]))
#         min_coord = min(min_coord, coord, key=lambda x: (x[0], x[1]))
#         if coord == target:
#             return visited
#         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#             x, y = coord[0] + dx, coord[1] + dy
#             if (x, y) not in visited:
#                 visited.add((x, y))
#                 queue.append((x, y))
#     return visited


def compute(s: str) -> int:
    lines = s.splitlines()

    # all_visited = set()
    all_beacons = set()
    all_sensors = set()
    sensor_beacons = []

    for line in lines:
        first_x, second = line.split(': closest beacon is at ')

        fxu, fyu = first_x.split(', ')
        fxu = fxu.replace('Sensor at ', '')
        senx = int(fxu.split('=')[1])
        seny = int(fyu.split('=')[1])

        sxu, syu = second.split(', ')
        # becx = 14
        becx = int(sxu.split('=')[1])
        # becy = 11
        becy = int(syu.split('=')[1])

        distance = abs(senx - becx) + abs(seny - becy)
        beacon = (becx, becy)
        sensor = (senx, seny, distance)

        sensor_beacons.append((sensor, beacon))
        all_beacons.add(beacon)
        all_sensors.add(sensor)

        # all_visited |= a_star(senx, seny, becx, becy)

        # all_beacons.add(beacon)
        #
        # all_visited.add(sensor)
        # all_visited |= a_star(sensor, beacon)

    # all_visited_without_beacons = all_visited - all_beacons
    # all_beacons = {(14, 11)}

    for to_find_y in range(0, 4000000):

        x_ranges = []
        for sensor, beacon in sensor_beacons:
            senx, seny, distance = sensor
            seny_diff_down = seny - distance
            seny_diff_up = seny + distance
            # if to_find_y is between seny_diff_down and senx_diff_up
            if seny_diff_down <= to_find_y <= seny_diff_up:
                width = distance - abs(seny - to_find_y)
                x_ranges.append((senx - width, senx + width))

        # sort x_ranges coords
        x_ranges.sort()

        first_x = x_ranges[0][0]
        for x, y in x_ranges:
            next_x = first_x + 1
            if next_x < x:
                return to_find_y + 4000000 * next_x
            else:
                if first_x < y:
                    first_x = y

    raise ValueError('No solution found')
    # return len(not_a_beacon - all_beacons)


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 56000011


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
