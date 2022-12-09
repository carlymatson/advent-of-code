from pathlib import Path
from typing import Tuple, List, Dict, Set
from pprint import pprint
from pyadvent import geometry as geo

### Parse Input ###


def parse_line(s: str):
    pass


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    lines = [line.split() for line in text.split("\n")]
    moves = [(a, int(b)) for a, b in lines]
    return moves


### Solution ###


class Rope:
    def __init__(self, length: int = 2):
        self.head = geo.Point(0, 0)
        self.tail = geo.Point(0, 0)
        self.chain = [geo.Point(0, 0) for _ in range(length)]
        self.visited = set()
        self.visited.add(self.tail)
        self.length = length

    def move_head(self, dir, amt):
        vec = geo.DIRECTIONS[dir]
        for _ in range(amt):
            self.chain[0] += vec
            for knot in range(1, self.length):
                self.move_tail(knot)
            self.visited.add(self.chain[-1])

    def move_tail(self, knot):
        delta = self.chain[knot - 1] - self.chain[knot]
        dx, dy = delta
        if abs(dx) >= 2 or abs(dy) >= 2:
            if abs(dx) > 1:
                dx = int(dx / 2)
            if abs(dy) > 1:
                dy = int(dy / 2)
            self.chain[knot] += geo.Point(dx, dy)


def solution() -> Tuple[int, int]:
    moves = load_input()

    ### Part 1 ###
    rope = Rope(2)
    for dir, amt in moves:
        rope.move_head(dir, amt)
    part_1_solution = len(rope.visited)

    ### Part 2 ###
    rope = Rope(10)
    for dir, amt in moves:
        rope.move_head(dir, amt)
    part_2_solution = len(rope.visited)

    return part_1_solution, part_2_solution
