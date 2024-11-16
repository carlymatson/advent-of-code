"""Day 1: Trebuchet?!

https://adventofcode.com/2023/day/1
"""

import re
from pathlib import Path

digit_mappings = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
digit_pattern = "|".join([r"\d", *digit_mappings.keys()])


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.lines = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[str]:
        return raw_input.split("\n")

    @staticmethod
    def find_numeral_digits(line: str) -> list[int]:
        return [int(match) for match in re.findall(r"\d", line)]

    @staticmethod
    def find_all_digits(line: str) -> list[int]:
        matches = (
            match.group()
            for idx in range(len(line))
            if (match := re.match(digit_pattern, line[idx:])) is not None
        )
        return [int(digit_mappings.get(match, match)) for match in matches]

    @staticmethod
    def get_calibration_value(digits: list[int]) -> int:
        return 10 * digits[0] + digits[-1]

    def solve_part_1(self) -> int | None:
        return sum(
            self.get_calibration_value(self.find_numeral_digits(line))
            for line in self.lines
        )

    def solve_part_2(self) -> int | None:
        return sum(
            self.get_calibration_value(self.find_all_digits(line))
            for line in self.lines
        )


def main(
    input_text: str = "",
    input_file: Path = Path(__file__).parent / "input.txt",
) -> None:
    """Day 1: Trebuchet?!

    https://adventofcode.com/2023/day/1
    """
    input_ = input_text or input_file.read_text().strip()
    solver = Solver(input_)

    print("(1) What is the sum of all of the calibration values?")
    part_1 = solver.solve_part_1()
    print("Solution: " + str(part_1))

    print("(2) What is the sum of all of the calibration values?")
    part_2 = solver.solve_part_2()
    print("Solution: " + str(part_2))


if __name__ == "__main__":
    main()
