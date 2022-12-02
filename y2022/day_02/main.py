from pathlib import Path
from typing import Tuple

from pyadvent import utils

verbose = False


def load_input():
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    return text


def solution() -> Tuple[int, int]:
    text = load_input()

    ### Part 1 ###
    part_1_solution = 0

    ### Part 2 ###
    part_2_solution = 0

    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = solution()
    print(f"Part 1 Solution: {part_1_solution}")
    print(f"Part 2 Solution: {part_2_solution}")
