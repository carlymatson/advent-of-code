import re
from copy import deepcopy
from pathlib import Path
from typing import Tuple, List, Dict, Set
from pprint import pprint

### Load Input ###

Stacks = Dict[int, List[str]]
StackMove = Tuple[int, int, int]


def transpose(array: List[List]) -> List[List]:
    length, width = len(array), len(array[0])
    transposition = [[array[y][x] for y in range(length)] for x in range(width)]
    return transposition


def parse_move(s: str) -> StackMove:
    # Return amount, source, target
    nums = re.findall("[0-9]+", s)
    return tuple([int(n) for n in nums])


def parse_stacks(s: str) -> Stacks:
    rows = s.split("\n")
    char_array = [[row[i + 1] for i in range(0, 35, 4)] for row in rows]
    transposition = transpose(char_array)
    stacks = {
        int(row.pop(-1)): [c for c in row[::-1] if c != " "] for row in transposition
    }
    return stacks


def load_input() -> Tuple[Stacks, List[StackMove]]:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    stacks_str, moves = text.split("\n\n")
    stacks = parse_stacks(stacks_str)
    lines = [parse_move(line) for line in moves.split("\n")]
    return stacks, lines


### Solution ###


def move_n(
    stacks: Stacks,
    source: int,
    target: int,
    amount: int,
    reverse_order: bool = True,
) -> Dict[int, List]:
    """Remove portion from top of source stack and add to top of target stack."""
    substack = stacks[source][-amount:]
    stacks[source] = stacks[source][:-amount]
    step = -1 if reverse_order else 1
    stacks[target].extend(substack[::step])
    return stacks


def find_top_crates_after_moves(
    stacks: Stacks, moves: List[StackMove], reverse_order: bool = True
) -> str:
    """Perform moves and find top crates. Warning: stacks are modified."""
    for amount, source, target in moves:
        stacks = move_n(stacks, source, target, amount, reverse_order=reverse_order)
    top_crates = [stacks[d][-1] for d in range(1, 10)]
    return "".join(top_crates)


def solution() -> Tuple[int, int]:
    stacks, lines = load_input()

    ### Part 1 ###
    stacks_copy = deepcopy(stacks)
    part_1_solution = find_top_crates_after_moves(stacks_copy, lines)

    ### Part 2 ###
    stacks_copy = deepcopy(stacks)
    part_2_solution = find_top_crates_after_moves(
        stacks_copy, lines, reverse_order=False
    )

    return part_1_solution, part_2_solution
