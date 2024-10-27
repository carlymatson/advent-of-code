"""Day 2: Rock Paper Scissors
https://adventofcode.com/2022/day/2
"""

from enum import Enum
from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


abc_shapes = {
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
}
xyz_shapes = {
    "X": Shape.ROCK,
    "Y": Shape.PAPER,
    "Z": Shape.SCISSORS,
}
xyz_outcomes = {
    "X": Outcome.LOSS,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}

EXAMPLE = """A Y
B X
C Z"""


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.strategy_guide = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[tuple[str, str]]:
        return [(line[0], line[2]) for line in raw_input.split("\n")]

    def get_outcome(self, theirs: Shape, mine: Shape) -> Outcome:
        if mine == theirs:
            return Outcome.DRAW
        i_win = (mine.value - theirs.value) % 3 == 1
        return Outcome.WIN if i_win else Outcome.LOSS

    def score_round(self, theirs: Shape, mine: Shape) -> int:
        outcome = self.get_outcome(theirs, mine)
        return mine.value + outcome.value

    def find_move(self, theirs: Shape, outcome: Outcome) -> Shape:
        if outcome == Outcome.DRAW:
            return theirs

        moves_to_make = {
            (Shape.ROCK, Outcome.WIN): Shape.PAPER,
            (Shape.ROCK, Outcome.LOSS): Shape.SCISSORS,
            (Shape.PAPER, Outcome.WIN): Shape.SCISSORS,
            (Shape.PAPER, Outcome.LOSS): Shape.ROCK,
            (Shape.SCISSORS, Outcome.WIN): Shape.ROCK,
            (Shape.SCISSORS, Outcome.LOSS): Shape.PAPER,
        }
        return moves_to_make[(theirs, outcome)]

    def solve_part_1(self) -> int | None:
        rounds = [
            (abc_shapes[their_move], xyz_shapes[my_move])
            for their_move, my_move in self.strategy_guide
        ]
        scores = [self.score_round(theirs, mine) for theirs, mine in rounds]
        return sum(scores)

    def solve_part_2(self) -> int | None:
        rounds = [
            (abc_shapes[their_move], xyz_outcomes[outcome])
            for their_move, outcome in self.strategy_guide
        ]
        moves = [
            (their_move, self.find_move(their_move, outcome))
            for their_move, outcome in rounds
        ]
        scores = [self.score_round(*move_pair) for move_pair in moves]
        return sum(scores)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
