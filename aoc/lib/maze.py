import bisect
import functools
from collections.abc import Hashable
from typing import Generic, Protocol, TypeVar

T = TypeVar("T", bound=Hashable)


class Navigable(Protocol, Generic[T]):
    def get_neighbors(self, node: T) -> list[tuple[T, float]]: ...


@functools.total_ordering
class Walk(Generic[T]):
    def __init__(self, nodes: list[T], length: float) -> None:
        self.nodes = tuple(nodes)
        self.length = length

    def __len__(self) -> float:
        return self.length

    def __str__(self) -> str:
        return str(self.nodes)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nodes={self.nodes}, length={self.length})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Walk):
            return False
        return self.nodes == other.nodes and self.length == other.length

    def __lt__(self, other: "Walk") -> bool:
        return self.length < other.length

    def __hash__(self) -> int:
        return hash(tuple(self.nodes))

    def extend(self, node: T, length: float) -> "Walk":
        """Return a new Walk by adding the given node."""
        return type(self)(nodes=[*self.nodes, node], length=self.length + length)


class MazeSolver(Generic[T]):
    def __init__(
        self,
        maze: Navigable[T],
        frontier: list[Walk] | None = None,
    ) -> None:
        self.maze = maze
        self.frontier: list[Walk[T]] = frontier if frontier is not None else []
        self.best_known_route: dict[T, Walk] = dict()

    def record(self, walk: Walk[T]) -> None:
        """Record information on new walk and optionally add to frontier."""
        end = walk.nodes[-1]
        best_route = self.best_known_route.get(end)
        if best_route is None or walk.length < best_route.length:
            self.best_known_route[end] = walk
            bisect.insort(self.frontier, walk)

    def find_extensions(self, walk: Walk[T]) -> list[Walk[T]]:
        """Find all valid extensions of this walk."""
        return [
            walk.extend(neighbor, distance)
            for neighbor, distance in self.maze.get_neighbors(walk.nodes[-1])
        ]

    def explore(self, walk: Walk[T]) -> None:
        """Extends a walk and records the new ones."""
        for new_walk in self.find_extensions(walk):
            self.record(new_walk)

    def search(self, goal: T) -> Walk[T] | None:
        while self.frontier:
            walk = self.frontier.pop(0)
            self.explore(walk)
            if goal in self.best_known_route:
                return self.best_known_route[goal]
