"""Day 2: Cube Conundrum
https://adventofcode.com/2023/day/2
"""

from pathlib import Path
from typing import Any

input_file = Path(__file__).parent / "input.txt"


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.game_counts = self.parse_input(raw_input)

    @staticmethod
    def _parse_game(game: str) -> tuple[int, list[dict[str, int]]]:
        label, data = game.split(": ")
        game_num = int(label.split(" ")[1])
        pulls = [
            [color_count.split(" ") for color_count in pull.split(", ")]
            for pull in data.split("; ")
        ]
        counts = [{color: int(count) for count, color in pull} for pull in pulls]
        return game_num, counts

    def parse_input(self, raw_input: str) -> Any:
        games = [self._parse_game(line) for line in raw_input.strip().split("\n")]
        return {label: counts for label, counts in games}

    def is_possible_pull(self, pull: dict[str, int], available: dict[str, int]) -> bool:
        return all(needed <= available.get(color, 0) for color, needed in pull.items())

    def get_min_needed(self, pulls: list[dict[str, int]]) -> dict[str, int]:
        colors = {color for pull in pulls for color in pull}
        return {
            color: int(max(pull.get(color, 0) for pull in pulls)) for color in colors
        }

    def solve_part_1(self) -> int:
        maxes = {"red": 12, "green": 13, "blue": 14}
        game_ids = [
            game_id
            for game_id, pulls in self.game_counts.items()
            if all(self.is_possible_pull(pull, maxes) for pull in pulls)
        ]
        return sum(game_ids)

    def solve_part_2(self) -> int:
        minimum_sets = [self.get_min_needed(game) for game in self.game_counts.values()]
        powers = (
            counts["red"] * counts["green"] * counts["blue"] for counts in minimum_sets
        )
        return sum(powers)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    print("--- Day 2: Cube Conundrum ---")
    print("https://adventofcode.com/2023/day/2")

    print("(1) What is the sum of the IDs of those games?")
    part_1 = solver.solve_part_1()
    print("Solution: " + str(part_1))
    print("Expected: 2348")

    print("(2) What is the sum of the power of these sets?")
    part_2 = solver.solve_part_2()
    print("Solution: " + str(part_2))
    print("Expected: 76008")
