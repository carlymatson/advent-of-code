import re
from pathlib import Path
from typing import Tuple, List, Dict, Set
from pprint import pprint

### Parse Input ###


Point2D = Tuple[int, int]


def parse_line(s: str) -> List[Point2D]:
    chunks = s.split(" -> ")
    points = [tuple([int(n) for n in c.split(",")]) for c in chunks]
    return points


def load_input() -> List:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    return [parse_line(l) for l in text.split("\n")]


### Solution ###


def get_points(a: Point2D, b: Point2D) -> List[Point2D]:
    assert len(a) == 2 and len(b) == 2
    if a[0] == b[0]:
        min_y, max_y = sorted([a[1], b[1]])
        return [(a[0], y) for y in range(min_y, max_y + 1)]
    elif a[1] == b[1]:
        min_x, max_x = sorted([a[0], b[0]])
        return [(x, a[1]) for x in range(min_x, max_x + 1)]
    else:
        print("Not horizontal or vertical: ", a, b)
    return []


class Sandbox:
    SAND_START = (500, 0)

    def __init__(self, rock_lines: List[Point2D]):
        self.rocks = {
            loc
            for line in rock_lines
            for i in range(len(line) - 1)
            for loc in get_points(line[i], line[i + 1])
        }
        self.sand = set()
        self.current_grain = None
        self.max_y = max((y for x, y in self.rocks))
        self.min_x = min((x for x, y in self.rocks))
        self.max_x = max((x for x, y in self.rocks))

    def move_one(self) -> bool:
        """Moves the current grain of sand if possible."""
        if self.current_grain is None:
            self.current_grain = self.SAND_START
        x, y = self.current_grain
        deltas = [(0, 1), (-1, 1), (1, 1)]
        for dx, dy in deltas:
            new_loc = (x + dx, y + dy)
            if (
                new_loc not in self.rocks
                and new_loc not in self.sand
                and new_loc[1] < self.max_y + 2
            ):
                self.current_grain = new_loc
                return
        # No viable new locations found! Sand is blocked.
        self.sand.add(self.current_grain)
        self.current_grain = None

    def in_free_fall(self) -> bool:
        if self.current_grain is None:
            return False
        return self.current_grain[1] >= self.max_y

    def is_blocked(self) -> bool:
        return self.SAND_START in self.sand

    def __str__(self) -> str:
        pixels = [
            [
                "#" if (x, y) in self.rocks else "o" if (x, y) in self.sand else "."
                for x in range(self.min_x, self.max_x + 1)
            ]
            for y in range(0, self.max_y + 1)
        ]
        return "\n".join(["".join(row) for row in pixels])


def solution() -> Tuple[int, int]:
    rock_lines = load_input()

    ### Part 1 ###
    box = Sandbox(rock_lines=rock_lines)
    for i in range(10000000):
        box.move_one()
        if box.in_free_fall():
            break

    part_1_solution = len(box.sand)

    ### Part 2 ###
    for i in range(10000000):
        box.move_one()
        if box.is_blocked():
            break
    part_2_solution = len(box.sand)
    print(box)

    return part_1_solution, part_2_solution
