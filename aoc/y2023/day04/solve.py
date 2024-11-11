"""Day 4: Scratchcards
https://adventofcode.com/2023/day/4
"""

import re
from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Scorecard:
    def __init__(self, label: int, nums: list[int], winning: list[int]) -> None:
        self.label = label
        self.nums = nums
        self.winning = winning

    def count_winners(self) -> int:
        return len(set(self.nums).intersection(self.winning))

    def get_score(self) -> int:
        num_winners = self.count_winners()
        if num_winners == 0:
            return 0
        return 2 ** (num_winners - 1)


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.cards = self.parse_input(raw_input)

    @staticmethod
    def _parse_card(line: str) -> Scorecard:
        label, data = line.split(": ")
        card_number = int(label[5:].strip())
        mine, winning = data.split(" | ")
        my_nums = [int(x) for x in re.findall(r"\d+", mine)]
        winning_nums = [int(x) for x in re.findall(r"\d+", winning)]
        return Scorecard(label=card_number, nums=my_nums, winning=winning_nums)

    def parse_input(self, raw_input: str) -> dict[int, Scorecard]:
        cards = (self._parse_card(line) for line in raw_input.split("\n"))
        return {card.label: card for card in cards}

    def count_cards(self, cards: list[Scorecard]) -> dict[int, int]:
        card_counts = {idx: 1 for idx in range(len(cards))}

        for idx, card in enumerate(cards):
            num_copies = card_counts[idx]
            count = card.count_winners()
            for offset in range(count):
                card_counts[idx + offset + 1] += num_copies
        return card_counts

    def solve_part_1(self) -> int | None:
        return sum(card.get_score() for card in self.cards.values())

    def solve_part_2(self) -> int | None:
        counts = self.count_cards(list(self.cards.values()))
        return sum(counts.values())


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    print("--- Day 4: Scratchcards ---")
    print("https://adventofcode.com/2023/day/4")

    print("(1) How many points are they worth in total?")
    part_1 = solver.solve_part_1()
    print("Solution: " + str(part_1))
    print("Expected: 21959")

    print("(2) how many total scratchcards do you end up with?")
    part_2 = solver.solve_part_2()
    print("Solution: " + str(part_2))
    print("Expected: 5132675")
