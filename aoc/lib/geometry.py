from functools import total_ordering
from typing import Iterator, Self, Sequence


@total_ordering
class Vector:
    def __init__(self, *coords: float):
        self.coords = coords

    def __str__(self) -> str:
        return f"{type(self).__name__}({', '.join(str(c) for c in self.coords)})"

    def __repr__(self) -> str:
        return str(self)

    def _check_same_length(self, other: Self) -> None:
        if len(self.coords) != len(other.coords):
            raise TypeError

    def __len__(self) -> int:
        return len(self.coords)

    def __getitem__(self, idx: int) -> float:
        return self.coords[idx]

    def __add__(self, other: Self) -> Self:
        self._check_same_length(other)
        sums = (self.coords[idx] + other.coords[idx] for idx in range(len(self.coords)))
        return type(self)(*sums)

    def __sub__(self, other: Self) -> Self:
        self._check_same_length(other)
        differences = (
            self.coords[idx] - other.coords[idx] for idx in range(len(self.coords))
        )
        return type(self)(*differences)

    def __mul__(self, constant: float) -> Self:
        scaled = (x * constant for x in self.coords)
        return type(self)(*scaled)

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.coords == other.coords  # pyright: ignore[reportAttributeAccessIssue]

    def __lt__(self, other: Self) -> bool:
        return self.coords < other.coords

    def __iter__(self) -> Iterator:
        for x in self.coords:
            yield x

    def __hash__(self) -> int:
        return hash(self.coords)

    def manhattan_distance(self, other: Self):
        self._check_same_length(other)
        return sum(
            abs(self.coords[idx] - other.coords[idx]) for idx in range(len(self.coords))
        )


class Point(Vector):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def neighbors(self) -> list["Point"]:
        return [
            Point(self.x + i, self.y + j)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if (i, j) != (0, 0)
        ]


CARDINALS = {
    "N": Point(0, 1),
    "S": Point(0, -1),
    "E": Point(1, 0),
    "W": Point(-1, 0),
}

DIRECTIONS = {
    "U": Point(0, 1),
    "D": Point(0, -1),
    "R": Point(1, 0),
    "L": Point(-1, 0),
}


def get_bounds(vectors: Sequence[Vector]) -> list[tuple[float, float]]:
    dimension = len(vectors[0])
    coordinate_values = [
        {vector[idx] for vector in vectors} for idx in range(dimension)
    ]
    return [(min(values), max(values)) for values in coordinate_values]


def get_grid_bounds(vectors: Sequence[Vector]) -> list[tuple[int, int]]:
    bounds = get_bounds(vectors)
    return [(int(min_), int(max_) + 1) for min_, max_ in bounds]
