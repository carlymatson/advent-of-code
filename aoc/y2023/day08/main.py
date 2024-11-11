from pathlib import Path
from pprint import pprint

INPUT_FILE = Path(__file__).parent / "input.txt"


class UnfindableError(Exception): ...


class Graph:
    def __init__(self, nodes: dict[str, tuple[str, str]]) -> None:
        self.nodes = nodes

    def find_path(self, target: str, steps: str) -> int:
        node = "AAA"
        count = 0
        for _ in range(10000000):
            for step in steps:
                if node == target:
                    return count
                index = 0 if step == "L" else 1
                next_node = self.nodes[node][index]
                node = next_node
                count += 1
        raise UnfindableError

    def find_ghost_path(self, steps: str) -> int:
        nodes = [node for node in self.nodes if node.endswith("A")]
        count = 0
        for _ in range(10000000):
            for step in steps:
                if all(node.endswith("Z") for node in nodes):
                    return count
                index = 0 if step == "L" else 1
                next_nodes = [self.nodes[node][index] for node in nodes]
                nodes = next_nodes
                count += 1
        raise UnfindableError


def load_input(text: str) -> tuple[str, Graph]:
    instructions, _, *tail = text.splitlines()
    nodes = [(line[0:3], line[7:10], line[12:15]) for line in tail]
    graph = Graph(
        {node: (left, right) for node, left, right in nodes},
    )
    return instructions, graph


def solve_part_1(input_: str) -> int:
    instructions, graph = load_input(input_)
    count = graph.find_path("ZZZ", instructions)
    print("Part 1: ", count)
    return count


def solve_part_2(input_: str) -> int:
    instructions, graph = load_input(input_)
    count = graph.find_ghost_path(instructions)
    print("Part 2: ", count)
    return count


EXAMPLE = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

EXAMPLE_2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


if __name__ == "__main__":
    my_input = INPUT_FILE.read_text()
    # my_input = EXAMPLE_2
    solve_part_1(my_input)
    solve_part_2(my_input)
