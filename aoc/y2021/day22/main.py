import re


def load_input(example=None):
    if example is None:
        filename = "input.txt"
    else:
        filename = f"example{example}.txt"
    with open(filename, "r") as f:
        text = f.read()
        f.close()
    # Processing
    int_pattern = "-?\d+"
    nrange_pattern = f"({int_pattern})\.\.({int_pattern})"
    pattern = f"(\w+) x={nrange_pattern},y={nrange_pattern},z={nrange_pattern}"
    steps = re.findall(pattern, text)
    return [
        {
            "switch": step[0] == "on",
            "bounds": [
                (int(step[i]), 1 + int(step[i + 1])) for i in range(1, len(step), 2)
            ],
        }
        for step in steps
    ]


class Grid:
    def __init__(self):
        self.bounds = [[0, 10] for dim in range(3)]
        self.cubes = {}

    def adjust_bounds(self, switch, bounds):
        if switch == False:
            return
        for dim, (lower, upper) in enumerate(bounds):
            if lower < self.bounds[dim][0]:
                self.bounds[dim][0] = lower
            if upper > self.bounds[dim][1]:
                self.bounds[dim][1] = upper

    def get_cubes(self, bounds):
        cubes = (
            (x, y, z)
            for x in range(*bounds[0])
            for y in range(*bounds[1])
            for z in range(*bounds[2])
        )
        return cubes

    def switch_cubes(self, switch, bounds):
        cubes = self.get_cubes(bounds)
        for cube in cubes:
            self.cubes[cube] = switch


def find_last_status(point, steps):
    for step in steps[::-1]:
        if is_in(point, step["bounds"]):
            return step["switch"]
    return False


def is_in(point, bounds):
    for dim in range(3):
        lower, upper = bounds[dim]
        if point[dim] < lower or upper < point[dim]:
            return False
    return True


def main():
    steps = load_input(2)
    grid = Grid()
    for step in steps:
        grid.adjust_bounds(**step)
    print(grid.bounds)
    on_count = 0
    count = 0
    for point in grid.get_cubes(grid.bounds):
        count += 1
        if count % 1000 == 0:
            print(f"...{count}")
        status = find_last_status(point, steps)
        if status:
            on_count += 1
    print(f"Count: {on_count}")


if __name__ == "__main__":
    main()
