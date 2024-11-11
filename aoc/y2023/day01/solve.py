"""Day 1: Trebuchet?!
https://adventofcode.com/2023/day/1
"""

import re
from pathlib import Path

input_file = Path(__file__).parent / "input.txt"

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


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.lines = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[str]:
        return raw_input.split("\n")

    def get_calibration_value(self, line: str) -> int:
        """Search for first and last numeral 0-9."""
        digits = re.findall(r"\d", line)
        first, last = (digits[0], digits[-1])
        return 10 * int(first) + int(last)

    @staticmethod
    def _get_num(match: str) -> int:
        if match in digit_mappings:
            return digit_mappings[match]
        return int(match)

    def get_calibration_value_2(self, line: str) -> int:
        """Search for first and last digits including spelled numbers."""

        any_digit_pattern = "|".join([r"\d", *digit_mappings.keys()])
        digits_matches = [
            match.group()
            for idx in range(len(line))
            if (match := re.match(any_digit_pattern, line[idx:])) is not None
        ]
        digits = [self._get_num(m) for m in digits_matches]
        first, last = (digits[0], digits[-1])
        return 10 * first + last

    def solve_part_1(self) -> int | None:
        return sum(self.get_calibration_value(line) for line in self.lines)

    def solve_part_2(self) -> int | None:
        return sum(self.get_calibration_value_2(line) for line in self.lines)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    print("--- Day 1: Trebuchet?! ---")
    print("https://adventofcode.com/2023/day/1")

    print("(1) What is the sum of all of the calibration values?")
    part_1 = solver.solve_part_1()
    print("Solution: " + str(part_1))
    print("Expected: 53386")

    print("(2) What is the sum of all of the calibration values?")
    part_2 = solver.solve_part_2()
    print("Solution: " + str(part_2))
    print("Expected: 53312")
