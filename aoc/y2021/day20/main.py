from typing import List, Set


def points_of_rectangle(x_bounds, y_bounds):
    points = [
        (x, y)
        for y in range(y_bounds[0], y_bounds[1] + 1)
        for x in range(x_bounds[0], x_bounds[1] + 1)
    ]
    return points


def extract_3_by_3_grid(x: int, y: int, light_pixels: Set) -> str:
    points = points_of_rectangle((x - 1, x + 1), (y - 1, y + 1))
    light_pixels = ["#" if point in light_pixels else "." for point in points]
    return light_pixels


def get_bounds(light_pixels, padding: int = 15) -> List:
    x_vals = [pt[0] for pt in light_pixels]
    y_vals = [pt[1] for pt in light_pixels]
    x_bounds = (min(x_vals) - padding, max(x_vals) + padding)
    y_bounds = (min(y_vals) - padding, max(y_vals) + padding)
    return x_bounds, y_bounds


def get_next_image(light_pixels: Set, enhancement_algorithm: str) -> Set:
    next_turn_light_pixels = set()
    x_bounds, y_bounds = get_bounds(light_pixels)
    grid_points = points_of_rectangle(x_bounds, y_bounds)
    for point in grid_points:
        x, y = point
        neighborhood = extract_3_by_3_grid(x, y, light_pixels)
        num = convert_to_integer(neighborhood)
        if enhancement_algorithm[num] == "#":
            next_turn_light_pixels.add((x, y))
    return next_turn_light_pixels


def convert_to_integer(s: str) -> int:
    digits = [int(c == "#") for c in s]
    powers_of_2 = [2 ** (8 - i) for i in range(9)]
    total = sum([digits[i] * powers_of_2[i] for i in range(9)])
    return total


def parse_input(text: str):
    lines = text.split("\n")
    enhancement_algorithm = lines[0]
    image = lines[2:]
    len_y = len(image)
    len_x = len(image[0])
    light_pixels = set(
        [(x, y) for x in range(len_x) for y in range(len_y) if image[y][x] == "#"]
    )
    return enhancement_algorithm, light_pixels


def print_grid(light_pixels):
    x_bounds, y_bounds = get_bounds(light_pixels)
    print(f"Bounds: {y_bounds}, {x_bounds}")
    for y in range(y_bounds[0], y_bounds[1] + 1):
        for x in range(x_bounds[0], x_bounds[1] + 1):
            symbol = "#" if (x, y) in light_pixels else "."
            print(symbol, end="", flush=False)
        print("")


def part_one(text, verbose=True):
    # FIXME Sometimes background will be lit and contrast is dark!
    enhancement_algorithm, light_pixels = parse_input(text)
    original_bounds = get_bounds(light_pixels)
    image2 = get_next_image(light_pixels, enhancement_algorithm)
    image3 = get_next_image(image2, enhancement_algorithm)
    if verbose:
        print("Step one...")
        print(enhancement_algorithm)
        print(light_pixels)
        print_grid(light_pixels)
        print("-" * 30)
        print_grid(image2)
        print("-" * 30)
        print_grid(image3)
        print("-" * 30)
    grid = points_of_rectangle(*original_bounds)
    restricted = [point for point in image3 if point in grid]
    print(f"Number of lit pixels: {len(restricted)}")


if __name__ == "__main__":
    myinput = "input.txt"
    example = "example.txt"
    with open(myinput, "r") as f:
        text = f.read()
    part_one(text)
