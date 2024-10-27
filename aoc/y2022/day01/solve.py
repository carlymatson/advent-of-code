"""Day 1: Calorie Counting
https://adventofcode.com/2022/day/1
"""

from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.num_groups = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[list[int]]:
        blocks = raw_input.strip().split("\n\n")
        return [[int(item) for item in block.split()] for block in blocks]

    def solve_part_1(self) -> int:
        group_sums = [sum(group) for group in self.num_groups]
        return max(group_sums)

    def solve_part_2(self) -> int:
        group_sums = [sum(group) for group in self.num_groups]
        top_3_sums = sorted(group_sums, reverse=True)[:3]
        return sum(top_3_sums)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
