from pathlib import Path
from typing import Any

from aoc.lib.utils import copy_to_clipboard

input_file = Path(__file__).parent / "input.txt"


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.parsed_input = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> Any:
        return raw_input

    def solve_part_1(self) -> int | None:
        return None

    def solve_part_2(self) -> int | None:
        return None


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)
    copy_to_clipboard(part_1)

    # part_2 = solver.solve_part_2()
    # print("Part 2 solution: ", part_2)
    # copy_to_clipboard(part_2)
