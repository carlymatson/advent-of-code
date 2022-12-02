import bisect
import functools
from numbers import Number
from typing import Any, Optional, List, Protocol, Tuple, Set, Dict, Iterable
from collections import Counter


class Node(Protocol):
    def __hash__(self) -> int:
        pass


class Navigable(Protocol):
    def get_neighbors(self, node: Node) -> Iterable[Tuple[Node, Number]]:
        pass


@functools.total_ordering
class Walk:
    def __init__(self, nodes: List, length: int) -> None:
        self.nodes = tuple(nodes)
        self.node_counts = Counter(nodes)
        self.length = length

    def __str__(self) -> str:
        return str(self.nodes)

    def __repr__(self) -> str:
        return f"Walk(nodes={self.nodes}, length={self.length})"

    def __eq__(self, o: "Walk") -> bool:
        return self.nodes == o.nodes and self.length == o.length

    def __lt__(self, o: "Walk") -> bool:
        return self.length < o.length

    def __hash__(self) -> int:
        return hash(tuple(self.nodes))

    def can_extend(self, node: Node) -> bool:
        """Determines whether extending the walk with the given node is allowed.
        Override this with custom behavior as desired."""
        return node not in self.node_counts

    def extend(self, node: Node, distance: int, prepend: bool = False) -> "Walk":
        """Return a new Walk by adding the given node."""
        new_length = self.length + distance
        if prepend:
            new_nodes = [node] + list(self.nodes)
        else:
            new_nodes = list(self.nodes) + [node]
        return type(self)(nodes=new_nodes, length=new_length)


class MazeSolver:
    def __init__(
        self,
        maze: Navigable,
        frontier: Optional[List[Walk]] = None,
        explore_best_only: bool = True,
    ):
        self.maze = maze
        self.frontier: List[Walk] = frontier if frontier is not None else []
        self.registered: Set[Walk] = set()
        self.explore_best_only = explore_best_only
        self.best_known_route: Dict[Node, Walk] = dict()

    def next_to_explore(self, breadth_first: bool = True) -> Optional[Walk]:
        """Get next walk to explore."""
        if not self.frontier:
            return None
        index = 0 if breadth_first else -1
        node = self.frontier.pop(index)
        return node

    def register(self, walk: Walk) -> None:
        """Record information on new walk and optionally add to frontier."""
        if walk in self.registered:
            return
        self.registered.add(walk)

        end = walk.nodes[-1]
        best_known = self.best_known_route.get(end, None)
        new_best = False
        if best_known is None or walk < best_known:
            self.best_known_route[end] = walk
            new_best = True

        if self.explore_best_only and not new_best:
            return
        bisect.insort(self.frontier, walk)

    def find_extensions(self, walk: Walk) -> List[Walk]:
        """Find all valid extensions of this walk."""
        node = walk.nodes[-1]
        extensions = [
            walk.extend(neighbor, distance)
            for neighbor, distance in self.maze.get_neighbors(node)
            if walk.can_extend(neighbor)
        ]
        return extensions

    def explore_one(self) -> None:
        """Attempts to expand one walk in the frontier."""
        walk = self.next_to_explore()
        if walk is None:
            return
        new_walks = self.find_extensions(walk)
        for new_walk in new_walks:
            self.register(new_walk)

    def more_to_explore(self) -> bool:
        """Checks the frontier for more walks to explore."""
        return len(self.frontier) > 0

    def explore_all(self, starting_walk: Optional[Walk] = None) -> None:
        """Explores walks until there is nothing left to explore."""
        if starting_walk is not None:
            self.register(starting_walk)

        while self.more_to_explore():
            self.explore_one()
            # if len(self.registered) > 155477:
            # print("BIG BIG BIG!!!")
            # break
