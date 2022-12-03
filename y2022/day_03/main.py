from pathlib import Path
from typing import Tuple, List


EXAMPLE = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def load_input():
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    # text = EXAMPLE
    lines = text.split("\n")
    return lines


def find_common_element(line: str) -> str:
    """Find common character between first and second halves of line."""
    n = len(line)
    first, last = line[: int(n / 2)], line[int(n / 2) :]
    common = set(first).intersection(set(last))
    item = common.pop()
    return item


def priority_score(s: str) -> int:
    """Score character based on position in alphabet."""
    if ord("a") <= ord(s) < ord("a") + 26:
        return ord(s) - ord("a") + 1
    return ord(s) - ord("A") + 27


def find_common(group: List[str]) -> str:
    """Find common character in triplet of strings."""
    a, b, c = [set(x) for x in group]
    common = a.intersection(b).intersection(c)
    item = common.pop()
    return item


def solution() -> Tuple[int, int]:
    lines = load_input()

    ### Part 1 ###
    common_elements = [find_common_element(line) for line in lines]
    priority_scores = [priority_score(elem) for elem in common_elements]
    part_1_solution = sum(priority_scores)

    ### Part 2 ###
    elf_groups = [lines[i : i + 3] for i in range(0, len(lines), 3)]
    print(elf_groups)
    common_elements = [find_common(group) for group in elf_groups]
    priority_scores = [priority_score(s) for s in common_elements]
    part_2_solution = sum(priority_scores)

    return part_1_solution, part_2_solution
