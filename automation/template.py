from pathlib import Path
from typing import Tuple, List, Dict, Set
from pprint import pprint


def parse_line(s: str):
    pass


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    return text


def solution() -> Tuple[int, int]:
    text = load_input()

    ### Part 1 ###
    part_1_solution = None

    ### Part 2 ###
    part_2_solution = None

    return part_1_solution, part_2_solution
