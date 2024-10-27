"""Day 3: Rucksack Reorganization
https://adventofcode.com/2022/day/3
"""

from pathlib import Path

input_file = Path(__file__).parent / "input.txt"

EXAMPLE = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.rucksacks = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[str]:
        return raw_input.split("\n")

    @staticmethod
    def score_item(item: str) -> int:
        if ord("a") <= ord(item) <= ord("z"):
            return ord(item) - ord("a") + 1
        if ord("A") <= ord(item) <= ord("Z"):
            return ord(item) - ord("A") + 27
        raise ValueError("can only score characters a-z and A-Z")

    def solve_part_1(self) -> int | None:
        compartments = [
            (sack[: int(len(sack) / 2)], sack[int(len(sack) / 2) :])
            for sack in self.rucksacks
        ]
        common_items = [
            set(compartment_1).intersection(compartment_2)
            for compartment_1, compartment_2 in compartments
        ]
        assert all(len(items) == 1 for items in common_items)
        return sum(self.score_item(item) for items in common_items for item in items)

    def solve_part_2(self) -> int | None:
        sack_groups = [
            self.rucksacks[idx : idx + 3] for idx in range(0, len(self.rucksacks), 3)
        ]
        common_items = [
            set(sack_1).intersection(sack_2).intersection(sack_3)
            for sack_1, sack_2, sack_3 in sack_groups
        ]
        assert all(len(items) == 1 for items in common_items)
        return sum(self.score_item(item) for items in common_items for item in items)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
