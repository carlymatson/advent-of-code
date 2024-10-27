"""Day 8: Treetop Tree House
https://adventofcode.com/2022/day/8
"""

import math
from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.tree_heights = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> list[list[int]]:
        return [[int(n) for n in line] for line in raw_input.split("\n")]

    def get_sight_lines(self, row: int, col: int) -> list:
        ncols = len(self.tree_heights[0])
        nrows = len(self.tree_heights)
        return [
            [(row, c) for c in reversed(range(col))],
            [(row, c) for c in range(col + 1, ncols)],
            [(r, col) for r in reversed(range(row))],
            [(r, col) for r in range(row + 1, nrows)],
        ]

    def is_visible(self, row: int, col: int) -> bool:
        height = self.tree_heights[row][col]
        return any(
            all(height > self.tree_heights[r][c] for r, c in sight_line)
            for sight_line in self.get_sight_lines(row, col)
        )

    @staticmethod
    def _count_visible_along(height: int, heights: list[int]) -> int:
        count = 0
        for other in heights:
            count += 1
            if other >= height:
                return count
        return count

    def score_view(self, row: int, col: int) -> int:
        height = self.tree_heights[row][col]
        line_heights = [
            [self.tree_heights[r][c] for r, c in line]
            for line in self.get_sight_lines(row, col)
        ]
        line_scores = (
            self._count_visible_along(height, heights) for heights in line_heights
        )
        return math.prod(line_scores)

    def solve_part_1(self) -> int | None:
        visible_trees = [
            (r, c)
            for r in range(len(self.tree_heights))
            for c in range(len(self.tree_heights[0]))
            if self.is_visible(r, c)
        ]
        return len(visible_trees)

    def solve_part_2(self) -> int | None:
        scenic_scores = (
            self.score_view(r, c)
            for r in range(len(self.tree_heights))
            for c in range(len(self.tree_heights[0]))
        )
        return max(scenic_scores)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
