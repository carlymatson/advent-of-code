from collections import defaultdict
from pathlib import Path
from typing import Protocol, Tuple

from colored import fore, style


class Grid:
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    CARDINALS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    DIAGONALS = {"UR": (1, -1), "DR": (1, 1), "UL": (-1, -1), "DL": (-1, 1)}

    def __init__(self, grid):
        self.grid = grid
        self.nearest_lowpoint = {}
        self.basin_sizes = defaultdict(lambda: 0)

    @classmethod
    def from_string(cls, text, row_splitter="\n", col_splitter=",", row_parser=None):
        if row_parser is None:
            row_parser = lambda s: s.split(col_splitter)  # Use regex instead?
        rows = text.split(row_splitter)
        grid = [row_parser(row) for row in rows]
        return grid

    def add(pt1, pt2):
        return (pt1[0] + pt2[0], pt1[1] + pt2[1])

    def is_valid(self, x, y):
        x_min, x_max = self.get_bounds("x")
        y_min, y_max = self.get_bounds("y")
        valid_x = (x_min <= x) and (x < x_max)
        valid_y = (y_min <= y) and (y < y_max)
        return valid_x and valid_y

    def get_bounds(self, axis):
        if axis == "x":
            return (0, len(self.grid[0]))
        return (0, len(self.grid))

    def get_neighbors(self, x, y):
        neighbors = []
        for vec in Grid.CARDINALS.values():
            neighbor = (x + vec[0], y + vec[1])
            if self.is_valid(*neighbor):
                neighbors.append(neighbor)
        return neighbors

    def get(self, x, y):
        return self.grid[y][x]

    def print_grid(self, formatter=None, joiner=" ", icon_width=1):
        for row in self.grid:
            if formatter is None:
                formatter = lambda x: f"{x:{icon_width}}"
            formatted_entries = [formatter(x) for x in row]
            print(joiner.join(formatted_entries))

    def is_local_minimum(self, x, y):
        height = self.get(x, y)
        for neighbor in self.get_neighbors(x, y):
            nb_height = self.get(*neighbor)
            if nb_height <= height:
                return False
        return True

    def find_basin(self, x, y):
        basin = set()
        # frontier = set(options)
        frontier = [(x, y)]
        while frontier:
            frontier.sort(key=lambda pt: self.get(*pt))
            point = frontier.pop(0)
            neighbors = [nb for nb in self.get_neighbors(*point) if self.get(*nb) < 9]
            for nb in neighbors:
                if nb not in basin:
                    basin.add(nb)
                    frontier.append(nb)
        return basin

    def score(self):
        score = 0
        basin_sizes = []
        for y in range(*self.get_bounds("y")):
            for x in range(*self.get_bounds("x")):
                if self.is_local_minimum(x, y):
                    score += self.get(x, y) + 1
                    basin = self.find_basin(x, y)
                    basin_sizes.append(len(basin))
        return score, basin_sizes

    def get_icon(self, x, y):
        height = self.get(x, y)
        if height == 9:
            return highlight(str(height), fore.BLUE)
        if self.is_local_minimum(x, y):
            return highlight(str(height))
        return str(height)


def highlight(text, styles=None):
    if styles is None:
        styler = fore.RED + style.BOLD
    else:
        styler = ""
        for s in styles:
            styler += s
    return styler + text + style.RESET


class PrintableGrid(Protocol):
    def get_icon(x: int, y: int) -> str:
        pass

    def get_bounds(axis: str) -> Tuple[int, int]:
        pass


def print_grid(g: PrintableGrid):
    for y in range(*g.get_bounds("y")):
        icons = [g.get_icon(x, y) for x in range(*g.get_bounds("x"))]
        print("".join(icons))


def load_input():
    input_file = Path(__file__).parent / "input.txt"
    text = input_file.read_text()
    nested_array = [[int(n) for n in row] for row in text.split("\n")]
    return Grid(nested_array)


def main(pretty_print=True):
    grid = load_input()
    if pretty_print:
        print_grid(grid)
    risk_level_sum, basin_sizes = grid.score()
    ### Part 1 ###
    print(f"Sum of all risk levels: {risk_level_sum}")
    ### Part 2 ###
    basin_sizes.sort(reverse=True)
    top_3 = basin_sizes[:3]
    top_3_product = top_3[0] * top_3[1] * top_3[2]
    print(f"Product of top 3 basin sizes: {top_3_product}")


if __name__ == "__main__":
    main()
