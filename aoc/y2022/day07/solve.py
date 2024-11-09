"""Day 7: No Space Left On Device
https://adventofcode.com/2022/day/7
"""

import re
from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class FileSystemInfo:
    def __init__(self, total_space: int = 70000000):
        self.disk_usage: dict[str, int | None] = {"/": None}
        self.cwd = "/"
        self.total_space = total_space

    def change_dir(self, arg: str):
        """Change directory."""
        if arg.startswith("/"):
            self.cwd = arg
        elif arg == "..":
            self.cwd = self._go_up(self.cwd)
        else:
            self.cwd = self._go_down(self.cwd, arg)

    @staticmethod
    def _go_up(cwd: str) -> str:
        path_parts = cwd.rstrip("/").split("/")
        return "/".join(path_parts[:-1]) + "/"

    @staticmethod
    def _go_down(cwd: str, subdir: str) -> str:
        return cwd + subdir + "/"

    def record_usage(self, contents: list[tuple[str, int | None]]) -> None:
        """Store the sizes as the contents of the current working directory."""
        for child, size in contents:
            self.disk_usage[self.cwd + child] = size

    def exec_cmd(self, op: str, arg: str, outputs: list[tuple[str, int | None]]):
        """Execute the given command and store the results."""
        if op == "cd":
            self.change_dir(arg)
        elif op == "ls":
            # Record the disk usage
            for child, size in outputs:
                self.disk_usage[self.cwd + child] = size

    def get_path_usage(self, path: str) -> int:
        """Total the disk usage of the path."""
        return sum(
            size
            for descendent, size in self.disk_usage.items()
            if descendent.startswith(path) and size is not None
        )

    def get_directory_sizes(self) -> dict[str, int]:
        return {
            path: self.get_path_usage(path)
            for path, usage in self.disk_usage.items()
            if usage is None
        }

    def get_available_space(self) -> int:
        """Compute available space."""
        return self.total_space - self.get_path_usage("/")


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.file_sys = self.parse_input(raw_input)

    @staticmethod
    def _parse_ls_line(line: str) -> tuple[str, int | None]:
        size_or_dir, name = line.split(" ")
        if size_or_dir == "dir":
            return name, None
        return name, int(size_or_dir)

    def _parse_block(self, block: str) -> tuple[str, str, list[tuple[str, int | None]]]:
        input_, *outputs = block.split("\n")
        try:
            command, arg = input_.split(" ")
        except ValueError:
            command, arg = input_, ""
        parsed_outputs = [self._parse_ls_line(line) for line in outputs]
        return (command, arg, parsed_outputs)

    def parse_input(self, raw_input: str) -> FileSystemInfo:
        pattern = r"^\$ (.*?)(?=\n\$)"
        blocks = re.findall(pattern, raw_input, flags=re.MULTILINE | re.DOTALL)
        command_outputs = (self._parse_block(block) for block in blocks)
        file_sys_info = FileSystemInfo()
        for op, arg, outputs in command_outputs:
            if op == "cd":
                file_sys_info.change_dir(arg)
            elif op == "ls":
                file_sys_info.record_usage(outputs)
        return file_sys_info

    def solve_part_1(self) -> int:
        return sum(
            size
            for size in self.file_sys.get_directory_sizes().values()
            if size < 100000
        )

    def solve_part_2(self) -> int:
        space_needed = 30000000
        space_available = self.file_sys.get_available_space()
        must_delete = space_needed - space_available
        directory_sizes = sorted(self.file_sys.get_directory_sizes().values())
        return next(size for size in directory_sizes if size >= must_delete)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
