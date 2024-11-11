"""Day 9: Mirage Maintenance
https://adventofcode.com/2023/day/9
"""

import re
from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.value_sets = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[list[int]]:
        return [
            [int(x) for x in re.findall(r"-?\d+", line)]
            for line in raw_input.split("\n")
        ]

    def get_deltas(self, values: list[int]) -> list[int]:
        return [values[idx + 1] - values[idx] for idx in range(len(values) - 1)]

    def get_all_derivatives(self, values: list[int]) -> list[list[int]]:
        derivatives = [values]
        deltas = values
        for _ in range(len(values)):
            deltas = self.get_deltas(deltas)
            derivatives.append(deltas)
            if all(delta == 0 for delta in deltas):
                break
        return derivatives

    def extend_right(self, values: list[int]) -> int:
        return sum(derivative[-1] for derivative in self.get_all_derivatives(values))

    def extend_left(self, values: list[int]) -> int:
        return sum(
            (-1) ** idx * derivative[0]
            for idx, derivative in enumerate(self.get_all_derivatives(values))
        )

    def solve_part_1(self) -> int | None:
        return sum(self.extend_right(values) for values in self.value_sets)

    def solve_part_2(self) -> int | None:
        return sum(self.extend_left(values) for values in self.value_sets)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    print("--- Day 9: Mirage Maintenance ---")
    print("https://adventofcode.com/2023/day/9")

    print("(1) What is the sum of these extrapolated values?")
    part_1 = solver.solve_part_1()
    print("Solution: " + str(part_1))
    print("Expected: 1980437560")

    print("(2) What is the sum of these extrapolated values?")
    part_2 = solver.solve_part_2()
    print("Solution: " + str(part_2))
    print("Expected: 977")
