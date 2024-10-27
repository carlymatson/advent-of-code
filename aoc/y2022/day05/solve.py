"""Day 5: Supply Stacks
https://adventofcode.com/2022/day/5
"""

import re
from enum import Enum, auto
from pathlib import Path
from typing import Any

input_file = Path(__file__).parent / "input.txt"


class MoveMode(Enum):
    ONE_AT_A_TIME = auto()
    ALL_AT_ONCE = auto()


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        stacks, instructions = self.parse_input(raw_input)
        self.stacks = stacks
        self.instructions = instructions

    def parse_input(self, raw_input: str) -> Any:
        lines = raw_input.split("\n")
        label_line_idx, label_line = next(
            (idx, line) for idx, line in enumerate(lines) if line.startswith(" 1 ")
        )
        stack_labels = [label for label in label_line.split() if label]
        stacks = {
            label: [
                crate
                for row in reversed(range(label_line_idx))
                if (crate := lines[row][1 + 4 * col]) != " "
            ]
            for col, label in enumerate(stack_labels)
        }
        instructions = [
            (int(match[0]), match[1], match[2])
            for line in lines[label_line_idx + 2 :]
            for match in re.findall(r"move (\d+) from (\d+) to (\d+)", line)
        ]
        return stacks, instructions

    def move_crates(
        self,
        number: int,
        from_stack: str,
        to_stack: str,
        mode: MoveMode = MoveMode.ONE_AT_A_TIME,
    ) -> None:
        to_move = self.stacks[from_stack][-number:]
        to_append = reversed(to_move) if mode == MoveMode.ONE_AT_A_TIME else to_move
        self.stacks[from_stack] = self.stacks[from_stack][:-number]
        self.stacks[to_stack] += to_append

    def solve_part_1(self) -> str | None:
        for number, to_, from_ in self.instructions:
            self.move_crates(number, to_, from_)
        top_crates = [stack[-1] for stack in self.stacks.values()]
        return "".join(top_crates)

    def solve_part_2(self) -> str | None:
        for number, to_, from_ in self.instructions:
            self.move_crates(number, to_, from_, mode=MoveMode.ALL_AT_ONCE)
        top_crates = [stack[-1] for stack in self.stacks.values()]
        return "".join(top_crates)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    solver = Solver(input_)
    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
