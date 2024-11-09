"""Day 9: Rope Bridge
https://adventofcode.com/2022/day/9
"""

from pathlib import Path
from typing import Any

from aoc.lib.geometry import DIRECTIONS, Point

input_file = Path(__file__).parent / "input.txt"


class Rope:
    def __init__(self, length: int = 2) -> None:
        self.knots = [Point(0, 0) for _ in range(length)]
        self.tail_visited = set()

    def _get_pixel(self, x: int, y: int) -> str:
        point = Point(x, y)
        if point == self.knots[0]:
            return "H"
        if point == self.knots[-1]:
            return "T"
        if point in self.knots:
            return "*"
        if point in self.tail_visited:
            return "."
        return " "

    def __str__(self) -> str:
        xs = [point.x for point in self.knots + list(self.tail_visited)]
        ys = [point.y for point in self.knots + list(self.tail_visited)]
        pixels = [
            [self._get_pixel(x, y) for x in range(int(min(xs)), int(max(xs)) + 1)]
            for y in range(int(min(ys)), int(max(ys)) + 1)
        ]
        return "\n".join("".join(row) for row in pixels)

    def _tug_next(self, idx: int) -> None:
        if idx + 1 >= len(self.knots):
            return
        dx, dy = self.knots[idx] - self.knots[idx + 1]
        if abs(dx) < 2 and abs(dy) < 2:
            return
        move_dx = int(dx / abs(dx)) if dx else 0
        move_dy = int(dy / abs(dy)) if dy else 0
        self.knots[idx + 1] += Point(move_dx, move_dy)

    def move(self, delta: Point) -> None:
        """Move the head of the chain and adjust following nodes accordingly."""
        self.knots[0] += delta
        for idx in range(len(self.knots)):
            self._tug_next(idx)
        self.tail_visited.add(self.knots[-1])


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.direction_amounts = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> Any:
        return [(line[0], int(line[2:])) for line in raw_input.split("\n")]

    def _apply_directions(self, rope: Rope) -> Rope:
        for direction, amount in self.direction_amounts[:500]:
            vector = DIRECTIONS[direction]
            for _ in range(amount):
                rope.move(vector)
        return rope

    def solve_part_1(self) -> int:
        rope = Rope()
        self._apply_directions(rope)
        return len(rope.tail_visited)

    def solve_part_2(self) -> int:
        rope = Rope(10)
        self._apply_directions(rope)
        return len(rope.tail_visited)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
