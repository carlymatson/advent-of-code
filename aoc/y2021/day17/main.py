from pathlib import Path
from pprint import pprint


def triangular_number(n):
    total = 0
    while n > 0:
        total += n
        n -= 1
    return total


def check_initial_velocity(vel_x, vel_y, x_bounds, y_bounds):
    x, y = 0, 0
    steps = 0
    # breakpoint()
    while steps < 500 and (x < x_bounds[1]) and (y > y_bounds[0]):
        x, y = x + vel_x, y + vel_y
        vel_x, vel_y = max(0, vel_x - 1), vel_y - 1
        steps = steps + 1
        if (x_bounds[0] <= x <= x_bounds[1]) and (y_bounds[0] <= y <= y_bounds[1]):
            return True
    return False


def load_input():
    file_path = Path(__file__).parent / "input.txt"
    text = file_path.read_text()


def main():
    peak = triangular_number(175)
    count = 0
    valid = []
    x_bounds = (79, 137)  # maximum x
    # x_bounds = (20, 30)
    y_bounds = (-176, -117)  # minimum y
    # y_bounds = (-10, -5)
    for vel_x in range(5, x_bounds[1] + 1):
        for vel_y in range(y_bounds[0], -y_bounds[0] + 1):
            passes = check_initial_velocity(vel_x, vel_y, x_bounds, y_bounds)
            if passes:
                count += 1
                valid.append((vel_x, vel_y))
    pprint(valid[:20])
    print(count)


if __name__ == "__main__":
    main()
