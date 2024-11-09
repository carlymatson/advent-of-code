from pathlib import Path
from typing import Iterable, Optional

NEEDED_AVAILABLE_SPACE = 30000000

### Parsing Input ###

LsRow = tuple[str, Optional[int]]
Command = tuple[str, str, list[LsRow]]


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


def parse_code(s: str) -> list[Command]:
    s_chunks = s.split("$ ")[1:]
    blocks = [parse_block(b.strip()) for b in s_chunks]
    return blocks


def load_input() -> list[Command]:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    code = parse_code(text)
    return code


### Solution ###


class MockFileSystem:
    TOTAL_SPACE = 70000000

    def __init__(self):
        self.known_paths = {"/": None}
        self.cwd = "/"

    def go_up(self):
        self.cwd = "/".join(self.cwd.split("/")[:-2] + [""])

    def go_down(self, subdir: str):
        self.cwd = self.cwd + subdir + "/"

    def cd(self, arg: str):
        if arg == "..":
            self.go_up()
        elif arg.startswith("/"):
            self.cwd = arg
        else:
            self.go_down(arg)

    def ls(self, outputs: list[LsRow]):
        for child, size in outputs:
            child_path = self.cwd + child
            self.known_paths[child_path] = size

    def exec_cmd(self, op: str, arg: str, outputs: list[LsRow]):
        if op == "cd":
            self.cd(arg)
        elif op == "ls":
            self.ls(outputs)

    def dir_size(self, d: str) -> int:
        contents_file_sizes = [size for f, size in self.iterdir(d) if size is not None]
        return sum(contents_file_sizes)

    def iterdir(self, d: str) -> Iterable[LsRow]:
        return ((f, size) for f, size in self.known_paths.items() if f.startswith(d))

    def files(self) -> list[str]:
        return [f for f, size in self.iterdir("/") if size is not None]

    def dirs(self) -> list[str]:
        return [d for d, size in self.iterdir("/") if size is None]

    def available_space(self) -> int:
        return self.TOTAL_SPACE - self.dir_size("/")


def solution() -> tuple[int, int]:
    commands = load_input()
    file_sys = MockFileSystem()
    for command in commands:
        file_sys.exec_cmd(*command)

    ### Part 1 ###
    dir_sizes = sorted([file_sys.dir_size(d) for d in file_sys.dirs()])
    part_1_solution = sum([d for d in dir_sizes if d <= 100000])

    ### Part 2 ###
    amount_to_delete = NEEDED_AVAILABLE_SPACE - file_sys.available_space()
    smallest = next((d for d in dir_sizes if d >= amount_to_delete))
    part_2_solution = smallest

    return part_1_solution, part_2_solution
