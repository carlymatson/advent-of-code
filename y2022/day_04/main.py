from pathlib import Path
from typing import Tuple, List, Dict, Set
from pprint import pprint


def parse_line(s: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    a, b = s.split(",")
    range_1 = tuple([int(n) for n in a.split("-")])
    range_2 = tuple([int(n) for n in b.split("-")])
    return range_1, range_2


def load_input() -> List[int]:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    ranges = [parse_line(line) for line in text.split("\n")]
    return ranges


def contains(range_1: Tuple[int, int], range_2: Tuple[int, int]) -> bool:
    a, b = range_1
    c, d = range_2
    return a <= c and d <= b


def overlap(r1: Tuple[int, int], r2: Tuple[int, int]) -> bool:
    a, b = r1
    c, d = r2
    fully_over = b < c
    fully_under = d < a
    return not fully_over and not fully_under


def solution() -> Tuple[int, int]:
    ranges = load_input()

    ### Part 1 ###
    fully_contains = [1 for r1, r2 in ranges if contains(r1, r2) or contains(r2, r1)]
    part_1_solution = sum(fully_contains)

    ### Part 2 ###
    overlaps = [1 for r1, r2 in ranges if overlap(r1, r2)]
    part_2_solution = sum(overlaps)

    return part_1_solution, part_2_solution
