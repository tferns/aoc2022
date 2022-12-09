from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass
from dataclasses import field

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Dir:
    name: str
    parent: Dir | None = None
    dirs: list[Dir] = field(default_factory=list)
    files: list[File] = field(default_factory=list)

    def find_size(self) -> int:
        return sum(f.size for f in self.files) + sum(d.find_size() for d in self.dirs)  # noqa

    def get_full_path(self) -> str:
        path = self.name
        if self.parent:
            path = self.parent.get_full_path() + '/' + path
        return path

    def get_dirs_to_size_map(self, dir_map: dict) -> dict:
        for d in self.dirs:
            unique_path = d.get_full_path()
            dir_map[unique_path] = d.find_size()
            d.get_dirs_to_size_map(dir_map)
        return dir_map


@dataclass
class File:
    name: str
    size: int


SIZE_REQUIRED_TO_FIND = 30000000
TOTAL_SIZE_OF_SYSTEM = 70000000


def compute(s: str) -> int:
    lines = s.splitlines()
    first_line = lines.pop(0)

    _, _, root_dir_name = first_line.split(' ')
    root = Dir(name=root_dir_name, parent=None, dirs=[], files=[])

    current_dir = root
    in_ls = False
    for line in lines:
        if line.startswith('$'):
            in_ls = False
            if line.startswith('$ ls'):
                in_ls = True
            elif line.startswith('$ cd ..'):
                current_dir = current_dir.parent
            else:
                _, dir_name = line.split('$ cd ')
                current_dir = next(
                    d for d in current_dir.dirs if d.name == dir_name
                )
        elif in_ls:
            a, b = line.split()
            if a == 'dir':
                _, dir_name = a, b
                current_dir.dirs.append(Dir(name=dir_name, parent=current_dir))
            else:
                size, filename = int(a), b
                current_dir.files.append(File(name=filename, size=int(size)))

    all_dirs_size = root.get_dirs_to_size_map({})

    remaining = TOTAL_SIZE_OF_SYSTEM - root.find_size()
    space_to_free = SIZE_REQUIRED_TO_FIND - remaining

    possible_deletions = (
        size for name, size in all_dirs_size.items() if size > space_to_free
    )
    return min(possible_deletions)


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642


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
