from pathlib import Path

from grid import Grid


def wrap_digit(num):
    num = num % 9
    if num == 0:
        return 9
    return num


def expand_grid(g):
    y_max = len(g)
    x_max = len(g[0])
    big_grid = [
        [wrap_digit(g[y][x] + I + J) for J in range(5) for x in range(x_max)]
        for I in range(5)
        for y in range(y_max)
    ]
    return big_grid


class MazeSolver:
    def __init__(self, start, end, risks):
        self.start = start
        self.end = end
        self.frontier = [start]
        self.least_risk = {start: 0}
        self.risks = risks

    def get_options(self, point):
        neighbors = self.risks.get_connections(*point)
        return [(nb, self.risks.get(*nb)) for nb in neighbors]

    def update_least_risks(self, neighbor, new_risk):
        if neighbor not in self.least_risk or new_risk < self.least_risk[neighbor]:
            self.least_risk[neighbor] = new_risk
            self.frontier.append(neighbor)
        # Add to frontier if need be

    def explore_point(self, point):
        options = self.get_options(point)
        for neighbor, cost in options:
            new_risk = self.least_risk[point] + cost
            self.update_least_risks(neighbor, new_risk)

    def explore(self, max_explored=100000000):
        num_explored = 0
        self.frontier.sort(key=lambda pt: self.least_risk[pt])
        while len(self.frontier) > 0 and num_explored <= max_explored:
            num_explored += 1
            if num_explored % 100000 == 0:
                print(num_explored)
                print(f"Number in self.frontier: {len(self.frontier)}")
            point = self.frontier.pop(0)
            self.explore_point(point)
        return self.least_risk

    def print_costs(self, grid_size=30):
        for y in range(grid_size):
            row = [
                f"{self.least_risk[(x, y)].cost():3}"
                if (x, y) in self.least_risk
                else " - "
                for x in range(grid_size)
            ]
            print(" ".join(row))


def main():
    input_file = Path(__file__).parent / "input.txt"
    text = input_file.read_text()

    risk_grid = [[int(n) for n in row] for row in text.split("\n")]
    risk_grid = expand_grid(risk_grid)
    risks = Grid(risk_grid)

    # Solve maze #
    START = (0, 0)
    END = (len(risk_grid) - 1, len(risk_grid[0]) - 1)
    solver = MazeSolver(START, END, risks)
    routes = solver.explore()
    print(routes)


if __name__ == "__main__":
    main()
