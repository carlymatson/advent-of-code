from functools import total_ordering
from numbers import Number
from typing import List, Optional, Tuple, Dict

Tuple2D = Tuple[int, int]


def enumerate_grid(s: str) -> Tuple[Tuple2D, Dict[Tuple2D, str]]:
    rows = s.split("\n")
    length, width = len(rows), len(rows[0])
    pixels = {
        (x, y): pixel for y, row in enumerate(rows) for x, pixel in enumerate(row)
    }
    return (length, width), pixels


def grid_to_string(
    dimensions: Tuple2D, pixels: Dict[Tuple2D, str], default: str = "."
) -> str:
    x_max, y_max = dimensions
    chars = [[pixels.get((i, j), default) for i in range(x_max)] for j in range(y_max)]
    s = "\n".join(["".join(row) for row in chars])
    return s


@total_ordering
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Point{(self.x, self.y)}"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __add__(self, o: "Point") -> "Point":
        result = Point(self.x + o.x, self.y + o.y)
        return result

    def __sub__(self, o: "Point") -> "Point":
        result = Point(self.x - o.x, self.y - o.y)
        return result

    def __mul__(self, c: Number) -> "Point":
        return Point(self.x * c, self.y * c)

    def __eq__(self, o: object) -> bool:
        return (self.x, self.y) == (o.x, o.y)

    def __lt__(self, o: "Point") -> bool:
        return (self.x, self.y) < (o.x, o.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return hash((self.x, self.y))

    def manhattan_distance(self, o: Optional["Point"] = None):
        if o is None:
            o = Point(0, 0)
        return abs(self.x - o.x) + abs(self.y - o.y)

    def neighbors(self) -> List["Point"]:
        neighbors = [
            Point(self.x + i, self.y + j)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i, j) != (0, 0)
        ]
        return neighbors


CARDINALS = {
    "N": Point(0, 1),
    "S": Point(0, -1),  # Switch since screen is reversed?
    "E": Point(1, 0),
    "W": Point(-1, 0),
}

DIRECTIONS = {
    "U": Point(0, 1),
    "D": Point(0, -1),  # Switch since screen is reversed?
    "R": Point(1, 0),
    "L": Point(-1, 0),
}
