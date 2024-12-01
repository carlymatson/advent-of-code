"""Day 1: Historian Hysteria

https://adventofcode.com/2024/day/1
"""

from pathlib import Path


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.left_list, self.right_list = self.parse_input(raw_input)

    def parse_input(self, raw_input: str) -> tuple[list[int], list[int]]:
        splits = [line.split("   ") for line in raw_input.split("\n")]
        left_list = [int(a) for a, _ in splits]
        right_list = [int(b) for _, b in splits]
        return left_list, right_list

    def solve_part_1(self) -> int | None:
        pairs = list(zip(sorted(self.left_list), sorted(self.right_list)))
        distances = [abs(a - b) for a, b in pairs]
        return sum(distances)

    def solve_part_2(self) -> int | None:
        similarity_scores = [a * self.right_list.count(a) for a in self.left_list]
        return sum(similarity_scores)


def main(
    input_text: str = "",
    input_file: Path = Path(__file__).parent / "input.txt",
) -> None:
    input_ = input_text or input_file.read_text().strip()
    solver = Solver(input_)

    print("--- Day 1: Historian Hysteria ---")
    print("https://adventofcode.com/2024/day/1")

    print("(1) What is the total distance between your lists?")
    part_1 = solver.solve_part_1()
    print("Solution: " + str(part_1))

    print("(2) ")
    part_2 = solver.solve_part_2()
    print("Solution: " + str(part_2))


if __name__ == "__main__":
    main()
