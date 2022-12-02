from pathlib import Path
from typing import Tuple, List


def load_input() -> List[List[int]]:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    groups = text.split("\n\n")
    int_groups = [[int(n) for n in s.split("\n")] for s in groups]
    return int_groups


def solution() -> Tuple[int, int]:
    int_groups = load_input()

    ### Part 1 ###
    totals = [sum(group) for group in int_groups]
    part_1_solution = max(totals)

    ### Part 2 ###
    sorted_totals = sorted(totals)
    top_3 = sorted_totals[-3:]
    part_2_solution = sum(top_3)

    return part_1_solution, part_2_solution
