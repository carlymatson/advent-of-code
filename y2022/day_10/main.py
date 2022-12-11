from pathlib import Path
from typing import Tuple, List, Dict, Set, Optional
from pprint import pprint

### Parse Input ###


def parse_command(s: str) -> Tuple[str, int]:
    op = s[:4]
    arg = int(s[5:]) if op == "addx" else None
    return op, arg


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    commands = (parse_command(l) for l in text.split("\n"))
    return commands


### Solution ###

CYCLES_OF_INTEREST = [20, 60, 100, 140, 180, 220]


class Computer:
    width = 40
    height = 6

    def __init__(self):
        self.x = 1
        self.x_values = []

    def elapse(self, t: int = 1) -> None:
        for _ in range(t):
            self.x_values.append(self.x)

    def run(self, cmd: str, arg: Optional[int]) -> None:
        if cmd == "noop":
            self.elapse(1)
        elif cmd == "addx":
            self.elapse(2)
            self.x += arg

    def signal_strength(self, cycle: int) -> int:
        return cycle * self.x_values[cycle - 1]

    def is_lit(self, n: int) -> bool:
        col = n % self.width
        position = self.x_values[n]
        lit = position - 1 <= col <= position + 1
        return lit

    def __str__(self) -> str:
        num_pixels = self.width * self.height
        pixels = ["#" if self.is_lit(n) else " " for n in range(num_pixels)]
        rows = [pixels[i : i + self.width] for i in range(0, num_pixels, self.width)]
        return "\n".join(["".join(row) for row in rows])


def solution() -> Tuple[int, int]:
    commands = load_input()
    comp = Computer()
    for cmd, arg in commands:
        comp.run(cmd, arg)

    ### Part 1 ###
    signals = [comp.signal_strength(c) for c in CYCLES_OF_INTEREST]
    part_1_solution = sum(signals)

    ### Part 2 ###
    # Solution must be read from terminal
    print(str(comp))
    part_2_solution = "RZEKEFHA"

    return part_1_solution, part_2_solution
