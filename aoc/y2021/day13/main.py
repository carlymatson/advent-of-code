import re
from pathlib import Path


def fold_point(fold_axis, fold_line, point):
    x, y = point
    if fold_axis == "x":
        new_x = fold_line - abs(x - fold_line)
        new_y = y
    if fold_axis == "y":
        new_x = x
        new_y = fold_line - abs(y - fold_line)
    return (new_x, new_y)


def fold_along(fold, points):
    fold_axis, fold_line = fold.split("=")
    fold_line = int(fold_line)
    folded_points = [fold_point(fold_axis, fold_line, pt) for pt in points]
    return folded_points


def print_points(points):
    x_max = max([pt[0] for pt in points])
    y_max = max([pt[1] for pt in points])
    for y in range(y_max + 1):
        row = ["#" if (x, y) in points else "." for x in range(x_max + 1)]
        print("".join(row))


def main():
    input_file = Path(__file__).parent / "input.txt"
    text = input_file.read_text()
    # Regex matches named capture groups "<x>,<y>|fold along <fold>"
    pattern = "(?P<x>\d+),(?P<y>\d+)|fold along (?P<fold>.+)"
    points_and_folds = (m.groupdict() for m in re.finditer(pattern, text))
    points = []
    folds = []
    for d in points_and_folds:
        if d["x"] is not None:
            x, y = int(d["x"]), int(d["y"])
            points.append((x, y))
        else:
            folds.append(d["fold"])
    folded_points = points
    for fold in folds:
        folded_points = fold_along(fold, folded_points)
    print_points(folded_points)
    print(len(set(folded_points)))


if __name__ == "__main__":
    main()
