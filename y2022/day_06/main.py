from pathlib import Path
from typing import Tuple


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    return text


def find_first_unique_n(s: str, n: int) -> int:
    i = 0
    while i < len(s) - n:
        substring = s[i : i + n]
        if len(set(substring)) == n:
            return i + n
        i += 1


def solution() -> Tuple[int, int]:
    text = load_input()

    ### Part 1 ###
    part_1_solution = find_first_unique_n(text, 4)

    ### Part 2 ###
    part_2_solution = find_first_unique_n(text, 14)

    return part_1_solution, part_2_solution
