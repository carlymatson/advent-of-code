"""Day 6: Tuning Trouble
https://adventofcode.com/2022/day/6
"""

from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.signal = raw_input

    def are_last_n_distinct(self, idx: int, n: int = 4) -> bool:
        if idx < n:
            return False
        distinct = set(self.signal[idx - n : idx])
        return len(distinct) == n

    def solve_part_1(self) -> int | None:
        first_marker = next(
            idx for idx in range(len(self.signal)) if self.are_last_n_distinct(idx, n=4)
        )
        return first_marker

    def solve_part_2(self) -> int | None:
        first_message = next(
            idx
            for idx in range(len(self.signal))
            if self.are_last_n_distinct(idx, n=14)
        )
        return first_message


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
