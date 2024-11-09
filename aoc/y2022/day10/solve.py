"""Day 10: Cathode-Ray Tube
https://adventofcode.com/2022/day/10
"""

from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Computer:
    width = 40
    height = 6

    def __init__(self):
        self.x = 1
        self.x_history = []

    def elapse(self, t: int = 1) -> None:
        self.x_history.extend([self.x for _ in range(t)])

    def run(self, cmd: str, arg: int = 0) -> None:
        if cmd == "noop":
            self.elapse(1)
        elif cmd == "addx":
            self.elapse(2)
            self.x += arg

    def signal_strength(self, cycle: int) -> int:
        return cycle * self.x_history[cycle - 1]

    def is_lit(self, cycle: int) -> bool:
        column = (cycle % self.width) + 1
        sprite_position = self.x_history[cycle]
        overlaps_sprite = sprite_position <= column <= sprite_position + 2
        return overlaps_sprite

    def __str__(self) -> str:
        pixels = [
            [
                "#" if self.is_lit(col + self.width * row) else " "
                for col in range(self.width)
            ]
            for row in range(self.height)
        ]
        return "\n".join(["".join(row) for row in pixels])


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.computer = self.parse_input(raw_input)

    @staticmethod
    def _parse_command(line: str) -> tuple[str, int]:
        parts = line.split(" ")
        op = parts[0]
        arg = int(parts[1]) if len(parts) > 1 else 0
        return op, arg

    def parse_input(self, raw_input: str) -> Computer:
        commands = [self._parse_command(line) for line in raw_input.split("\n")]
        comp = Computer()
        for command in commands:
            comp.run(*command)
        return comp

    def solve_part_1(self) -> int:
        cycles_of_interest = [20, 60, 100, 140, 180, 220]
        signals = [self.computer.signal_strength(c) for c in cycles_of_interest]
        return sum(signals)

    def solve_part_2(self) -> str:
        print("-" * 40)
        print(self.computer)
        print("-" * 40)
        return "printed above ^"


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
