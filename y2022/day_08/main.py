from pathlib import Path
from typing import Tuple, List

from pyadvent.array_2d import Array2D

### Load and Parse ###


def load_input() -> str:
    filepath = Path(__file__).parent / "input.txt"
    text = filepath.read_text().strip()
    trees = Woods.from_string(text, parser=lambda n: int(n))
    return trees


### Solution ###


class Woods(Array2D):
    def eyelines(self, x, y) -> List:
        return [
            self[x, y - 1 :: -1],
            self[x, y + 1 :],
            self[x - 1 :: -1, y],
            self[x + 1 : :, y],
        ]

    def is_visible(self, x, y) -> bool:
        width, height = self.size()
        if x == 0 or x == width - 1 or y == 0 or y == height - 1:
            return True
        tree_height = self[x, y]
        eyelines = self.eyelines(x, y)
        if any([len(el) == 0 for el in eyelines]):
            return True
        return any([max(el) < tree_height for el in eyelines])

    def scenic_score(self, x, y) -> int:
        product = 1
        for el in self.eyelines(x, y):
            count_along_eyeline = 0
            for other_height in el:
                count_along_eyeline += 1
                if other_height >= self[x, y]:
                    break
            product *= count_along_eyeline
        return product


def solution() -> Tuple[int, int]:
    trees = load_input()

    ### Part 1 ###
    visible = [(x, y) for (x, y), _ in trees.enumerate() if trees.is_visible(x, y)]
    part_1_solution = len(visible)

    ### Part 2 ###
    scores = [trees.scenic_score(x, y) for (x, y), _ in trees.enumerate()]
    part_2_solution = max(scores)

    return part_1_solution, part_2_solution
