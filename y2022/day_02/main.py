from pathlib import Path
from typing import Tuple


EXAMPLE = """A Y
B X
C Z"""


def letter_to_int(s: str) -> int:
    values = {
        "A": 0,
        "B": 1,
        "C": 2,
        "X": 0,
        "Y": 1,
        "Z": 2,
    }
    return values.get(s)


def load_input():
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    # text = EXAMPLE
    lines = text.split("\n")
    int_pairs = [tuple([letter_to_int(c) for c in line.split(" ")]) for line in lines]
    return int_pairs


def score_pair(my_move: int, win_status: int) -> int:
    return (my_move + 1) + win_status * 3


def score_round(their_move: int, my_move: int) -> int:
    win_status = (my_move - their_move + 1) % 3
    return score_pair(my_move, win_status)


def rescore_round(their_move: int, win_status: int) -> int:
    my_move = (their_move + win_status - 1) % 3
    return score_pair(my_move, win_status)


def solution() -> Tuple[int, int]:
    rounds = load_input()

    ### Part 1 ###
    scores = [score_round(their_move, my_move) for their_move, my_move in rounds]
    part_1_solution = sum(scores)

    ### Part 2 ###
    scores = [
        rescore_round(their_move, win_status) for their_move, win_status in rounds
    ]
    part_2_solution = sum(scores)

    return part_1_solution, part_2_solution
