from dataclasses import dataclass, Field
from pathlib import Path
from typing import Tuple, List, Dict, Set, Union, Optional, Iterable
from pprint import pprint

EXAMPLE = """$ cd /
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
7214296 k"""

NEEDED_AVAILABLE_SPACE = 30000000

### Parsing Input ###

LsRow = Tuple[str, Optional[int]]
Command = Tuple[str, str, List[LsRow]]


def parse_ls_line(l: str) -> LsRow:
    size, name = l.split(" ")
    size = None if size == "dir" else int(size)
    return name, size


def parse_block(b: str) -> Command:
    opline, *outputs = b.split("\n")
    opline = opline.lstrip("$ ")
    op = opline[:2]
    arg = opline[2:].strip()
    outputs = [parse_ls_line(l) for l in outputs]
    return op, arg, outputs


def parse_code(s: str) -> List[Command]:
    s_chunks = s.split("$ ")[1:]
    blocks = [parse_block(b.strip()) for b in s_chunks]
    return blocks


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    # text = EXAMPLE
    code = parse_code(text)
    return code


### Solution ###


class MockFileSystem:
    TOTAL_SPACE = 70000000

    def __init__(self):
        self.known_paths = {"/": None}
        self.working_dir = "/"

    def build(self, commands):
        cwd = self.working_dir
        for op, arg, outputs in commands:
            if op == "cd":
                if arg == "..":
                    cwd = "/".join(cwd.split("/")[:-2] + [""])
                elif arg.startswith("/"):
                    cwd = arg
                else:
                    cwd = cwd + arg + "/"
                self.working_dir = cwd
            elif op == "ls":
                # Add to known_paths
                for child, size in outputs:
                    child_path = cwd + child + "/"
                    # If child is directory, size is returned as None.
                    self.known_paths[child_path] = size

    def dir_size(self, dir_path) -> int:
        contents_file_sizes = [
            size
            for f, size in self.known_paths.items()
            if f.startswith(dir_path) and size is not None
        ]
        return sum(contents_file_sizes)

    def files(self) -> List[str]:
        return [f for f, size in self.known_paths.items() if size is not None]

    def dirs(self) -> List[str]:
        return [f for f, size in self.known_paths.items() if size is None]

    def available_space(self) -> int:
        return self.TOTAL_SPACE - self.dir_size("/")


def solution() -> Tuple[int, int]:
    commands = load_input()
    file_sys = MockFileSystem()
    file_sys.build(commands)

    ### Part 1 ###
    dir_sizes = sorted([file_sys.dir_size(d) for d in file_sys.dirs()])
    part_1_solution = sum([d for d in dir_sizes if d <= 100000])

    ### Part 2 ###
    # Find the smallest directory we can delete to free up enough space
    amount_to_delete = NEEDED_AVAILABLE_SPACE - file_sys.available_space()
    smallest = next((d for d in dir_sizes if d >= amount_to_delete))
    part_2_solution = smallest

    return part_1_solution, part_2_solution
