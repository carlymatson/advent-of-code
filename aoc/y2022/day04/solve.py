from pathlib import Path

input_file = Path(__file__).parent / "input.txt"


class Solver:
    def __init__(self, raw_input: str) -> None:
        self.raw_input = raw_input
        self.range_pairs = self.parse_input(raw_input)

    @staticmethod
    def _parse_line(line: str) -> list[tuple[int, int]]:
        pairs = line.split(",")
        split_pairs = [pair.split("-") for pair in pairs]
        return [(int(x), int(y)) for x, y in split_pairs]

    def parse_input(self, raw_input: str) -> list[list[tuple[int, int]]]:
        return [self._parse_line(line) for line in raw_input.split("\n")]

    @staticmethod
    def full_overlap(range_1: tuple[int, int], range_2: tuple[int, int]) -> bool:
        """Return True if one range fully contains the other."""
        if range_1[0] <= range_2[0] and range_1[1] >= range_2[1]:
            return True
        if range_1[0] >= range_2[0] and range_1[1] <= range_2[1]:
            return True
        return False

    @staticmethod
    def any_overlap(range_1: tuple[int, int], range_2: tuple[int, int]) -> bool:
        """Return True if one range fully contains the other."""
        return any(
            range[0] <= endpoint <= range[1]
            for range, endpoint in [
                (range_1, range_2[0]),
                (range_1, range_2[1]),
                (range_2, range_1[0]),
                (range_2, range_1[1]),
            ]
        )

    def solve_part_1(self) -> int | None:
        full_overlaps = [
            pair for pair in self.range_pairs if self.full_overlap(pair[0], pair[1])
        ]
        return len(full_overlaps)

    def solve_part_2(self) -> int | None:
        partial_overlaps = [
            pair for pair in self.range_pairs if self.any_overlap(pair[0], pair[1])
        ]
        return len(partial_overlaps)


if __name__ == "__main__":
    input_ = input_file.read_text().strip()
    solver = Solver(input_)

    part_1 = solver.solve_part_1()
    print("Part 1 solution: ", part_1)

    part_2 = solver.solve_part_2()
    print("Part 2 solution: ", part_2)
